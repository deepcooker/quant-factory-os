from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tests" / "fakes"))

from tools.main import Orchestrator  # noqa: E402
from fake_app import FakeAppServerClient, prepare_smoke_root  # noqa: E402


def main() -> None:
    root = prepare_smoke_root(REPO_ROOT, "smoke_resume_merged")
    fake = FakeAppServerClient(scenario="happy_path")
    orchestrator = Orchestrator(root=root, client=fake)
    try:
        orchestrator.state.baseline_snapshot = fake._baseline_snapshot(version=1)
        job_id = orchestrator.create_job("验证 MERGED -> refresh resume")
        job = orchestrator.state.jobs[job_id]
        job.clarified_job_v1 = fake._clarified_job("resume merged", True, job_id=job_id)
        job.evidence_packs = []
        job.clarified_job_v2 = fake._clarified_job("resume merged", True, job_id=job_id)
        job.corrected_job = {
            "job_id": job_id,
            "status": "approved",
            "corrected_goal": "resume merged",
            "chosen_approach": "minimal-smoke",
            "reasons": ["seeded for resume"],
            "open_questions": [],
            "risks": [],
            "ready_for_task_planning": True,
        }
        job.task_plan = fake._task_plan(job_id)
        job.final_summary = fake._merge_result(job_id)
        job.status = "MERGED"
        orchestrator._save_state()

        before_calls = len(fake.calls)
        orchestrator.resume_job(job_id)
        after_calls = fake.calls[before_calls:]
        phases = [call["phase"] for call in after_calls]

        assert phases == ["refresh_learning_baseline"]
        assert orchestrator.state.jobs[job_id].status == "DONE"
        assert orchestrator.state.baseline_snapshot["baseline_version"] == 2

        print("SMOKE_RESUME_AFTER_MERGED_OK")
    finally:
        orchestrator.client.stop()


if __name__ == "__main__":
    main()
