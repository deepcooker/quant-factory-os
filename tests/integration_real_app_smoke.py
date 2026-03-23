from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.app import AppServerClient, SkillRef  # noqa: E402


def main() -> None:
    if os.environ.get("RUN_REAL_APP_SERVER") != "1":
        print("SKIPPED: set RUN_REAL_APP_SERVER=1 to run real app-server smoke")
        return

    client = AppServerClient(cwd=str(REPO_ROOT))
    client.start()
    try:
        thread_id = client.create_thread(title="real-app-smoke", cwd=str(REPO_ROOT))
        skill = SkillRef(
            name="contract-echo",
            path=str(REPO_ROOT / "tests" / "fixtures" / "skills" / "contract-echo" / "SKILL.md"),
        )
        result = client.start_turn(
            thread_id=thread_id,
            text="Use $contract-echo to return the minimal JSON fenced block only.",
            skill=skill,
            metadata={"phase": "integration_real_app_smoke"},
        )
        assert result["thread_id"] == thread_id
        assert result["turn_id"]
        assert result["final_text"]
        assert isinstance(result["payload"], dict)
        assert result["payload"]["ok"] is True
        assert result["payload"]["kind"] == "contract_echo"
        print("INTEGRATION_REAL_APP_SMOKE_OK")
    finally:
        client.stop()


if __name__ == "__main__":
    main()
