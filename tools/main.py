
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.app import AppServerClient, SkillRef
from core.schema_utils import validate_with_schema, SchemaValidationError

SCHEMA_DIR = REPO_ROOT / "schemas"
SCHEMAS = {
    "clarified_job": SCHEMA_DIR / "clarified_job.schema.json",
    "claim": SCHEMA_DIR / "claim.schema.json",
    "evidence_pack": SCHEMA_DIR / "evidence_pack.schema.json",
    "corrected_job": SCHEMA_DIR / "corrected_job.schema.json",
    "demand_critic_result": SCHEMA_DIR / "demand_critic_result.schema.json",
    "solution_designer_result": SCHEMA_DIR / "solution_designer_result.schema.json",
    "risk_reviewer_result": SCHEMA_DIR / "risk_reviewer_result.schema.json",
    "baseline_snapshot": SCHEMA_DIR / "learning_baseline_snapshot.schema.json",
    "task_plan": SCHEMA_DIR / "task_plan.schema.json",
    "merge_result": SCHEMA_DIR / "merge_result.schema.json",
    "defect_triage_result": SCHEMA_DIR / "defect_triage_result.schema.json",
    "replan_decision": SCHEMA_DIR / "replan_decision.schema.json",
    "discussion_resolution": SCHEMA_DIR / "discussion_resolution.schema.json",
    "dev_worker_result": SCHEMA_DIR / "dev_worker_result.schema.json",
    "test_worker_result": SCHEMA_DIR / "test_worker_result.schema.json",
    "arch_reviewer_result": SCHEMA_DIR / "arch_reviewer_result.schema.json",
}

MAX_REPAIR_CYCLES = 2
MAX_REPLAN_CYCLES = 2
MAX_DISCUSSION_CYCLES = 2


# =========================
# Data models
# =========================


@dataclass
class Claim:
    claim_id: str
    claim: str
    type: str
    confidence: float = 0.0
    evidence_level: str = "unknown"  # documented | code_verified | runtime_verified | inferred | unknown
    verification_required: bool = True
    status: str = "pending"          # pending | confirmed | rejected
    doc_support: List[str] = field(default_factory=list)
    code_support: List[str] = field(default_factory=list)
    runtime_support: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)


@dataclass
class ThreadRecord:
    thread_id: str
    role: str
    status: str
    parent_thread_id: Optional[str] = None
    job_id: Optional[str] = None
    task_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


@dataclass
class Job:
    job_id: str
    raw_request: str
    source: str = "manual"
    clarified_job_v1: Optional[Dict[str, Any]] = None
    evidence_packs: Optional[List[Dict[str, Any]]] = None
    clarified_job_v2: Optional[Dict[str, Any]] = None
    corrected_job: Optional[Dict[str, Any]] = None
    task_plan: Optional[Dict[str, Any]] = None
    defect_triage: Optional[Dict[str, Any]] = None
    final_summary: Optional[Dict[str, Any]] = None
    defect_status: str = "none"
    repair_cycle_count: int = 0
    replan_cycle_count: int = 0
    discussion_cycle_count: int = 0
    discussion_required: bool = False
    status: str = "NEW"  # NEW -> COACHED -> VERIFIED -> CORRECTED -> PLANNED -> EXECUTING -> MERGED -> DONE


@dataclass
class RegistryState:
    learning_baseline_thread_id: Optional[str] = None
    run_baseline_thread_id: Optional[str] = None
    threads: Dict[str, ThreadRecord] = field(default_factory=dict)
    jobs: Dict[str, Job] = field(default_factory=dict)
    claims: Dict[str, Claim] = field(default_factory=dict)
    baseline_snapshot: Dict[str, Any] = field(default_factory=lambda: {
        "core_truths": [],
        "candidate_truths": [],
        "open_questions": []
    })


# =========================
# Utilities
# =========================

def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def now_ms() -> int:
    return int(time.time() * 1000)


def gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


# =========================
# Orchestrator
# =========================

class Orchestrator:
    def __init__(self, root: Path, client: Optional[Any] = None):
        self.root = root
        self.config_path = root / "tools" / "project_config.json"
        self.state_dir = root / "state"
        self.registry_path = self.state_dir / "registry.json"
        self.events_path = self.state_dir / "events.jsonl"
        self.checkpoints_root = self.state_dir / "checkpoints"

        self.config = load_json(self.config_path, {})
        self.state = self._load_state()
        self.client = client or AppServerClient(cwd=str(self.root))
        if client is None:
            self.client.start()
        self.skill_registry = self._load_skill_registry()

    def _load_state(self) -> RegistryState:
        raw = load_json(self.registry_path, {})
        if not raw:
            return RegistryState()

        state = RegistryState(
            learning_baseline_thread_id=raw.get("learning_baseline_thread_id"),
            run_baseline_thread_id=raw.get("run_baseline_thread_id"),
            baseline_snapshot=raw.get("baseline_snapshot", {
                "core_truths": [],
                "candidate_truths": [],
                "open_questions": []
            }),
        )

        for tid, tr in raw.get("threads", {}).items():
            state.threads[tid] = ThreadRecord(**tr)

        for jid, job in raw.get("jobs", {}).items():
            state.jobs[jid] = Job(**job)

        for cid, claim in raw.get("claims", {}).items():
            state.claims[cid] = Claim(**claim)

        return state

    def _save_state(self) -> None:
        raw = {
            "learning_baseline_thread_id": self.state.learning_baseline_thread_id,
            "run_baseline_thread_id": self.state.run_baseline_thread_id,
            "threads": {k: asdict(v) for k, v in self.state.threads.items()},
            "jobs": {k: asdict(v) for k, v in self.state.jobs.items()},
            "claims": {k: asdict(v) for k, v in self.state.claims.items()},
            "baseline_snapshot": self.state.baseline_snapshot,
        }
        save_json(self.registry_path, raw)

    def _append_event(
        self,
        job_id: str,
        stage: str,
        status_before: str,
        status_after: str,
        decision: str = "",
        refs: Optional[List[str]] = None,
    ) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        event = {
            "ts": time.time(),
            "job_id": job_id,
            "stage": stage,
            "status_before": status_before,
            "status_after": status_after,
            "decision": decision,
            "refs": refs or [],
        }
        with self.events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _write_checkpoint(self, job_id: str, stage: str, data: Any) -> None:
        checkpoint_dir = self.checkpoints_root / f"job_{job_id}"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        save_json(checkpoint_dir / f"{stage}.json", data)

    def _set_job_status(
        self,
        job_id: str,
        stage: str,
        new_status: str,
        decision: str = "",
        refs: Optional[List[str]] = None,
        checkpoint: Any = None,
    ) -> None:
        job = self.state.jobs[job_id]
        status_before = job.status
        job.status = new_status
        if checkpoint is not None:
            self._write_checkpoint(job_id, stage, checkpoint)
        self._append_event(job_id, stage, status_before, new_status, decision=decision, refs=refs)
        self._save_state()

    def _is_terminal_status(self, status: str) -> bool:
        return status in {
            "DONE",
            "BLOCKED_AFTER_CORRECTION",
            "WAITING_MORE_EVIDENCE",
            "DEFECT_BLOCKED",
        }

    def _load_skill_registry(self) -> Dict[str, SkillRef]:
        skills = self.config.get("skills", {})
        registry: Dict[str, SkillRef] = {}
        for key, path in skills.items():
            registry[key] = SkillRef(name=key.replace("_", "-"), path=str(self.root / path))
        return registry

    def _get_skill(self, key: str) -> SkillRef:
        if key not in self.skill_registry:
            raise KeyError(f"Missing skill: {key}")
        return self.skill_registry[key]

    def validate_environment(self) -> None:
        required_docs = self.config.get("docs", {})
        missing = []
        for _, rel in required_docs.items():
            if isinstance(rel, list):
                for item in rel:
                    if not (self.root / item).exists():
                        missing.append(item)
                continue
            if not (self.root / rel).exists():
                missing.append(rel)
        for _, rel in self.config.get("skills", {}).items():
            if not (self.root / rel).exists():
                missing.append(rel)
        for schema_path in SCHEMAS.values():
            if not (self.root / schema_path).exists():
                missing.append(str(schema_path))
        if missing:
            raise FileNotFoundError(f"Missing required docs: {missing}")
        self.state_dir.mkdir(parents=True, exist_ok=True)
        probe = self.state_dir / ".write_test"
        probe.write_text("", encoding="utf-8")
        probe.unlink()

    # ---------- Thread ensure ----------

    def ensure_learning_thread(self) -> str:
        result = self.client.run_business_turn(
            slot="learning_baseline",
            prompt="",
            force_new=False,
            fork_thread="",
            is_plan=False,
            effort="low",
            skill_name="",
            cwd=str(self.root),
            metadata={"phase": "learning_thread_ensure"},
            rename=True,
        )
        thread_id = result["thread_id"]

        self.state.learning_baseline_thread_id = thread_id
        self.state.threads[thread_id] = ThreadRecord(thread_id=thread_id, role="learning_baseline", status="RUNNING")
        self._save_state()
        return thread_id

    def ensure_run_thread(self) -> str:
        learning_thread_id = self.ensure_learning_thread()
        result = self.client.run_business_turn(
            slot="run_baseline",
            prompt="",
            force_new=False,
            fork_thread="" if self.state.run_baseline_thread_id else learning_thread_id,
            is_plan=False,
            effort="low",
            skill_name="",
            cwd=str(self.root),
            metadata={"phase": "run_thread_ensure"},
            rename=True,
            parent_slot="learning_baseline",
        )
        thread_id = result["thread_id"]

        self.state.run_baseline_thread_id = thread_id
        self.state.threads[thread_id] = ThreadRecord(
            thread_id=thread_id,
            role="run_baseline",
            status="RUNNING",
            parent_thread_id=learning_thread_id
        )
        self._save_state()
        return thread_id

    # ---------- Learning baseline ----------

    def initialize_or_refresh_learning_baseline(self) -> Dict[str, Any]:
        skill = self._get_skill("learn_baseline")
        prompt = (
            "$learn-baseline 初始化或刷新项目学习基线。\n"
            "读取 PROJECT_GUIDE、WORKFLOW、AGENTS 以及已有 baseline snapshot。\n"
            "只提取长期有效项目真相，输出结构化 baseline JSON。"
        )
        result = self.client.run_business_turn(
            slot="learning_baseline",
            prompt=prompt,
            force_new=False,
            fork_thread="",
            is_plan=False,
            effort="low",
            skill_name=skill.name,
            cwd=str(self.root),
            metadata={"phase": "learning_baseline_init"},
            rename=True,
        )
        thread_id = result["thread_id"]
        baseline_snapshot = result["payload"]
        validate_with_schema(baseline_snapshot, SCHEMAS["baseline_snapshot"])
        self.state.baseline_snapshot = baseline_snapshot
        self.state.learning_baseline_thread_id = thread_id
        self._save_state()
        return result

    # ---------- Jobs ----------

    def create_job(self, raw_request: str, source: str = "manual") -> str:
        job_id = gen_id("job")
        job = Job(job_id=job_id, raw_request=raw_request, source=source)
        self.state.jobs[job_id] = job
        self._write_checkpoint(job_id, "00_created", asdict(job))
        self._append_event(job_id, "create_job", "", "NEW", decision="create_job", refs=[])
        self._save_state()
        return job_id

    def resume_job(self, job_id: str) -> str:
        self.validate_environment()
        self.ensure_learning_thread()
        if not self.state.baseline_snapshot.get("core_truths") and not self.state.baseline_snapshot.get("candidate_truths"):
            self.initialize_or_refresh_learning_baseline()
        self.ensure_run_thread()

        if job_id not in self.state.jobs:
            raise KeyError(f"Unknown job_id: {job_id}")

        job = self.state.jobs[job_id]
        if self._is_terminal_status(job.status):
            self._append_event(job_id, "resume_job", job.status, job.status, decision="already_terminal", refs=[])
            self._save_state()
            return job_id
        if job.defect_status == "DEFECT_BLOCKED":
            self._append_event(job_id, "resume_job", job.status, job.status, decision="defect_blocked", refs=[])
            self._save_state()
            return job_id

        if job.clarified_job_v1 is None:
            result = self.coach_round_v1(job_id)
            self._set_job_status(job_id, "01_coach_v1", "COACHED", checkpoint=result)
            job = self.state.jobs[job_id]

        if job.evidence_packs is None:
            verify_result = self.verification_round(job_id)
            self._set_job_status(job_id, "02_verification", "VERIFIED", checkpoint=verify_result)
            job = self.state.jobs[job_id]

        if job.clarified_job_v2 is None:
            result = self.coach_round_v2(job_id)
            self._set_job_status(job_id, "03_coach_v2", "COACHED_V2", checkpoint=result)
            job = self.state.jobs[job_id]

        if job.corrected_job is None:
            result = self.correction_round(job_id)
            self._set_job_status(job_id, "04_correction", "CORRECTED", checkpoint=result)
            job = self.state.jobs[job_id]

        corrected_job = job.corrected_job or {}
        if corrected_job.get("status") == "blocked":
            self._set_job_status(job_id, "04_correction_gate", "BLOCKED_AFTER_CORRECTION", decision="corrected_job_blocked")
            return job_id
        if not corrected_job.get("ready_for_task_planning", False):
            self._set_job_status(job_id, "04_correction_gate", "WAITING_MORE_EVIDENCE", decision="not_ready_for_task_planning")
            return job_id

        if job.task_plan is None:
            result = self.planning_round(job_id)
            self._set_job_status(job_id, "05_planning", "PLANNED", checkpoint=result)
            job = self.state.jobs[job_id]

        if job.final_summary is None and job.status == "PLANNED":
            child_ids = self.spawn_role_threads(job_id)
            self._append_event(job_id, "06_spawn_role_threads", job.status, "EXECUTING", decision="spawn_role_threads", refs=child_ids)
            job.status = "EXECUTING"
            self._save_state()

        if job.final_summary is None and job.status == "EXECUTING":
            child_results = self.collect_active_child_results(job_id)
            triage_result = self.defect_triage_round(job_id, child_results)
            self._write_checkpoint(job_id, "06_defect_triage", triage_result)
            ready_child_results = self._consume_triage_route(job_id, triage_result, child_results)
            if ready_child_results is None:
                self._append_event(job_id, "06_defect_flow", self.state.jobs[job_id].status, self.state.jobs[job_id].status, decision="flow_paused_or_blocked", refs=[])
                self._save_state()
                return job_id
            merge_result = self.merge_in_run_baseline(job_id, ready_child_results)
            self._set_job_status(job_id, "07_merge", "MERGED", checkpoint=merge_result)
            job = self.state.jobs[job_id]

        if job.status == "MERGED":
            baseline_result = self.refresh_learning_baseline(job_id)
            self._set_job_status(job_id, "08_baseline_refresh", "DONE", checkpoint=baseline_result)

        return job_id

    def resume_latest_incomplete_job(self) -> Optional[str]:
        for job_id in reversed(list(self.state.jobs.keys())):
            job = self.state.jobs[job_id]
            if not self._is_terminal_status(job.status) and job.defect_status != "DEFECT_BLOCKED":
                return self.resume_job(job_id)
        return None

    def coach_round_v1(self, job_id: str) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        skill = self._get_skill("project_coach")
        result = run_with_validation(
            "coach_v1",
            lambda: run_project_coach_v1(
                client=self.client,
                run_thread_id=run_thread,
                skill=skill,
                raw_request=job.raw_request,
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
            ),
            "clarified_job",
        )

        job.clarified_job_v1 = result
        job.status = "COACHED"
        self._save_state()
        return result

    def verification_round(self, job_id: str) -> Dict[str, Any]:
        """
        For each claim:
        - doc-evidence-worker
        - code-evidence-worker
        - runtime-evidence-worker
        - contradiction-checker
        """
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()

        claims = job.clarified_job_v1.get("claims", []) if job.clarified_job_v1 else []
        evidence_results = []

        for claim_ref in claims:
            claim_id = claim_ref["claim_id"]
            claim_text = claim_ref["claim"]
            claim = Claim(
                claim_id=claim_id,
                claim=claim_text,
                type="general",
                confidence=0.5,
                evidence_level="inferred",
                verification_required=True,
                status="pending"
            )
            self.state.claims[claim_id] = claim

            evidence_pack = run_with_validation(
                f"verify_claim_{claim_id}",
                lambda claim_ref=claim_ref: run_verification_for_claim(
                    client=self.client,
                    run_thread_id=run_thread,
                    claim=claim_ref,
                    skill_registry=self.skill_registry,
                    schema_map=SCHEMAS,
                    validate_with_schema=validate_with_schema,
                ),
                "evidence_pack",
            )
            evidence_results.append(evidence_pack)

            final_status = evidence_pack.get("final_status")
            if final_status in ("confirmed", "partially_confirmed"):
                claim.status = "confirmed"
            elif final_status == "rejected":
                claim.status = "rejected"
            else:
                claim.status = "pending"
            claim.doc_support = evidence_pack.get("doc_evidence", {}).get("support_refs", [])
            claim.code_support = evidence_pack.get("code_evidence", {}).get("support_refs", [])
            claim.runtime_support = evidence_pack.get("runtime_evidence", {}).get("support_refs", [])
            claim.contradictions = evidence_pack.get("contradiction_check", {}).get("conflict_points", [])

        job.evidence_packs = evidence_results

        job.status = "VERIFIED"
        self._save_state()
        return {"status": "ok", "evidence_results": evidence_results}

    def coach_round_v2(self, job_id: str) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        skill = self._get_skill("project_coach")
        result = run_with_validation(
            "coach_v2",
            lambda: run_project_coach_v2(
                client=self.client,
                run_thread_id=run_thread,
                skill=skill,
                clarified_job_v1=job.clarified_job_v1,
                evidence_packs=job.evidence_packs or [],
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
            ),
            "clarified_job",
        )
        job.clarified_job_v2 = result
        self._save_state()
        return result

    def correction_round(self, job_id: str) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        corrected_job = run_with_validation(
            "correction_round",
            lambda: run_correction_round(
                client=self.client,
                run_thread_id=run_thread,
                clarified_job_v2=job.clarified_job_v2,
                skill_registry=self.skill_registry,
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
                job_id=job_id,
                raw_request=job.raw_request,
            ),
            "corrected_job",
        )
        job.corrected_job = corrected_job
        job.status = "CORRECTED"
        self._save_state()
        return corrected_job

    def planning_round(self, job_id: str) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        skill = self._get_skill("run_manager")
        result = run_with_validation(
            "task_planning",
            lambda: run_task_planning(
                client=self.client,
                run_thread_id=run_thread,
                skill=skill,
                corrected_job=job.corrected_job,
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
            ),
            "task_plan",
        )
        job.task_plan = result
        job.status = "PLANNED"
        self._save_state()
        return result

    # ---------- Child threads ----------

    def _role_to_skill_key(self, role: str) -> str:
        mapping = {
            "dev": "dev_worker",
            "test": "test_worker",
            "arch_review": "arch_reviewer",
        }
        return mapping[role]

    def spawn_role_threads(self, job_id: str) -> List[str]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        task_plan = job.task_plan or {}
        child_ids: List[str] = []

        for task in task_plan.get("tasks", []):
            if not task.get("needs_thread", False):
                continue
            skill_key = self._role_to_skill_key(task["role"])
            skill = self._get_skill(skill_key)

            response = fork_and_run_client_turn(
                client=self.client,
                slot=f"{task['role']}_{task['task_id']}",
                parent_thread_id=run_thread,
                title=f"{task['role']}-{task['task_id']}",
                prompt=(
                    f"${skill.name} 请执行以下 task。\n"
                    f"task_id: {task['task_id']}\n"
                    f"role: {task['role']}\n"
                    f"goal: {task['goal']}\n"
                    "输出结构化 worker result。"
                ),
                skill=skill,
                metadata={
                    "phase": "role_execution",
                    "job_id": job_id,
                    "task_id": task["task_id"],
                    "role": task["role"],
                },
                cwd=str(self.root),
            )
            child_thread_id = response["thread_id"]

            self.state.threads[child_thread_id] = ThreadRecord(
                thread_id=child_thread_id,
                role=task["role"],
                status="RUNNING",
                parent_thread_id=run_thread,
                job_id=job_id,
                task_id=task["task_id"],
            )
            validate_role_result(response["payload"])
            self.state.threads[child_thread_id].result = response["payload"]
            self.state.threads[child_thread_id].status = "DONE"
            self.state.threads[child_thread_id].updated_at = time.time()

            child_ids.append(child_thread_id)

        job.status = "EXECUTING"
        self._save_state()
        return child_ids

    def spawn_selected_tasks(self, job_id: str, selected_tasks: List[Dict[str, Any]]) -> List[str]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        child_ids: List[str] = []

        for task in selected_tasks:
            if not task.get("needs_thread", False):
                continue
            skill_key = self._role_to_skill_key(task["role"])
            skill = self._get_skill(skill_key)

            response = fork_and_run_client_turn(
                client=self.client,
                slot=f"{task['role']}_{task['task_id']}",
                parent_thread_id=run_thread,
                title=f"{task['role']}-{task['task_id']}",
                prompt=(
                    f"${skill.name} 请执行以下 task。\n"
                    f"task_id: {task['task_id']}\n"
                    f"role: {task['role']}\n"
                    f"goal: {task['goal']}\n"
                    "输出结构化 worker result。"
                ),
                skill=skill,
                metadata={
                    "phase": "role_execution",
                    "job_id": job_id,
                    "task_id": task["task_id"],
                    "role": task["role"],
                },
                cwd=str(self.root),
            )
            child_thread_id = response["thread_id"]

            self.state.threads[child_thread_id] = ThreadRecord(
                thread_id=child_thread_id,
                role=task["role"],
                status="RUNNING",
                parent_thread_id=run_thread,
                job_id=job_id,
                task_id=task["task_id"],
            )
            validate_role_result(response["payload"])
            self.state.threads[child_thread_id].result = response["payload"]
            self.state.threads[child_thread_id].status = "DONE"
            self.state.threads[child_thread_id].updated_at = time.time()

            child_ids.append(child_thread_id)

        job.status = "EXECUTING"
        self._save_state()
        return child_ids

    def collect_child_results(self, job_id: str) -> List[Dict[str, Any]]:
        results = []
        for thread_id, record in self.state.threads.items():
            if record.job_id == job_id and record.parent_thread_id == self.state.run_baseline_thread_id:
                if record.result is not None:
                    results.append(record.result)
        self._save_state()
        return results

    def collect_active_child_results(self, job_id: str) -> List[Dict[str, Any]]:
        latest_by_key: Dict[str, tuple[float, Dict[str, Any]]] = {}
        for _, record in self.state.threads.items():
            if record.job_id != job_id or record.parent_thread_id != self.state.run_baseline_thread_id:
                continue
            if record.result is None:
                continue
            task_id = record.task_id or record.result.get("task_id") or "unknown_task"
            role = record.role or record.result.get("role") or "unknown_role"
            key = f"{task_id}:{role}"
            ts = record.updated_at or 0.0
            existing = latest_by_key.get(key)
            if existing is None or ts >= existing[0]:
                latest_by_key[key] = (ts, record.result)
        active_results = [item[1] for item in latest_by_key.values()]
        self._save_state()
        return active_results

    def defect_triage_round(self, job_id: str, child_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        skill = self._get_skill("defect_triage")

        test_results = [
            result
            for result in child_results
            if isinstance(result, dict) and result.get("role") == "test"
        ]

        if not test_results:
            result = {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "done",
                "summary": "当前 job 没有 test 结果，跳过 defect triage，允许继续 merge。",
                "severity_assessment": {
                    "highest_severity": "none",
                    "rationale": "无 test-worker 输出，当前不触发缺陷分流。"
                },
                "scope_assessment": {
                    "scope": "none",
                    "rationale": "未观察到测试侧问题范围。"
                },
                "recommended_route": "proceed_merge",
                "block_merge": False,
                "block_baseline_update": False,
                "participants": ["system"],
                "target_task_ids": [],
                "key_findings": [],
                "next_actions": []
            }
            validate_with_schema(result, SCHEMAS["defect_triage_result"])
            job.defect_triage = result
            job.defect_status = "READY_TO_MERGE"
            self._write_checkpoint(job_id, "06_defect_triage", result)
            self._append_event(job_id, "defect_triage", job.status, job.status, decision="no_test_shortcut", refs=[])
            self._save_state()
            return result

        result = run_with_validation(
            "defect_triage",
            lambda: run_defect_triage(
                client=self.client,
                run_thread_id=run_thread,
                skill=skill,
                job_id=job_id,
                test_results=test_results,
                child_results=child_results,
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
            ),
            "defect_triage_result",
        )
        if not result.get("target_task_ids"):
            inferred_task_ids = []
            for item in test_results:
                task_id = item.get("task_id")
                if task_id and task_id not in inferred_task_ids:
                    inferred_task_ids.append(task_id)
            result["target_task_ids"] = inferred_task_ids
        job.defect_triage = result
        route = result.get("recommended_route")
        if route == "proceed_merge":
            job.defect_status = "READY_TO_MERGE"
        elif route == "send_back_to_dev":
            job.defect_status = "DEFECT_REPAIRING"
        elif route == "send_to_run_manager":
            job.defect_status = "DEFECT_REPLANNING"
        else:
            job.defect_status = "DEFECT_DISCUSSING"
        self._write_checkpoint(job_id, "06_defect_triage", result)
        self._append_event(job_id, "defect_triage", job.status, job.status, decision=route or "", refs=result.get("target_task_ids", []))
        self._save_state()
        return result

    def start_discussion_round(self, job_id: str, triage_result: Dict[str, Any]) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        skill = self._get_skill("run_manager")
        discussion = run_with_validation(
            "discussion_round",
            lambda: run_discussion_round(
                client=self.client,
                run_thread_id=run_thread,
                skill=skill,
                job_id=job_id,
                triage_result=triage_result,
                corrected_job=job.corrected_job or {},
                task_plan=job.task_plan or {},
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
            ),
            "discussion_resolution",
        )
        if job.defect_triage is None:
            job.defect_triage = {}
        job.defect_triage["discussion_round"] = discussion
        job.discussion_required = True
        job.defect_status = "DEFECT_DISCUSSING"
        job.discussion_cycle_count += 1
        if job.discussion_cycle_count > MAX_DISCUSSION_CYCLES:
            job.status = "DEFECT_BLOCKED"
            job.defect_status = "DEFECT_BLOCKED"
        self._write_checkpoint(job_id, "06_discussion_round", discussion)
        self._append_event(job_id, "discussion_round", job.status, job.status, decision=discussion.get("next_route", ""), refs=discussion.get("participants", []))
        self._save_state()
        return discussion

    def handle_dev_repair_loop(self, job_id: str, triage_result: Dict[str, Any], child_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        if job.repair_cycle_count >= MAX_REPAIR_CYCLES:
            overflow_triage = {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "blocked",
                "summary": "repair 循环已超过上限，升级到 discussion round。",
                "severity_assessment": {
                    "highest_severity": "critical",
                    "rationale": "重复返工仍未闭合，自动升级处理。"
                },
                "scope_assessment": {
                    "scope": "systemic",
                    "rationale": "返工回路已出现循环风险。"
                },
                "recommended_route": "start_discussion_round",
                "block_merge": True,
                "block_baseline_update": True,
                "participants": ["test-worker", "dev-worker", "arch-reviewer", "run-manager"],
                "key_findings": ["repair_cycle_limit_exceeded"],
                "next_actions": ["start_discussion_round"]
            }
            validate_with_schema(overflow_triage, SCHEMAS["defect_triage_result"])
            self._append_event(job_id, "dev_repair", job.status, job.status, decision="repair_cycle_limit_exceeded", refs=[])
            return overflow_triage
        job.repair_cycle_count += 1
        job.defect_status = "DEFECT_REPAIRING"
        target_task_ids = triage_result.get("target_task_ids") or []
        primary_target_task_id = target_task_ids[0] if target_task_ids else None

        dev_skill = self._get_skill("dev_worker")
        dev_thread_id = next(
            (
                thread_id
                for thread_id, record in self.state.threads.items()
                if record.job_id == job_id
                and record.role == "dev"
                and (primary_target_task_id is None or record.task_id == primary_target_task_id)
            ),
            None,
        )
        if dev_thread_id is None:
            dev_response = fork_and_run_client_turn(
                client=self.client,
                slot=f"dev_repair_{primary_target_task_id or job_id}",
                parent_thread_id=run_thread,
                title=f"dev-repair-{primary_target_task_id or job_id}",
                prompt=(
                    f"${dev_skill.name} 请根据 defect triage 和 test findings 做最小返工修复。\n\n"
                    f"target_task_ids: {target_task_ids}\n\n"
                    f"triage_result: {triage_result}\n\n"
                    f"child_results: {child_results}"
                ),
                skill=dev_skill,
                metadata={"phase": "dev_repair", "job_id": job_id, "repair_cycle": job.repair_cycle_count},
                cwd=str(self.root),
            )
            dev_thread_id = dev_response["thread_id"]
            self.state.threads[dev_thread_id] = ThreadRecord(
                thread_id=dev_thread_id,
                role="dev",
                status="RUNNING",
                parent_thread_id=run_thread,
                job_id=job_id,
                task_id=primary_target_task_id or f"{job_id}_repair_dev",
            )
        else:
            dev_response = run_client_turn(
                client=self.client,
                slot=f"dev_repair_{primary_target_task_id or job_id}",
                thread_id=dev_thread_id,
                prompt=(
                    f"${dev_skill.name} 请根据 defect triage 和 test findings 做最小返工修复。\n\n"
                    f"target_task_ids: {target_task_ids}\n\n"
                    f"triage_result: {triage_result}\n\n"
                    f"child_results: {child_results}"
                ),
                skill=dev_skill,
                metadata={"phase": "dev_repair", "job_id": job_id, "repair_cycle": job.repair_cycle_count},
                cwd=str(self.root),
            )
        validate_role_result(dev_response["payload"])
        self.state.threads[dev_thread_id].result = dev_response["payload"]
        self.state.threads[dev_thread_id].status = "DONE"
        self.state.threads[dev_thread_id].updated_at = time.time()

        test_skill = self._get_skill("test_worker")
        test_thread_id = next(
            (
                thread_id
                for thread_id, record in self.state.threads.items()
                if record.job_id == job_id
                and record.role == "test"
                and (primary_target_task_id is None or record.task_id == primary_target_task_id)
            ),
            None,
        )
        if test_thread_id is None:
            test_response = fork_and_run_client_turn(
                client=self.client,
                slot=f"test_recheck_{primary_target_task_id or job_id}",
                parent_thread_id=run_thread,
                title=f"test-recheck-{primary_target_task_id or job_id}",
                prompt=(
                    f"${test_skill.name} 请对最新 dev repair 结果做 re-check，并输出完整 test worker 结构化结果。\n\n"
                    f"target_task_ids: {target_task_ids}\n\n"
                    f"triage_result: {triage_result}\n\n"
                    f"dev_repair_result: {dev_response['payload']}"
                ),
                skill=test_skill,
                metadata={"phase": "test_recheck", "job_id": job_id, "repair_cycle": job.repair_cycle_count},
                cwd=str(self.root),
            )
            test_thread_id = test_response["thread_id"]
            self.state.threads[test_thread_id] = ThreadRecord(
                thread_id=test_thread_id,
                role="test",
                status="RUNNING",
                parent_thread_id=run_thread,
                job_id=job_id,
                task_id=primary_target_task_id or f"{job_id}_repair_test",
            )
        else:
            test_response = run_client_turn(
                client=self.client,
                slot=f"test_recheck_{primary_target_task_id or job_id}",
                thread_id=test_thread_id,
                prompt=(
                    f"${test_skill.name} 请对最新 dev repair 结果做 re-check，并输出完整 test worker 结构化结果。\n\n"
                    f"target_task_ids: {target_task_ids}\n\n"
                    f"triage_result: {triage_result}\n\n"
                    f"dev_repair_result: {dev_response['payload']}"
                ),
                skill=test_skill,
                metadata={"phase": "test_recheck", "job_id": job_id, "repair_cycle": job.repair_cycle_count},
                cwd=str(self.root),
            )
        validate_role_result(test_response["payload"])
        self.state.threads[test_thread_id].result = test_response["payload"]
        self.state.threads[test_thread_id].status = "DONE"
        self.state.threads[test_thread_id].updated_at = time.time()

        self._write_checkpoint(job_id, f"06_dev_repair_cycle_{job.repair_cycle_count}", dev_response["payload"])
        self._write_checkpoint(job_id, f"06_test_recheck_cycle_{job.repair_cycle_count}", test_response["payload"])
        self._append_event(job_id, "dev_repair_loop", job.status, job.status, decision="repair_and_recheck", refs=target_task_ids)
        updated_child_results = self.collect_active_child_results(job_id)
        return self.defect_triage_round(job_id, updated_child_results)

    def handle_run_manager_replan(self, job_id: str, triage_result: Dict[str, Any], child_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        if job.replan_cycle_count >= MAX_REPLAN_CYCLES:
            blocked = {
                "job_id": job_id,
                "status": "blocked",
                "decision": "rollback_to_correction_round",
                "reason": "replan 循环超过上限，阻断自动流转。",
                "reopen_planning": False,
                "revised_tasks": []
            }
            validate_with_schema(blocked, SCHEMAS["replan_decision"])
            if job.defect_triage is None:
                job.defect_triage = {}
            job.defect_triage["replan_decision"] = blocked
            job.defect_status = "DEFECT_BLOCKED"
            self._save_state()
            return blocked
        job.replan_cycle_count += 1
        skill = self._get_skill("run_manager")
        replan = run_with_validation(
            "run_replan",
            lambda: run_replan_round(
                client=self.client,
                run_thread_id=run_thread,
                skill=skill,
                job_id=job_id,
                triage_result=triage_result,
                child_results=child_results,
                corrected_job=job.corrected_job or {},
                task_plan=job.task_plan or {},
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
            ),
            "replan_decision",
        )
        if job.defect_triage is None:
            job.defect_triage = {}
        job.defect_triage["replan_decision"] = replan
        job.defect_status = "DEFECT_REPLANNING"
        if replan.get("revised_tasks"):
            current = job.task_plan or {"job_id": job_id, "mode": "planning", "tasks": [], "notes": [], "risks": []}
            current["tasks"] = replan["revised_tasks"]
            job.task_plan = current
        self._write_checkpoint(job_id, "06_replan_decision", replan)
        self._append_event(job_id, "run_replan", job.status, job.status, decision=replan.get("decision", ""), refs=[task.get("task_id", "") for task in replan.get("revised_tasks", [])])
        self._save_state()
        return replan

    def _consume_replan_decision(self, job_id: str, replan: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        decision = replan.get("decision")
        revised_tasks = replan.get("revised_tasks", [])
        if decision in {"reopen_current_task", "add_new_test_task", "add_arch_review_task"}:
            child_ids = self.spawn_selected_tasks(job_id, revised_tasks)
            print(f"Respawned child threads after replan: {child_ids}")
            updated_child_results = self.collect_active_child_results(job_id)
            triage_result = self.defect_triage_round(job_id, updated_child_results)
            return self._consume_triage_route(job_id, triage_result, updated_child_results)

        if decision in {"revise_corrected_job", "rollback_to_correction_round"}:
            self.correction_round(job_id)
            corrected_job = self.state.jobs[job_id].corrected_job or {}
            if corrected_job.get("status") == "blocked":
                self.state.jobs[job_id].status = "BLOCKED_AFTER_CORRECTION"
                self.state.jobs[job_id].defect_status = "DEFECT_BLOCKED"
                self._save_state()
                return None
            if not corrected_job.get("ready_for_task_planning", False):
                self.state.jobs[job_id].status = "WAITING_MORE_EVIDENCE"
                self._save_state()
                return None
            self.planning_round(job_id)
            child_ids = self.spawn_role_threads(job_id)
            print(f"Respawned child threads after correction rollback: {child_ids}")
            updated_child_results = self.collect_active_child_results(job_id)
            triage_result = self.defect_triage_round(job_id, updated_child_results)
            return self._consume_triage_route(job_id, triage_result, updated_child_results)

        self.state.jobs[job_id].status = "DEFECT_BLOCKED"
        self.state.jobs[job_id].defect_status = "DEFECT_BLOCKED"
        self._save_state()
        return None

    def _consume_discussion_resolution(self, job_id: str, discussion: Dict[str, Any], child_results: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        next_route = discussion.get("next_route")
        summary = discussion.get("summary", "")
        if next_route == "send_back_to_dev":
            if self.state.jobs[job_id].repair_cycle_count >= MAX_REPAIR_CYCLES:
                self.state.jobs[job_id].status = "DEFECT_BLOCKED"
                self.state.jobs[job_id].defect_status = "DEFECT_BLOCKED"
                self._save_state()
                return None
            triage_result = {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "done",
                "summary": summary,
                "severity_assessment": {"highest_severity": "major", "rationale": "discussion round routed to dev repair"},
                "scope_assessment": {"scope": "local", "rationale": "discussion round judged local repair feasible"},
                "recommended_route": "send_back_to_dev",
                "block_merge": False,
                "block_baseline_update": False,
                "participants": discussion.get("participants", []),
                "target_task_ids": (self.state.jobs[job_id].defect_triage or {}).get("target_task_ids", []),
                "key_findings": [],
                "next_actions": discussion.get("next_actions", []),
            }
            validate_with_schema(triage_result, SCHEMAS["defect_triage_result"])
            return self._consume_triage_route(job_id, triage_result, child_results)
        if next_route == "send_to_run_manager":
            triage_result = {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "done",
                "summary": summary,
                "severity_assessment": {"highest_severity": "major", "rationale": "discussion round routed to run manager"},
                "scope_assessment": {"scope": "cross_task", "rationale": "discussion round judged replan necessary"},
                "recommended_route": "send_to_run_manager",
                "block_merge": False,
                "block_baseline_update": False,
                "participants": discussion.get("participants", []),
                "target_task_ids": (self.state.jobs[job_id].defect_triage or {}).get("target_task_ids", []),
                "key_findings": [],
                "next_actions": discussion.get("next_actions", []),
            }
            validate_with_schema(triage_result, SCHEMAS["defect_triage_result"])
            return self._consume_triage_route(job_id, triage_result, child_results)
        if next_route == "rollback_to_correction_round":
            self.correction_round(job_id)
            corrected_job = self.state.jobs[job_id].corrected_job or {}
            if corrected_job.get("status") == "blocked":
                self.state.jobs[job_id].status = "BLOCKED_AFTER_CORRECTION"
                self.state.jobs[job_id].defect_status = "DEFECT_BLOCKED"
                self._save_state()
                return None
            if not corrected_job.get("ready_for_task_planning", False):
                self.state.jobs[job_id].status = "WAITING_MORE_EVIDENCE"
                self._save_state()
                return None
            self.planning_round(job_id)
            child_ids = self.spawn_role_threads(job_id)
            print(f"Respawned child threads after discussion rollback: {child_ids}")
            updated_child_results = self.collect_active_child_results(job_id)
            triage_result = self.defect_triage_round(job_id, updated_child_results)
            return self._consume_triage_route(job_id, triage_result, updated_child_results)

        self.state.jobs[job_id].status = "DEFECT_BLOCKED"
        self.state.jobs[job_id].defect_status = "DEFECT_BLOCKED"
        self._save_state()
        return None

    def _consume_triage_route(self, job_id: str, triage_result: Dict[str, Any], child_results: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        route = triage_result.get("recommended_route")
        if route == "proceed_merge":
            self.state.jobs[job_id].defect_status = "READY_TO_MERGE"
            self._save_state()
            return child_results
        if route == "send_back_to_dev":
            recheck_result = self.handle_dev_repair_loop(job_id, triage_result, child_results)
            updated_child_results = self.collect_active_child_results(job_id)
            return self._consume_triage_route(job_id, recheck_result, updated_child_results)
        if route == "send_to_run_manager":
            replan = self.handle_run_manager_replan(job_id, triage_result, child_results)
            return self._consume_replan_decision(job_id, replan)
        if route == "start_discussion_round" or triage_result.get("block_merge") or triage_result.get("block_baseline_update"):
            discussion = self.start_discussion_round(job_id, triage_result)
            return self._consume_discussion_resolution(job_id, discussion, child_results)
        self.state.jobs[job_id].status = "DEFECT_BLOCKED"
        self.state.jobs[job_id].defect_status = "DEFECT_BLOCKED"
        self._save_state()
        return None

    def merge_in_run_baseline(self, job_id: str, child_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        run_thread = self.ensure_run_thread()
        skill = self._get_skill("run_manager")

        result = run_with_validation(
            "merge",
            lambda: run_merge(
                client=self.client,
                run_thread_id=run_thread,
                skill=skill,
                job_id=job_id,
                child_results=child_results,
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
            ),
            "merge_result",
        )
        job.final_summary = result
        self._write_checkpoint(job_id, "07_merge", result)
        self._append_event(job_id, "merge", job.status, "MERGED", decision="merge_complete", refs=[])
        job.status = "MERGED"
        self._save_state()
        return result

    def refresh_learning_baseline(self, job_id: str) -> Dict[str, Any]:
        job = self.state.jobs[job_id]
        learning_thread = self.ensure_learning_thread()
        skill = self._get_skill("learn_baseline")

        result = run_with_validation(
            "baseline_refresh",
            lambda: run_refresh_learning_baseline(
                client=self.client,
                learning_thread_id=learning_thread,
                skill=skill,
                merge_result=job.final_summary,
                schema_map=SCHEMAS,
                validate_with_schema=validate_with_schema,
                job_id=job_id,
            ),
            "baseline_snapshot",
        )
        self.state.baseline_snapshot = result
        self._write_checkpoint(job_id, "08_baseline_refresh", result)
        self._append_event(job_id, "baseline_refresh", job.status, "DONE", decision="baseline_refresh_complete", refs=[])
        job.status = "DONE"
        self._save_state()
        return result

    # ---------- End-to-end ----------

    def run_job(self, raw_request: str) -> str:
        job_id = self.create_job(raw_request=raw_request, source="manual")
        return self.resume_job(job_id)


def validate_claims(claims: List[Dict[str, Any]]) -> None:
    for claim in claims:
        validate_with_schema(claim, SCHEMAS["claim"])


def validate_role_result(result: Dict[str, Any]) -> None:
    role = result.get("role")
    if role == "dev":
        validate_with_schema(result, SCHEMAS["dev_worker_result"])
    elif role == "test":
        validate_with_schema(result, SCHEMAS["test_worker_result"])
    elif role == "arch_review":
        validate_with_schema(result, SCHEMAS["arch_reviewer_result"])
    else:
        raise SchemaValidationError(f"未知 role，无法校验: {role}")


def run_client_turn(
    client,
    slot: str,
    thread_id: str,
    prompt: str,
    skill=None,
    metadata: Optional[Dict[str, Any]] = None,
    is_plan: bool = False,
    effort: str = "low",
    cwd: Optional[str] = None,
) -> Dict[str, Any]:
    return client.run_business_turn(
        slot=slot,
        prompt=prompt,
        force_new=False,
        fork_thread="",
        is_plan=is_plan,
        effort=effort,
        skill_name=getattr(skill, "name", "") if skill is not None else "",
        cwd=cwd,
        metadata=metadata,
        rename=False,
    )


def fork_and_run_client_turn(
    client,
    slot: str,
    parent_thread_id: str,
    title: str,
    prompt: str,
    skill=None,
    metadata: Optional[Dict[str, Any]] = None,
    cwd: Optional[str] = None,
) -> Dict[str, Any]:
    return client.run_business_turn(
        slot=slot,
        prompt=prompt,
        force_new=False,
        fork_thread=parent_thread_id,
        is_plan=False,
        effort="low",
        skill_name=getattr(skill, "name", "") if skill is not None else "",
        cwd=cwd,
        metadata=metadata,
        rename=True,
        parent_slot="run_baseline",
    )


def run_with_validation(step_name: str, fn, schema_key: str, max_retries: int = 2):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            result = fn()
            validate_with_schema(result, SCHEMAS[schema_key])
            return result
        except Exception as e:
            last_error = e
            print(f"[{step_name}] 第 {attempt + 1} 次失败: {e}")
    raise RuntimeError(f"{step_name} 最终失败: {last_error}")

def run_project_coach_v1(
    client,
    run_thread_id: str,
    skill,
    raw_request: str,
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    """
    调用 project-coach，生成 clarified_job_v1
    """

    prompt = (
        "$project-coach 请对以下原始需求做第一轮澄清。\n\n"
        "要求：\n"
        "1. 重述问题\n"
        "2. 推测真实目标\n"
        "3. 提炼成功标准\n"
        "4. 生成结构化 claims\n"
        "5. 标出 missing_evidence\n"
        "6. 输出 clarified_job_v1 JSON\n\n"
        f"原始需求：{raw_request}"
    )

    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={
            "phase": "coach_v1",
            "raw_request": raw_request,
        },
    )

    # 这里你要换成自己真实的 JSON 提取逻辑
    result = response["payload"]

    validate_with_schema(result, schema_map["clarified_job"])

    return result


def run_single_evidence_worker(
    client,
    run_thread_id: str,
    skill,
    claim: Dict[str, Any],
) -> Dict[str, Any]:
    """
    调用单个 evidence worker
    """
    prompt = (
        f"${skill.name} 请围绕以下 claim 做取证。\n\n"
        f"claim_id: {claim['claim_id']}\n"
        f"claim: {claim['claim']}\n"
        f"type: {claim.get('type', '')}\n\n"
        "请输出结构化 JSON。"
    )

    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={
            "phase": "verification",
            "claim_id": claim["claim_id"],
            "claim": claim["claim"],
            "worker": skill.name,
        },
    )

    return response["payload"]


def build_evidence_pack(
    claim_id: str,
    doc_result: Dict[str, Any],
    code_result: Dict[str, Any],
    runtime_result: Dict[str, Any],
    contradiction_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    聚合成统一 evidence_pack
    """

    # 一个很简单的 final_status 判断逻辑，后面你可以升级
    if contradiction_result.get("recommendation") == "block_baseline_update":
        final_status = "rejected"
    elif (
        doc_result.get("supported") or
        code_result.get("supported") or
        runtime_result.get("supported")
    ):
        if contradiction_result.get("unresolved"):
            final_status = "needs_more_evidence"
        elif (
            doc_result.get("support_level") == "fully_supported" or
            code_result.get("support_level") == "fully_supported" or
            runtime_result.get("support_level") == "fully_supported"
        ):
            final_status = "confirmed"
        else:
            final_status = "partially_confirmed"
    else:
        final_status = "needs_more_evidence"

    summary = (
        f"doc={doc_result.get('support_level')}, "
        f"code={code_result.get('support_level')}, "
        f"runtime={runtime_result.get('support_level')}, "
        f"conflict={contradiction_result.get('conflict_strength')}"
    )

    return {
        "claim_id": claim_id,
        "doc_evidence": doc_result,
        "code_evidence": code_result,
        "runtime_evidence": runtime_result,
        "contradiction_check": contradiction_result,
        "final_status": final_status,
        "summary": summary,
    }


def run_verification_for_claim(
    client,
    run_thread_id: str,
    claim: Dict[str, Any],
    skill_registry: Dict[str, Any],
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    """
    对单条 claim 执行完整 verification
    """

    doc_result = run_single_evidence_worker(
        client=client,
        run_thread_id=run_thread_id,
        skill=skill_registry["doc_evidence_worker"],
        claim=claim,
    )

    code_result = run_single_evidence_worker(
        client=client,
        run_thread_id=run_thread_id,
        skill=skill_registry["code_evidence_worker"],
        claim=claim,
    )

    runtime_result = run_single_evidence_worker(
        client=client,
        run_thread_id=run_thread_id,
        skill=skill_registry["runtime_evidence_worker"],
        claim=claim,
    )

    contradiction_prompt_input = {
        "claim_id": claim["claim_id"],
        "claim": claim["claim"],
        "doc_evidence": doc_result,
        "code_evidence": code_result,
        "runtime_evidence": runtime_result,
    }

    contradiction_prompt = (
        "$contradiction-checker 请围绕以下 claim 与证据做冲突检查。\n\n"
        f"{contradiction_prompt_input}\n\n"
        "请输出结构化 JSON。"
    )

    contradiction_response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=contradiction_prompt,
        skill=skill_registry["contradiction_checker"],
        metadata={
            "phase": "contradiction_check",
            "claim_id": claim["claim_id"],
        },
    )

    contradiction_result = contradiction_response["payload"]

    evidence_pack = build_evidence_pack(
        claim_id=claim["claim_id"],
        doc_result=doc_result,
        code_result=code_result,
        runtime_result=runtime_result,
        contradiction_result=contradiction_result,
    )

    validate_with_schema(evidence_pack, schema_map["evidence_pack"])
    return evidence_pack


def run_project_coach_v2(
    client,
    run_thread_id: str,
    skill,
    clarified_job_v1: Dict[str, Any],
    evidence_packs: List[Dict[str, Any]],
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    prompt = (
        "$project-coach 结合 evidence_pack，对 clarified_job_v1 做第二轮修正。\n"
        "输出 clarified_job_v2，并给出是否 ready_for_run_planning。\n\n"
        f"clarified_job_v1: {clarified_job_v1}\n\n"
        f"evidence_packs: {evidence_packs}"
    )

    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={
            "phase": "coach_v2",
            "job_id": clarified_job_v1["job_id"],
        },
    )

    result = response["payload"]
    validate_with_schema(result, schema_map["clarified_job"])

    return result


def run_correction_round(
    client,
    run_thread_id: str,
    clarified_job_v2: Dict[str, Any],
    skill_registry: Dict[str, Any],
    schema_map: Dict[str, Any],
    validate_with_schema,
    job_id: str,
    raw_request: str,
) -> Dict[str, Any]:
    outputs = []
    skill_schema_pairs = [
        ("demand_critic", "demand_critic_result"),
        ("solution_designer", "solution_designer_result"),
        ("risk_reviewer", "risk_reviewer_result"),
    ]

    for skill_key, schema_key in skill_schema_pairs:
        skill = skill_registry[skill_key]
        prompt = (
            f"${skill.name} 请基于 clarified_job_v2 参与需求博弈/校正，"
            "输出结构化观点。"
        )
        response = run_client_turn(
            client=client,
            slot="run_baseline",
            thread_id=run_thread_id,
            prompt=prompt,
            skill=skill,
            metadata={"phase": "correction", "job_id": job_id},
        )
        payload = response["payload"]
        validate_with_schema(payload, schema_map[schema_key])
        outputs.append(
            {
                "skill": skill_key,
                "payload": payload,
            }
        )

    corrected_job = {
        "job_id": job_id,
        "status": "approved" if not any(
            item["payload"].get("status") == "blocked"
            for item in outputs
            if isinstance(item["payload"], dict)
        ) else "blocked",
        "corrected_goal": (
            (clarified_job_v2 or {}).get("suspected_true_goal")
            or (clarified_job_v2 or {}).get("clarified_problem")
            or raw_request
        ),
        "chosen_approach": next(
            (
                item["payload"].get("chosen_approach")
                for item in outputs
                if isinstance(item["payload"], dict) and item["payload"].get("chosen_approach")
            ),
            "balanced",
        ),
        "reasons": [
            item["payload"].get("summary")
            for item in outputs
            if isinstance(item["payload"], dict) and item["payload"].get("summary")
        ],
        "open_questions": [
            question
            for item in outputs
            if isinstance(item["payload"], dict)
            for question in item["payload"].get("open_questions", [])
        ],
        "risks": [
            risk
            for item in outputs
            if isinstance(item["payload"], dict)
            for risk in (
                item["payload"].get("risks", [])
                + item["payload"].get("hard_risks", [])
                + item["payload"].get("soft_risks", [])
            )
        ],
        "ready_for_task_planning": not any(
            item["payload"].get("status") == "blocked"
            for item in outputs
            if isinstance(item["payload"], dict)
        ),
    }
    validate_with_schema(corrected_job, schema_map["corrected_job"])
    return corrected_job


def run_task_planning(
    client,
    run_thread_id: str,
    skill,
    corrected_job: Dict[str, Any],
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    """
    调用 run-manager 生成 task_plan
    """

    prompt = (
        "$run-manager 请基于以下 corrected_job 进入 planning 模式。\n\n"
        "要求：\n"
        "1. 输出最小可执行 task 集\n"
        "2. 每个 task 必须包含 task_id / role / goal / needs_thread / priority / depends_on\n"
        "3. 只在必要时设置 needs_thread=true\n"
        "4. 输出 task_plan JSON\n\n"
        f"corrected_job: {corrected_job}"
    )

    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={
            "phase": "task_planning",
            "job_id": corrected_job["job_id"],
        },
    )

    result = response["payload"]
    validate_with_schema(result, schema_map["task_plan"])
    return result


def run_merge(
    client,
    run_thread_id: str,
    skill,
    job_id: str,
    child_results: List[Dict[str, Any]],
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    prompt = (
        "$run-manager 请对以下 role 线程结果做去噪汇总。\n"
        "要求区分 accepted_findings / rejected_findings / risks / open_questions / final_summary。\n\n"
        f"child_results: {child_results}"
    )

    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={
            "phase": "merge",
            "job_id": job_id,
            "child_results": child_results,
        },
    )

    result = response["payload"]
    validate_with_schema(result, schema_map["merge_result"])
    return result


def run_defect_triage(
    client,
    run_thread_id: str,
    skill,
    job_id: str,
    test_results: List[Dict[str, Any]],
    child_results: List[Dict[str, Any]],
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    prompt = (
        "$defect-triage 请对当前 job 的测试结果做缺陷分流。\n"
        "你必须输出 severity、scope、recommended_route，以及是否阻断 merge / baseline。\n\n"
        f"job_id: {job_id}\n\n"
        f"test_results: {test_results}\n\n"
        f"child_results: {child_results}"
    )

    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={
            "phase": "defect_triage",
            "job_id": job_id,
        },
    )

    result = response["payload"]
    validate_with_schema(result, schema_map["defect_triage_result"])
    return result


def run_replan_round(
    client,
    run_thread_id: str,
    skill,
    job_id: str,
    triage_result: Dict[str, Any],
    child_results: List[Dict[str, Any]],
    corrected_job: Dict[str, Any],
    task_plan: Dict[str, Any],
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    prompt = (
        "$run-manager 请根据 defect triage 与当前 child results 做重规划判断。\n"
        "输出 replan decision，并在必要时给出 revised_tasks。\n\n"
        f"job_id: {job_id}\n\n"
        f"triage_result: {triage_result}\n\n"
        f"corrected_job: {corrected_job}\n\n"
        f"task_plan: {task_plan}\n\n"
        f"child_results: {child_results}"
    )
    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={"phase": "run_replan", "job_id": job_id},
    )
    result = response["payload"]
    validate_with_schema(result, schema_map["replan_decision"])
    return result


def run_discussion_round(
    client,
    run_thread_id: str,
    skill,
    job_id: str,
    triage_result: Dict[str, Any],
    corrected_job: Dict[str, Any],
    task_plan: Dict[str, Any],
    schema_map: Dict[str, Any],
    validate_with_schema,
) -> Dict[str, Any]:
    prompt = (
        "$run-manager 请围绕当前 critical/systemic defect 做讨论回合裁决。\n"
        "参与视角至少包含 test-worker、dev-worker、arch-reviewer、run-manager。\n"
        "输出 discussion_resolution。\n\n"
        f"job_id: {job_id}\n\n"
        f"triage_result: {triage_result}\n\n"
        f"corrected_job: {corrected_job}\n\n"
        f"task_plan: {task_plan}"
    )
    response = run_client_turn(
        client=client,
        slot="run_baseline",
        thread_id=run_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={"phase": "discussion_round", "job_id": job_id},
    )
    result = response["payload"]
    validate_with_schema(result, schema_map["discussion_resolution"])
    return result


def run_refresh_learning_baseline(
    client,
    learning_thread_id: str,
    skill,
    merge_result: Dict[str, Any],
    schema_map: Dict[str, Any],
    validate_with_schema,
    job_id: str,
) -> Dict[str, Any]:
    prompt = (
        "$learn-baseline 请吸收本次 run 基线最终去噪结论。\n"
        "只将稳定、已验证、长期有效内容更新到 baseline。\n\n"
        f"merge_result: {merge_result}"
    )

    response = run_client_turn(
        client=client,
        slot="learning_baseline",
        thread_id=learning_thread_id,
        prompt=prompt,
        skill=skill,
        metadata={
            "phase": "refresh_learning_baseline",
            "job_id": job_id,
        },
    )

    result = response["payload"]
    validate_with_schema(result, schema_map["baseline_snapshot"])
    return result


def main() -> None:
    project_root = Path(os.environ.get("PROJECT_ROOT", str(REPO_ROOT))).resolve()
    orchestrator = Orchestrator(project_root)
    try:
        resume_job_id = os.environ.get("RESUME_JOB_ID")
        resume_latest = os.environ.get("RESUME_LATEST", "").lower() in {"1", "true", "yes"}
        raw_request = os.environ.get(
            "RAW_REQUEST",
            "请根据 PROJECT_GUIDE 和当前仓库状态，推进自动化线程系统的下一步实现。"
        )

        if resume_job_id:
            job_id = orchestrator.resume_job(resume_job_id)
        elif resume_latest:
            resumed = orchestrator.resume_latest_incomplete_job()
            if resumed is None:
                job_id = orchestrator.run_job(raw_request)
            else:
                job_id = resumed
        else:
            job_id = orchestrator.run_job(raw_request)
        print(f"Completed job: {job_id}")
    finally:
        orchestrator.client.stop()


if __name__ == "__main__":
    main()
