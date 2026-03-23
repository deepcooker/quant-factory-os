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
    root = prepare_smoke_root(REPO_ROOT, "smoke_discussion_block")
    fake = FakeAppServerClient(scenario="critical_discussion_block")
    orchestrator = Orchestrator(root=root, client=fake)
    try:
        job_id = orchestrator.run_job("验证 critical defect -> discussion -> block_job")
        job = orchestrator.state.jobs[job_id]

        assert job.status == "DEFECT_BLOCKED"
        assert job.discussion_cycle_count >= 1

        events = read_events(root / "state" / "events.jsonl")
        event_names = [event["stage"] for event in events]
        assert "discussion_round" in event_names
        assert "merge" not in event_names
        assert "baseline_refresh" not in event_names

        print("SMOKE_CRITICAL_DISCUSSION_BLOCK_OK")
    finally:
        orchestrator.client.stop()


if __name__ == "__main__":
    main()
