from __future__ import annotations

import json
from pathlib import Path

from tools import codex_transport as ct


def test_runtime_reasoning_effort_minimal_upgrade() -> None:
    eff, reason = ct.runtime_reasoning_effort("minimal")
    assert eff == "low"
    assert "upgraded-to-low" in reason

    eff2, reason2 = ct.runtime_reasoning_effort("high")
    assert eff2 == "high"
    assert reason2 == "as-requested"


def test_extract_command_evidence_exec_and_app_server(tmp_path: Path) -> None:
    events = tmp_path / "events.jsonl"
    lines = [
        json.dumps(
            {
                "item": {
                    "type": "command_execution",
                    "raw_input": "/bin/bash -lc tools/view.sh docs/PROJECT_GUIDE.md",
                }
            }
        ),
        json.dumps(
            {
                "method": "item/completed",
                "params": {
                    "item": {
                        "type": "commandExecution",
                        "command": "/bin/bash -lc tools/view.sh AGENTS.md",
                    }
                },
            }
        ),
        json.dumps(
            {
                "method": "codex/event/exec_command_begin",
                "params": {
                    "msg": {
                        "command": ["/bin/bash", "-lc", "tools/view.sh docs/WORKFLOW.md"],
                    }
                },
            }
        ),
    ]
    events.write_text("\n".join(lines) + "\n", encoding="utf-8")

    commands = ct.extract_command_evidence(events)
    assert len(commands) == 3
    assert "tools/view.sh docs/PROJECT_GUIDE.md" in commands[0]
    assert "tools/view.sh AGENTS.md" in commands[1]
    assert "tools/view.sh docs/WORKFLOW.md" in commands[2]


def test_run_plan_sync_app_server_only(monkeypatch, tmp_path: Path) -> None:
    prompt = tmp_path / "prompt.txt"
    raw = tmp_path / "raw.txt"
    events = tmp_path / "events.jsonl"
    stderr = tmp_path / "stderr.log"
    prompt.write_text("{}", encoding="utf-8")

    def fake_primary(*args, **kwargs):  # type: ignore[no-untyped-def]
        raw.write_text('{"mainline":"ok"}\n', encoding="utf-8")
        events.write_text("primary-events\n", encoding="utf-8")
        stderr.write_text("primary-stderr\n", encoding="utf-8")
        return 0

    monkeypatch.setattr(ct, "run_app_server_transport", fake_primary)

    req = ct.TransportRequest(
        model_name="gpt-5.4",
        model_reasoning_effort="xhigh",
        cwd=tmp_path,
    )
    artifacts = ct.TransportArtifacts(
        prompt_file=prompt,
        raw_file=raw,
        events_file=events,
        stderr_file=stderr,
    )
    result = ct.run_plan_sync(req, artifacts)

    assert result.success is True
    assert result.effective_transport == ct.MODEL_TRANSPORT_PRIMARY
    assert result.primary_rc == 0
    assert result.final_rc == 0
