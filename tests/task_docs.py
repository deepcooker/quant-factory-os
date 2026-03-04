from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_docs_owner_files_exist() -> None:
    required = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs" / "WORKFLOW.md",
        REPO_ROOT / "docs" / "PROJECT_GUIDE.md",
        REPO_ROOT / "docs" / "ENTITIES.md",
        REPO_ROOT / "docs" / "CODEX_CLI_OPERATION.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"missing docs: {missing}"

