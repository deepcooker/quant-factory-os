from pathlib import Path


def test_no_raw_run_id_placeholder_in_docs_templates_and_queue():
    repo_root = Path(__file__).resolve().parents[1]
    paths = [
        repo_root / "TASKS" / "_TEMPLATE.md",
        repo_root / "TASKS" / "QUEUE.md",
        repo_root / "docs" / "WORKFLOW.md",
    ]
    for path in paths:
        content = path.read_text(encoding="utf-8")
        assert "<RUN_ID>" not in content, f"raw placeholder found in {path}"


def test_gitignore_includes_pytest_and_python_cache_rules():
    repo_root = Path(__file__).resolve().parents[1]
    content = (repo_root / ".gitignore").read_text(encoding="utf-8")
    for token in [".pytest_cache/", "__pycache__/", "*.py[cod]", ".venv/", "venv/"]:
        assert token in content, f"missing ignore rule: {token}"
