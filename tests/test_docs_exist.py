from pathlib import Path


def test_docs_exist_and_have_key_titles():
    repo_root = Path(__file__).resolve().parents[1]
    workflow = repo_root / "docs" / "WORKFLOW.md"
    entities = repo_root / "docs" / "ENTITIES.md"
    integration = repo_root / "docs" / "INTEGRATION_A9.md"

    assert workflow.exists()
    assert entities.exists()
    assert integration.exists()

    workflow_text = workflow.read_text(encoding="utf-8")
    entities_text = entities.read_text(encoding="utf-8")
    integration_text = integration.read_text(encoding="utf-8")

    assert "Standard start" in workflow_text
    assert "Entities" in entities_text
    assert "Integration: a9quant" in integration_text
