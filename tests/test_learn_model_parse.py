from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.learn import parse_model_output



def _base_model_payload(required_files: list[str]) -> dict:
    return {
        "mainline": "mainline",
        "current_stage": "stage",
        "next_step": "next",
        "files_read": required_files,
        "plan_protocol": {
            "goal": "goal",
            "non_goal": "non-goal",
            "evidence": [f"docs/PROJECT_GUIDE.md#S: fact", f"AGENTS.md#S: fact", f"docs/WORKFLOW.md#S: fact"],
            "alternatives": ["a", "b"],
            "rebuttal": "r",
            "decision_stop_condition": "stop",
        },
        "oral_restate": {
            "project_understanding": "p",
            "constitution_workflow": "c",
            "evidence_chain": "e",
            "session_continuity": "s",
            "current_focus": "f",
            "next_action": "n",
        },
        "guide_oral": [
            {
                "question_id": "Q1",
                "question": "Question one",
                "answer": "Answer one",
                "standard_alignment": "aligned",
                "evidence": [f"docs/PROJECT_GUIDE.md#Q1: fact", f"AGENTS.md#Q1: fact"],
                "drift_note": "none",
                "return_to_mainline": "keep focus",
            },
            {
                "question_id": "Q2",
                "question": "Question two",
                "answer": "Answer two",
                "standard_alignment": "partial",
                "evidence": [f"docs/WORKFLOW.md#Q2: fact"],
                "drift_note": "detail gap",
                "return_to_mainline": "return to workflow gate order",
            },
        ],
        "anchor_realign": {
            "question_id": "Q2",
            "status": "on_track",
            "drift_detail": "none",
            "return_to_mainline": "keep focus",
        },
    }



def _learn_context(required_files: list[str]) -> dict:
    return {
        "context_files": required_files,
        "owner_files": ["docs/PROJECT_GUIDE.md", "AGENTS.md", "docs/WORKFLOW.md"],
        "guide_questions": [
            {"question_id": "Q1", "title": "Question one", "must_read_files": ["docs/PROJECT_GUIDE.md", "AGENTS.md"]},
            {"question_id": "Q2", "title": "Question two", "must_read_files": ["docs/WORKFLOW.md"]},
        ],
    }



def _write_event_commands(events_file: Path, required_files: list[str]) -> None:
    lines = []
    for path in required_files:
        lines.append(
            json.dumps(
                {
                    "item": {
                        "type": "command_execution",
                        "raw_input": f"/bin/bash -lc tools/view.sh {path}",
                    }
                }
            )
        )
    events_file.write_text("\n".join(lines) + "\n", encoding="utf-8")



def test_parse_model_output_accepts_mixed_text_with_json(tmp_path: Path) -> None:
    required = ["docs/PROJECT_GUIDE.md", "AGENTS.md", "docs/WORKFLOW.md"]
    learn_file = tmp_path / "learn.json"
    raw_file = tmp_path / "model.raw.txt"
    model_json = tmp_path / "model.json"
    events_file = tmp_path / "events.jsonl"

    learn_file.write_text(json.dumps(_learn_context(required), ensure_ascii=False), encoding="utf-8")
    payload = _base_model_payload(required)
    raw_file.write_text("note before json\n" + json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    _write_event_commands(events_file, required)

    obj = parse_model_output(raw_file, model_json, "strong", learn_file, events_file)
    assert obj["mainline"] == "mainline"
    assert obj["practice"]["command_execution_count"] == 3
    assert model_json.is_file()



def test_parse_model_output_rejects_missing_question_evidence(tmp_path: Path) -> None:
    required = ["docs/PROJECT_GUIDE.md", "AGENTS.md", "docs/WORKFLOW.md"]
    learn_file = tmp_path / "learn.json"
    raw_file = tmp_path / "model.raw.txt"
    model_json = tmp_path / "model.json"
    events_file = tmp_path / "events.jsonl"

    learn_file.write_text(json.dumps(_learn_context(required), ensure_ascii=False), encoding="utf-8")
    payload = _base_model_payload(required)
    payload["guide_oral"][0]["evidence"] = ["docs/PROJECT_GUIDE.md#Q1: fact"]
    raw_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    _write_event_commands(events_file, required)

    with pytest.raises(ValueError, match="guide_oral evidence missing required files"):
        parse_model_output(raw_file, model_json, "strong", learn_file, events_file)



def test_parse_model_output_rejects_question_order_mismatch(tmp_path: Path) -> None:
    required = ["docs/PROJECT_GUIDE.md", "AGENTS.md", "docs/WORKFLOW.md"]
    learn_file = tmp_path / "learn.json"
    raw_file = tmp_path / "model.raw.txt"
    model_json = tmp_path / "model.json"
    events_file = tmp_path / "events.jsonl"

    learn_file.write_text(json.dumps(_learn_context(required), ensure_ascii=False), encoding="utf-8")
    payload = _base_model_payload(required)
    payload["guide_oral"] = list(reversed(payload["guide_oral"]))
    raw_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    _write_event_commands(events_file, required)

    with pytest.raises(ValueError, match="guide_oral order mismatch"):
        parse_model_output(raw_file, model_json, "strong", learn_file, events_file)


def test_parse_model_output_falls_back_to_events_when_raw_missing(tmp_path: Path) -> None:
    required = ["docs/PROJECT_GUIDE.md", "AGENTS.md", "docs/WORKFLOW.md"]
    learn_file = tmp_path / "learn.json"
    raw_file = tmp_path / "model.raw.txt"
    model_json = tmp_path / "model.json"
    events_file = tmp_path / "events.jsonl"

    learn_file.write_text(json.dumps(_learn_context(required), ensure_ascii=False), encoding="utf-8")
    payload = _base_model_payload(required)
    raw_file.write_text("", encoding="utf-8")
    event_lines = [
        json.dumps(
            {
                "method": "codex/event/item_started",
                "params": {
                    "msg": {
                        "item": {
                            "type": "AgentMessage",
                            "id": "msg-final",
                            "phase": "final_answer",
                        }
                    }
                },
            }
        )
    ]
    text = json.dumps(payload, ensure_ascii=False)
    split_at = text.find('"guide_oral"')
    event_lines.append(
        json.dumps(
            {
                "method": "codex/event/agent_message_content_delta",
                "params": {"msg": {"item_id": "msg-final", "delta": text[:split_at]}},
            }
        )
    )
    event_lines.append(
        json.dumps(
            {
                "method": "codex/event/agent_message_content_delta",
                "params": {"msg": {"item_id": "msg-final", "delta": text[split_at:]}},
            }
        )
    )
    for path in required:
        event_lines.append(
            json.dumps(
                {
                    "item": {
                        "type": "command_execution",
                        "raw_input": f"/bin/bash -lc tools/view.sh {path}",
                    }
                }
            )
        )
    events_file.write_text("\n".join(event_lines) + "\n", encoding="utf-8")

    obj = parse_model_output(raw_file, model_json, "strong", learn_file, events_file)
    assert obj["mainline"] == "mainline"
    assert model_json.is_file()
