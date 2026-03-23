from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tests" / "fakes"))

from tools.main import Orchestrator  # noqa: E402
from fake_app import FakeAppServerClient, prepare_smoke_root  # noqa: E402


def read_events(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    root = prepare_smoke_root(REPO_ROOT, "smoke_send_back_to_dev")
    fake = FakeAppServerClient(scenario="send_back_to_dev")
    orchestrator = Orchestrator(root=root, client=fake)
    try:
        job_id = orchestrator.run_job("验证 send_back_to_dev -> repair loop -> merge")
        job = orchestrator.state.jobs[job_id]

        assert job.status == "DONE"
        assert job.repair_cycle_count >= 1

        phases = [call["phase"] for call in fake.calls]
        assert "dev_repair" in phases
        assert "test_recheck" in phases

        events = read_events(root / "state" / "events.jsonl")
        event_names = [event["stage"] for event in events]
        assert "dev_repair_loop" in event_names
        assert "merge" in event_names
        assert "baseline_refresh" in event_names

        print("SMOKE_SEND_BACK_TO_DEV_REPAIR_OK")
    finally:
        orchestrator.client.stop()


if __name__ == "__main__":
    main()
