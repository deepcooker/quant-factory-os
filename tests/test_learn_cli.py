from __future__ import annotations

from tools.learn import parse_cli


def test_parse_cli_defaults_to_gpt_5_4() -> None:
    cfg = parse_cli([])
    assert cfg["model_name"] == "gpt-5.4"


def test_parse_cli_accepts_model_equals_override() -> None:
    cfg = parse_cli(["model=gpt-5.3-codex"])
    assert cfg["model_name"] == "gpt-5.3-codex"


def test_parse_cli_accepts_dash_model_override() -> None:
    cfg = parse_cli(["-model", "gpt-5.2-codex"])
    assert cfg["model_name"] == "gpt-5.2-codex"
