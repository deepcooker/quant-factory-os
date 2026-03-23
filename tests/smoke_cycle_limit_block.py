from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tests" / "fakes"))

from tools.main import MAX_REPAIR_CYCLES, Orchestrator  # noqa: E402
from fake_app import FakeAppServerClient, prepare_smoke_root  # noqa: E402


def read_events(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    root = prepare_smoke_root(REPO_ROOT, "smoke_cycle_limit")
    fake = FakeAppServerClient(scenario="repair_cycle_limit_block")
    orchestrator = Orchestrator(root=root, client=fake)
    try:
        job_id = orchestrator.run_job("验证 repair cycle limit -> discussion -> block")
        job = orchestrator.state.jobs[job_id]

        assert job.status == "DEFECT_BLOCKED"
        assert job.repair_cycle_count == MAX_REPAIR_CYCLES

        events = read_events(root / "state" / "events.jsonl")
        event_names = [event["stage"] for event in events]
        assert "dev_repair_loop" in event_names
        assert "discussion_round" in event_names
        assert "merge" not in event_names

        print("SMOKE_CYCLE_LIMIT_BLOCK_OK")
    finally:
        orchestrator.client.stop()


if __name__ == "__main__":
    main()
