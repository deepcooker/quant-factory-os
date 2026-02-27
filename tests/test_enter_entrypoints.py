from pathlib import Path


def test_enter_script_is_qf_init_wrapper() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    text = (repo_root / "tools" / "enter.sh").read_text(encoding="utf-8")
    assert "tools/qf init" in text
    assert "NOTICE: tools/enter.sh is deprecated" in text


def test_enter_maps_legacy_autostash_env() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    text = (repo_root / "tools" / "enter.sh").read_text(encoding="utf-8")
    assert "ENTER_AUTOSTASH" in text
    assert "QF_AUTOSTASH" in text
