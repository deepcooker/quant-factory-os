from pathlib import Path


def test_ship_untracked_allowlist_includes_docs():
    ship_script = Path("tools/ship.sh")
    content = ship_script.read_text(encoding="utf-8")
    assert "tools/*|tests/*|TASKS/*|docs/*|Makefile" in content
