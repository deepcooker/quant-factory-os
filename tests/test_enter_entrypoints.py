from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def _make_fake_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "tools").mkdir(parents=True)
    (repo / "bin").mkdir(parents=True)
    shutil.copy2(Path("tools/enter.sh"), repo / "tools/enter.sh")

    _write_executable(
        repo / "tools/doctor.sh",
        "#!/usr/bin/env bash\nset -euo pipefail\nexit 0\n",
    )
    _write_executable(
        repo / "bin/git",
        """#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "rev-parse" && "${2:-}" == "--show-toplevel" ]]; then
  pwd
  exit 0
fi
if [[ "${1:-}" == "branch" && "${2:-}" == "--show-current" ]]; then
  echo "test-branch"
  exit 0
fi
if [[ "${1:-}" == "diff" ]]; then
  exit 0
fi
if [[ "${1:-}" == "ls-files" ]]; then
  exit 0
fi
if [[ "${1:-}" == "pull" && "${2:-}" == "--rebase" ]]; then
  exit 0
fi
echo "unexpected git command: $*" >&2
exit 1
""",
    )
    return repo


def _run_enter(repo: Path, run_id: str | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{repo / 'bin'}:{env['PATH']}"
    if run_id is None:
        env.pop("RUN_ID", None)
    else:
        env["RUN_ID"] = run_id
    return subprocess.run(
        ["bash", "tools/enter.sh"],
        cwd=repo,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_enter_prints_entrypoints(tmp_path: Path) -> None:
    repo = _make_fake_repo(tmp_path)
    proc = _run_enter(repo)
    output = proc.stdout + proc.stderr
    assert proc.returncode == 0
    assert "Entry points:" in output
    assert "TASKS/STATE.md" in output
    assert "TASKS/QUEUE.md" in output


def test_enter_prints_run_id_when_set(tmp_path: Path) -> None:
    repo = _make_fake_repo(tmp_path)
    proc = _run_enter(repo, run_id="run-test")
    output = proc.stdout + proc.stderr
    assert proc.returncode == 0
    assert "RUN_ID: run-test" in output
