from pathlib import Path


def test_enter_delegates_to_qf_init():
    repo_root = Path(__file__).resolve().parents[1]
    enter_text = (repo_root / "tools" / "enter.sh").read_text(encoding="utf-8")

    assert "tools/qf init" in enter_text
    assert "QF_AUTOSTASH" in enter_text


def test_start_delegates_to_qf_init():
    repo_root = Path(__file__).resolve().parents[1]
    start_text = (repo_root / "tools" / "start.sh").read_text(encoding="utf-8")

    assert "bash tools/qf init" in start_text
