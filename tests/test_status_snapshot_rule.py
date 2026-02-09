from pathlib import Path


def test_status_snapshot_rule_documented():
    repo_root = Path(__file__).resolve().parents[1]
    workflow_doc = repo_root / "docs" / "WORKFLOW.md"
    if workflow_doc.exists():
        content = workflow_doc.read_text(encoding="utf-8")
        assert "/status" in content
        return

    readme = repo_root / "README.md"
    content = readme.read_text(encoding="utf-8")
    assert "/status" in content
