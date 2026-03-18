#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

# 在这里维护真实试点项目；也支持命令行继续追加。
SYNC_TARGET_PROJECT_ROOTS = [
    "/root/a9quant-strategy",
]

# 只同步 foundation tools 层和 prompts，不碰目标项目自己的 project_config.json。
SYNC_RELATIVE_PATHS = [
    "docs/FOUNDATION_BRIDGE.md",
    "tools/appserverclient.py",
    "tools/codex_transport.py",
    "tools/common_helpers.py",
    "tools/evidence.py",
    "tools/gitclient.py",
    "tools/init.py",
    "tools/project_config.py",
    "tools/project_config.template.json",
    "tools/result_schema.py",
    "tools/slice.py",
    "tools/sync_tools.py",
    "tools/taskclient.py",
    "tools/view.sh",
    "tools/prompts/init_project_prompt.md",
    "tools/prompts/learnbaseline_prompt.md",
    "tools/prompts/refresh_baseline_prompt.md",
    "tools/prompts/summarize_current_prompt.md",
    "tools/prompts/summarize_role_prompt.md",
]


def parse_args(argv: list[str]) -> tuple[list[Path], bool]:
    targets: list[Path] = []
    dry_run = False
    idx = 0
    while idx < len(argv):
        token = str(argv[idx]).strip()
        if token in {"-n", "--dry-run"}:
            dry_run = True
            idx += 1
            continue
        if token in {"-p", "--project-root"}:
            if idx + 1 >= len(argv):
                raise SystemExit("--project-root requires a path")
            targets.append(Path(str(argv[idx + 1]).strip()).resolve())
            idx += 2
            continue
        raise SystemExit(f"unknown argument: {token}")
    if not targets:
        targets = [Path(path).resolve() for path in SYNC_TARGET_PROJECT_ROOTS]
    return targets, dry_run


def validate_target(project_root: Path) -> None:
    if not project_root.exists():
        raise SystemExit(f"target project_root does not exist: {project_root}")
    if not project_root.is_dir():
        raise SystemExit(f"target project_root is not a directory: {project_root}")
    if project_root.resolve() == REPO_ROOT.resolve():
        raise SystemExit("refusing to sync tools into the foundation repo itself")


def sync_one(project_root: Path, dry_run: bool) -> dict[str, object]:
    validate_target(project_root)
    copied: list[str] = []
    for rel in SYNC_RELATIVE_PATHS:
        src = (REPO_ROOT / rel).resolve()
        dst = (project_root / rel).resolve()
        if not src.exists():
            raise SystemExit(f"source path missing: {src}")
        if dry_run:
            copied.append(rel)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)
    return {
        "project_root": str(project_root),
        "dry_run": dry_run,
        "copied": copied,
    }


def main(argv: list[str]) -> int:
    targets, dry_run = parse_args(argv)
    results = [sync_one(project_root, dry_run=dry_run) for project_root in targets]
    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
