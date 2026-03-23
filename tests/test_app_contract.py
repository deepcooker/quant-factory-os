from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.app import AppServerClient, SkillRef  # noqa: E402


class StubAppServerClient(AppServerClient):
    def __init__(self):
        super().__init__(codex_bin="codex", cwd=str(REPO_ROOT))

    def _request(self, method: str, params):
        if method == "turn/start":
            return {"turnId": "turn_stub_1"}
        raise RuntimeError(f"unexpected method: {method}")

    def _collect_turn_result(self, thread_id: str, turn_id: str):
        return {
            "thread_id": thread_id,
            "turn_id": turn_id,
            "final_text": "```json\n{\"ok\": true}\n```",
            "payload": {"ok": True},
        }


def main() -> None:
    client = AppServerClient(codex_bin="codex", cwd=str(REPO_ROOT))

    fenced = "before\n```json\n{\"a\": 1}\n```\nafter"
    assert client._extract_json_from_text(fenced) == {"a": 1}
    assert client._extract_json_from_text('{"b": 2}') == {"b": 2}
    assert client._extract_payload_from_item({"text": "```json\n{\"c\": 3}\n```"}) == {"c": 3}

    stub = StubAppServerClient()
    result = stub.start_turn(
        thread_id="thread_1",
        text="contract test",
        skill=SkillRef(name="dummy-skill", path=str(REPO_ROOT / ".agents/skills/project-coach/SKILL.md")),
        metadata={"phase": "contract_test"},
    )

    assert result["thread_id"] == "thread_1"
    assert result["turn_id"] == "turn_stub_1"
    assert result["final_text"]
    assert result["payload"] == {"ok": True}

    print("TEST_APP_CONTRACT_OK")


if __name__ == "__main__":
    main()
