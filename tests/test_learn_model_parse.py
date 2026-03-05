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
            "evidence": [f"{required_files[0]}#S: fact", f"{required_files[1]}#S: fact"],
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
        "oral_exam": [
            {"question_id": "Q1", "question": "q1", "answer": "a1", "score": "pass"},
            {"question_id": "Q2", "question": "q2", "answer": "a2", "score": "pass"},
            {"question_id": "Q3", "question": "q3", "answer": "a3", "score": "fail"},
        ],
        "anchor_realign": {
            "question_id": "Q1",
            "status": "on_track",
            "drift_detail": "none",
            "return_to_mainline": "keep focus",
        },
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
    required = ["docs/PROJECT_GUIDE.md", "AGENTS.md"]
    learn_file = tmp_path / "learn.json"
    raw_file = tmp_path / "model.raw.txt"
    model_json = tmp_path / "model.json"
    events_file = tmp_path / "events.jsonl"

    learn_file.write_text(json.dumps({"context_files": required}, ensure_ascii=False), encoding="utf-8")
    payload = _base_model_payload(required)
    raw_file.write_text("note before json\n" + json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    _write_event_commands(events_file, required)

    obj = parse_model_output(raw_file, model_json, "strong", learn_file, events_file)
    assert obj["mainline"] == "mainline"
    assert obj["practice"]["command_execution_count"] == 2
    assert model_json.is_file()


def test_parse_model_output_rejects_insufficient_exam_passes(tmp_path: Path) -> None:
    required = ["docs/PROJECT_GUIDE.md", "AGENTS.md"]
    learn_file = tmp_path / "learn.json"
    raw_file = tmp_path / "model.raw.txt"
    model_json = tmp_path / "model.json"
    events_file = tmp_path / "events.jsonl"

    learn_file.write_text(json.dumps({"context_files": required}, ensure_ascii=False), encoding="utf-8")
    payload = _base_model_payload(required)
    payload["oral_exam"] = [
        {"question_id": "Q1", "question": "q1", "answer": "a1", "score": "pass"},
        {"question_id": "Q2", "question": "q2", "answer": "a2", "score": "fail"},
        {"question_id": "Q3", "question": "q3", "answer": "a3", "score": "fail"},
    ]
    raw_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    _write_event_commands(events_file, required)

    with pytest.raises(ValueError, match="oral_exam insufficient passes"):
        parse_model_output(raw_file, model_json, "strong", learn_file, events_file)
