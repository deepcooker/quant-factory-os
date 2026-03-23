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
    root = prepare_smoke_root(REPO_ROOT, "smoke_replan")
    fake = FakeAppServerClient(scenario="major_defect_replan")
    orchestrator = Orchestrator(root=root, client=fake)
    try:
        job_id = orchestrator.run_job("验证 major defect -> replan -> task 级精准重跑")
        job = orchestrator.state.jobs[job_id]

        assert job.status == "DONE"
        assert job.replan_cycle_count >= 1
        assert fake.role_call_counts.get("task_test_hotspot:test") == 2
        assert fake.role_call_counts.get("task_test_control:test") == 1

        active_results = orchestrator.collect_active_child_results(job_id)
        task_ids = sorted(result["task_id"] for result in active_results if result.get("role") == "test")
        assert task_ids == ["task_test_control", "task_test_hotspot"]

        events = read_events(root / "state" / "events.jsonl")
        event_names = [event["stage"] for event in events]
        assert "run_replan" in event_names
        assert "merge" in event_names
        assert "baseline_refresh" in event_names

        print("SMOKE_MAJOR_DEFECT_REPLAN_OK")
    finally:
        orchestrator.client.stop()


if __name__ == "__main__":
    main()
