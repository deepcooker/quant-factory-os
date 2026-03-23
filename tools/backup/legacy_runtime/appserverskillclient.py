#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_SKILLS_DIR = REPO_ROOT / ".agents" / "skills"


def _load_skill_metadata(skill_name: str) -> dict[str, Any]:
    skill_dir = LOCAL_SKILLS_DIR / skill_name
    skill_md = skill_dir / "SKILL.md"
    yaml_file = skill_dir / "agents" / "openai.yaml"
    if not skill_md.is_file():
        raise FileNotFoundError(f"repo-local skill not found: {skill_name} ({skill_md})")
    metadata: dict[str, Any] = {
        "skill_name": skill_name,
        "skill_dir": str(skill_dir),
        "skill_md": str(skill_md),
        "display_name": skill_name,
        "default_prompt": "",
    }
    if yaml_file.is_file():
        raw = yaml_file.read_text(encoding="utf-8", errors="replace")
        for line in raw.splitlines():
            stripped = line.strip()
            if stripped.startswith("display_name:"):
                metadata["display_name"] = stripped.split(":", 1)[1].strip().strip("\"'")
            if stripped.startswith("default_prompt:"):
                metadata["default_prompt"] = stripped.split(":", 1)[1].strip().strip("\"'")
    return metadata


def build_explicit_skill_prompt(skill_name: str, prompt: str) -> str:
    body = str(prompt or "").strip()
    if body:
        return f"Use ${skill_name} {body}"
    return f"Use ${skill_name}"


def call_skill(
    *,
    skill_name: str,
    prompt: str,
    cwd: Path,
    model: str = "",
) -> dict[str, Any]:
    metadata = _load_skill_metadata(skill_name)
    final_prompt = build_explicit_skill_prompt(
        skill_name,
        prompt or str(metadata.get("default_prompt") or ""),
    )
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as fp:
        last_message_path = Path(fp.name)
    cmd = [
        "codex",
        "exec",
        "--dangerously-bypass-approvals-and-sandbox",
        "-C",
        str(cwd),
        "-o",
        str(last_message_path),
    ]
    if model:
        cmd.extend(["-m", model])
    cmd.append(final_prompt)
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    last_message = ""
    if last_message_path.is_file():
        last_message = last_message_path.read_text(encoding="utf-8", errors="replace").strip()
        try:
            last_message_path.unlink()
        except OSError:
            pass
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "skill_name": skill_name,
        "display_name": metadata["display_name"],
        "skill_dir": metadata["skill_dir"],
        "cwd": str(cwd),
        "prompt": final_prompt,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "last_message": last_message,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Experimental Python client for explicit Codex skill invocation."
    )
    parser.add_argument("--skill", required=True, help="repo-local skill name under .agents/skills")
    parser.add_argument(
        "--prompt",
        default="",
        help="extra prompt text appended after `Use $skill-name`; falls back to skill default_prompt when empty",
    )
    parser.add_argument("--cwd", default=str(REPO_ROOT), help="working directory for codex exec")
    parser.add_argument("--model", default="", help="optional model override")
    args = parser.parse_args()

    result = call_skill(
        skill_name=args.skill,
        prompt=args.prompt,
        cwd=Path(args.cwd).resolve(),
        model=args.model,
    )
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0 if result["ok"] else int(result["returncode"] or 1)


if __name__ == "__main__":
    raise SystemExit(main())
