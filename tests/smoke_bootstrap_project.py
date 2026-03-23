from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    target = Path("/tmp/demo-bootstrap-runnable")
    if target.exists():
        shutil.rmtree(target)

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/bootstrap_experiment_project.py",
            str(target),
            "--with-core-skills",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr

    result = json.loads(proc.stdout)
    assert result["ok"] is True
    assert result["validation"]["skills_non_empty"] is True
    assert result["validation"]["skills_paths_exist"] is True

    config = json.loads((target / "tools" / "project_config.json").read_text(encoding="utf-8"))
    assert config["skills"]

    for rel in [
        "AGENTS.md",
        "docs/PROJECT_GUIDE.md",
        "docs/WORKFLOW.md",
        "docs/NEXT_STEPS.md",
    ]:
        assert (target / rel).exists()

    for rel in config["skills"].values():
        assert (target / rel).exists()

    print("SMOKE_BOOTSTRAP_PROJECT_OK")


if __name__ == "__main__":
    main()
