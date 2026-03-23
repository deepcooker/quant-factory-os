from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional


class FakeAppServerClient:
    def __init__(self, scenario: str = "happy_path"):
        self.scenario = scenario
        self.started = False
        self._thread_counter = 0
        self.calls: List[Dict[str, Any]] = []
        self.slot_threads: Dict[str, str] = {}
        self.role_call_counts: Dict[str, int] = {}
        self.triage_counts: Dict[str, int] = {}
        self.replan_counts: Dict[str, int] = {}

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False

    def create_thread(self, title: str, cwd: Optional[str] = None) -> str:
        self._thread_counter += 1
        return f"thread_{self._thread_counter}"

    def resume_thread(self, thread_id: str) -> str:
        return thread_id

    def fork_thread(self, parent_thread_id: str, title: str) -> str:
        self._thread_counter += 1
        return f"thread_{self._thread_counter}"

    def run_business_turn(
        self,
        slot: str,
        prompt: str = "",
        force_new: bool = False,
        fork_thread: str = "",
        is_plan: bool = False,
        effort: str = "low",
        skill_name: str = "",
        cwd: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        rename: bool = True,
        identity: bool = False,
        is_test: bool = False,
        parent_slot: str = "",
    ) -> Dict[str, Any]:
        if fork_thread:
            thread_id = self.fork_thread(fork_thread, title=slot)
            thread_action = "forked"
        elif slot in self.slot_threads and not force_new:
            thread_id = self.resume_thread(self.slot_threads[slot])
            thread_action = "resumed"
        else:
            thread_id = self.create_thread(title=slot, cwd=cwd)
            thread_action = "started"

        self.slot_threads[slot] = thread_id
        result: Dict[str, Any] = {
            "ok": True,
            "err_code": 0,
            "slot": slot,
            "thread_action": thread_action,
            "thread_id": thread_id,
            "thread_path": "",
            "parent_thread_id": str(fork_thread or ""),
            "thread_name": slot,
            "rename_ok": True if rename else None,
            "rename_error": "",
            "turn_id": "",
            "final_text": "",
            "payload": None,
            "rollout_ready": True,
            "rollout_error": "",
        }

        if prompt:
            skill = type("SkillStub", (), {"name": skill_name})() if skill_name else None
            turn = self.start_turn(thread_id=thread_id, text=prompt, skill=skill, metadata=metadata, cwd=cwd)
            result["payload"] = turn.get("payload")
            result["turn_id"] = f"{thread_id}_turn"
        return result

    def start_turn(
        self,
        thread_id: str,
        text: str,
        skill: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
        cwd: Optional[str] = None,
    ) -> Dict[str, Any]:
        metadata = metadata or {}
        phase = metadata.get("phase", "")
        skill_name = getattr(skill, "name", "")
        payload = self._payload_for(phase=phase, skill_name=skill_name, metadata=metadata, text=text)
        self.calls.append(
            {
                "thread_id": thread_id,
                "phase": phase,
                "skill": skill_name,
                "metadata": metadata,
                "text": text,
                "payload": payload,
            }
        )
        return {"payload": payload}

    def _payload_for(self, phase: str, skill_name: str, metadata: Dict[str, Any], text: str) -> Dict[str, Any]:
        if phase == "learning_baseline_init":
            return self._baseline_snapshot(version=1)
        if phase == "coach_v1":
            return self._clarified_job(raw_request=metadata.get("raw_request", ""), ready=True)
        if phase == "verification":
            return self._evidence_result(worker=metadata.get("worker", skill_name))
        if phase == "contradiction_check":
            return self._contradiction_result()
        if phase == "coach_v2":
            return self._clarified_job(raw_request="refined", ready=True, job_id=metadata.get("job_id", "job_unknown"))
        if phase == "correction":
            return self._correction_payload(skill_name)
        if phase == "task_planning":
            return self._task_plan(job_id=metadata["job_id"])
        if phase == "role_execution":
            return self._role_result(task_id=metadata["task_id"], role=metadata["role"])
        if phase == "dev_repair":
            return self._dev_result(task_id=self._extract_target_task_id(text))
        if phase == "test_recheck":
            task_id = self._extract_target_task_id(text)
            if self.scenario == "repair_cycle_limit_block":
                return self._test_result(task_id=task_id, severity="major", route="send_back_to_dev", summary="repair still failing")
            return self._test_result(task_id=task_id, severity="none", route="proceed_merge", summary="repair recheck clean")
        if phase == "defect_triage":
            return self._triage_result(job_id=metadata["job_id"])
        if phase == "run_replan":
            return self._replan_result(job_id=metadata["job_id"])
        if phase == "discussion_round":
            return self._discussion_result(job_id=metadata["job_id"])
        if phase == "merge":
            return self._merge_result(job_id=metadata["job_id"])
        if phase == "refresh_learning_baseline":
            return self._baseline_snapshot(version=2)
        raise RuntimeError(f"Unsupported fake phase: {phase} / skill={skill_name}")

    def _extract_target_task_id(self, text: str) -> str:
        marker = "target_task_ids: "
        if marker in text:
            raw = text.split(marker, 1)[1].split("\n", 1)[0].strip()
            if raw.startswith("[") and raw.endswith("]"):
                try:
                    values = json.loads(raw.replace("'", '"'))
                    if values:
                        return values[0]
                except Exception:
                    pass
        return "task_test_hotspot"

    def _clarified_job(self, raw_request: str, ready: bool, job_id: str = "job_unknown") -> Dict[str, Any]:
        return {
            "job_id": job_id,
            "raw_request": raw_request or "smoke request",
            "clarified_problem": "需要验证实验性 orchestrator 主流程是否可回归。",
            "suspected_true_goal": "建立一条可验证、可恢复、可回归的实验线。",
            "success_criteria": ["主流程可完成", "状态可恢复", "关键事件可审计"],
            "assumptions": ["使用 fake app-server 客户端", "schemas 已存在"],
            "missing_evidence": [],
            "claims": [{"claim_id": "claim_1", "claim": "当前实验线可以闭环运行"}],
            "recommended_next_step": "verification" if ready else "collect_more_evidence",
            "ready_for_run_planning": ready,
        }

    def _evidence_result(self, worker: str) -> Dict[str, Any]:
        return {
            "supported": True,
            "support_level": "fully_supported",
            "support_refs": [f"{worker}:ref1"],
            "conflict_refs": [],
            "gaps": [],
            "summary": f"{worker} supports the claim",
        }

    def _contradiction_result(self) -> Dict[str, Any]:
        return {
            "has_conflict": False,
            "conflict_type": [],
            "conflict_strength": "none",
            "conflict_points": [],
            "stronger_side": "evidence_pack",
            "unresolved": False,
            "recommendation": "no_conflict",
            "summary": "no contradiction",
        }

    def _correction_payload(self, skill_name: str) -> Dict[str, Any]:
        if skill_name == "solution-designer":
            return {
                "status": "approved",
                "summary": "保留当前主线并保持最小执行路径。",
                "chosen_approach": "minimal-smoke",
                "open_questions": [],
                "risks": [],
            }
        if skill_name == "risk-reviewer":
            return {
                "status": "approved",
                "summary": "风险可控，适合做 smoke。",
                "open_questions": [],
                "risks": [],
                "hard_risks": [],
                "soft_risks": [],
            }
        return {
            "status": "approved",
            "summary": "需求表达清晰，可继续。",
            "open_questions": [],
            "risks": [],
        }

    def _task_plan(self, job_id: str) -> Dict[str, Any]:
        if self.scenario == "major_defect_replan":
            tasks = [
                {
                    "task_id": "task_test_hotspot",
                    "role": "test",
                    "goal": "验证热点路径",
                    "needs_thread": True,
                    "priority": "high",
                    "depends_on": [],
                },
                {
                    "task_id": "task_test_control",
                    "role": "test",
                    "goal": "验证对照路径",
                    "needs_thread": True,
                    "priority": "medium",
                    "depends_on": [],
                },
            ]
        else:
            tasks = [
                {
                    "task_id": "task_dev_core",
                    "role": "dev",
                    "goal": "完成核心实现",
                    "needs_thread": True,
                    "priority": "high",
                    "depends_on": [],
                },
                {
                    "task_id": "task_test_core",
                    "role": "test",
                    "goal": "完成主流程验证",
                    "needs_thread": True,
                    "priority": "high",
                    "depends_on": ["task_dev_core"],
                },
            ]
        return {
            "job_id": job_id,
            "mode": "planning",
            "tasks": tasks,
            "notes": [],
            "risks": [],
        }

    def _role_result(self, task_id: str, role: str) -> Dict[str, Any]:
        key = f"{task_id}:{role}"
        self.role_call_counts[key] = self.role_call_counts.get(key, 0) + 1
        if role == "dev":
            return self._dev_result(task_id=task_id)
        if role == "arch_review":
            return {
                "task_id": task_id,
                "role": "arch_review",
                "status": "done",
                "decision": "accept",
                "summary": "architecture accepted",
                "hard_risks": [],
                "soft_risks": [],
                "recommended_actions": [],
            }
        if self.scenario == "major_defect_replan" and task_id == "task_test_hotspot" and self.role_call_counts[key] == 1:
            return self._test_result(task_id=task_id, severity="major", route="send_to_run_manager", summary="hotspot defect found")
        if self.scenario in {"send_back_to_dev", "repair_cycle_limit_block"} and task_id == "task_test_core" and self.role_call_counts[key] == 1:
            return self._test_result(task_id=task_id, severity="minor", route="send_back_to_dev", summary="repairable defect found")
        if self.scenario == "critical_discussion_block" and task_id == "task_test_core":
            return self._test_result(task_id=task_id, severity="critical", route="start_discussion_round", summary="critical systemic defect found")
        return self._test_result(task_id=task_id, severity="none", route="proceed_merge", summary="tests passed")

    def _dev_result(self, task_id: str) -> Dict[str, Any]:
        return {
            "task_id": task_id,
            "role": "dev",
            "status": "done",
            "summary": "implementation done",
            "artifacts": [f"artifact:{task_id}"],
            "risks": [],
            "next_actions": [],
            "requested_child_threads": [],
        }

    def _test_result(self, task_id: str, severity: str, route: str, summary: str) -> Dict[str, Any]:
        return {
            "task_id": task_id,
            "role": "test",
            "status": "done",
            "summary": summary,
            "requirement_findings": [],
            "functional_findings": [] if severity == "none" else [summary],
            "workflow_findings": [],
            "data_state_findings": [],
            "non_functional_findings": [],
            "severity_assessment": {
                "highest_severity": severity,
                "rationale": summary,
            },
            "scope_assessment": {
                "scope": "none" if severity == "none" else "local",
                "rationale": summary,
            },
            "recommended_escalation": {
                "route": route,
                "block_merge": severity != "none",
                "block_baseline_update": severity != "none",
                "reason": summary,
            },
            "confirmed_failures": [] if severity == "none" else [summary],
            "suspected_failures": [],
            "untested_areas": [],
            "artifacts": [f"test-log:{task_id}"],
            "next_actions": [],
            "requested_child_threads": [],
        }

    def _triage_result(self, job_id: str) -> Dict[str, Any]:
        self.triage_counts[job_id] = self.triage_counts.get(job_id, 0) + 1
        if self.scenario == "major_defect_replan" and self.triage_counts[job_id] == 1:
            return {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "done",
                "summary": "需要对热点 task 重新规划测试路径。",
                "severity_assessment": {"highest_severity": "major", "rationale": "hotspot defect"},
                "scope_assessment": {"scope": "local", "rationale": "single task affected"},
                "recommended_route": "send_to_run_manager",
                "block_merge": True,
                "block_baseline_update": True,
                "participants": ["test-worker", "run-manager"],
                "target_task_ids": ["task_test_hotspot"],
                "key_findings": ["hotspot_defect"],
                "next_actions": ["replan_targeted_task"],
            }
        if self.scenario == "send_back_to_dev" and self.triage_counts[job_id] == 1:
            return {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "done",
                "summary": "局部缺陷可直接回开发修复。",
                "severity_assessment": {"highest_severity": "minor", "rationale": "repairable local issue"},
                "scope_assessment": {"scope": "local", "rationale": "single task affected"},
                "recommended_route": "send_back_to_dev",
                "block_merge": False,
                "block_baseline_update": False,
                "participants": ["test-worker", "dev-worker"],
                "target_task_ids": ["task_test_core"],
                "key_findings": ["repairable_defect"],
                "next_actions": ["repair_and_recheck"],
            }
        if self.scenario == "critical_discussion_block":
            return {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "done",
                "summary": "critical defect requires discussion",
                "severity_assessment": {"highest_severity": "critical", "rationale": "systemic critical defect"},
                "scope_assessment": {"scope": "systemic", "rationale": "cannot auto-resolve safely"},
                "recommended_route": "start_discussion_round",
                "block_merge": True,
                "block_baseline_update": True,
                "participants": ["test-worker", "dev-worker", "arch-reviewer", "run-manager"],
                "target_task_ids": ["task_test_core"],
                "key_findings": ["critical_systemic_defect"],
                "next_actions": ["start_discussion_round"],
            }
        if self.scenario == "repair_cycle_limit_block":
            return {
                "job_id": job_id,
                "role": "defect_triage",
                "status": "done",
                "summary": "持续回开发修复，等待达到 cycle limit",
                "severity_assessment": {"highest_severity": "major", "rationale": "defect persists after repair"},
                "scope_assessment": {"scope": "local", "rationale": "single task remains broken"},
                "recommended_route": "send_back_to_dev",
                "block_merge": False,
                "block_baseline_update": False,
                "participants": ["test-worker", "dev-worker"],
                "target_task_ids": ["task_test_core"],
                "key_findings": ["persistent_defect"],
                "next_actions": ["repair_and_recheck"],
            }
        return {
            "job_id": job_id,
            "role": "defect_triage",
            "status": "done",
            "summary": "当前结果允许继续 merge。",
            "severity_assessment": {"highest_severity": "none", "rationale": "no active defect"},
            "scope_assessment": {"scope": "none", "rationale": "all active test results clean"},
            "recommended_route": "proceed_merge",
            "block_merge": False,
            "block_baseline_update": False,
            "participants": ["test-worker", "run-manager"],
            "target_task_ids": [],
            "key_findings": [],
            "next_actions": [],
        }

    def _replan_result(self, job_id: str) -> Dict[str, Any]:
        self.replan_counts[job_id] = self.replan_counts.get(job_id, 0) + 1
        return {
            "job_id": job_id,
            "status": "done",
            "decision": "reopen_current_task",
            "reason": "只重跑热点 task，避免整单重跑。",
            "reopen_planning": False,
            "revised_tasks": [
                {
                    "task_id": "task_test_hotspot",
                    "role": "test",
                    "goal": "重跑热点测试并验证修复后状态",
                    "needs_thread": True,
                    "priority": "high",
                    "depends_on": [],
                }
            ],
        }

    def _discussion_result(self, job_id: str) -> Dict[str, Any]:
        if self.scenario in {"critical_discussion_block", "repair_cycle_limit_block"}:
            return {
                "job_id": job_id,
                "status": "done",
                "participants": ["test-worker", "dev-worker", "arch-reviewer", "run-manager"],
                "root_cause": "critical unresolved defect",
                "decision": "block_job",
                "next_route": "block_job",
                "summary": "discussion decided to block job",
                "next_actions": [],
            }
        return {
            "job_id": job_id,
            "status": "done",
            "participants": ["test-worker", "dev-worker", "arch-reviewer", "run-manager"],
            "root_cause": "synthetic",
            "decision": "block_job",
            "next_route": "block_job",
            "summary": "discussion forced block",
            "next_actions": [],
        }

    def _merge_result(self, job_id: str) -> Dict[str, Any]:
        return {
            "job_id": job_id,
            "mode": "merge",
            "accepted_findings": ["mainline completed"],
            "rejected_findings": [],
            "risks": [],
            "open_questions": [],
            "final_summary": "merge completed",
            "should_update_learning_baseline": True,
        }

    def _baseline_snapshot(self, version: int) -> Dict[str, Any]:
        return {
            "baseline_version": version,
            "project_identity": "quant-factory-os experimental orchestrator",
            "core_truths": [
                {
                    "id": "truth_mainline",
                    "statement": "experimental orchestrator smoke path is available",
                    "evidence_level": "documented",
                    "source_refs": ["tests/fakes/fake_app.py"],
                }
            ],
            "role_model": ["project-coach", "run-manager", "dev-worker", "test-worker"],
            "thread_model": ["learning_baseline", "run_baseline", "role_threads"],
            "constraints": ["fake-client-only"],
            "terminology": ["baseline", "merge", "refresh"],
            "candidate_truths": [],
            "open_questions": [],
            "missing_sources": [],
        }


def prepare_smoke_root(repo_root: Path, name: str) -> Path:
    temp_root = Path(tempfile.mkdtemp(prefix=f"{name}_"))
    for dirname in ["docs", "schemas", ".agents"]:
        src = repo_root / dirname
        dst = temp_root / dirname
        if src.is_dir():
            dst.symlink_to(src, target_is_directory=True)
    agents_src = repo_root / "AGENTS.md"
    if agents_src.exists():
        (temp_root / "AGENTS.md").symlink_to(agents_src)
    (temp_root / "tools").mkdir(parents=True, exist_ok=True)
    shutil.copy2(repo_root / "tools" / "project_config.json", temp_root / "tools" / "project_config.json")
    return temp_root
