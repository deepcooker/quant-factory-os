import os
import subprocess


def run_parse(input_text: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["SHIP_RUN_ID_PARSE_ONLY"] = "1"
    env["SHIP_RUN_ID_PARSE_INPUT"] = input_text
    return subprocess.run(
        ["bash", "tools/ship.sh", "parse-run-id"],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_ship_parse_runid_trims_trailing_colon() -> None:
    res = run_parse("run-2026-02-27-session-conversation-fallback-log:")
    assert res.returncode == 0
    assert "PARSED_RUN_ID: run-2026-02-27-session-conversation-fallback-log" in res.stdout


def test_ship_parse_runid_from_sentence_with_punctuation() -> None:
    res = run_parse(
        "run-2026-02-27-ship-runid-normalization: fix run id parser and keep paths clean."
    )
    assert res.returncode == 0
    assert "PARSED_RUN_ID: run-2026-02-27-ship-runid-normalization" in res.stdout
