from pathlib import Path


def test_enter_script_contains_explicit_autostash_switch():
    repo_root = Path(__file__).resolve().parents[1]
    content = (repo_root / "tools" / "enter.sh").read_text(encoding="utf-8")
    assert "ENTER_AUTOSTASH" in content
    assert "QF_AUTOSTASH" in content
    assert "tools/qf init" in content
