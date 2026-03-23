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
    root = prepare_smoke_root(REPO_ROOT, "smoke_happy")
    fake = FakeAppServerClient(scenario="happy_path")
    orchestrator = Orchestrator(root=root, client=fake)
    try:
        job_id = orchestrator.run_job("验证 happy path 是否可以一路到 DONE")
        job = orchestrator.state.jobs[job_id]

        assert job.status == "DONE"
        assert orchestrator.state.baseline_snapshot["baseline_version"] == 2

        events = read_events(root / "state" / "events.jsonl")
        event_names = [event["stage"] for event in events]
        assert "create_job" in event_names
        assert "merge" in event_names
        assert "baseline_refresh" in event_names

        checkpoint_dir = root / "state" / "checkpoints" / f"job_{job_id}"
        assert (checkpoint_dir / "01_coach_v1.json").exists()
        assert (checkpoint_dir / "05_planning.json").exists()
        assert (checkpoint_dir / "07_merge.json").exists()
        assert (checkpoint_dir / "08_baseline_refresh.json").exists()

        print("SMOKE_HAPPY_PATH_OK")
    finally:
        orchestrator.client.stop()


if __name__ == "__main__":
    main()
