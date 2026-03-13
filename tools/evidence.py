#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.project_config import load_runtime_state
    from tools.taskclient import find_task_id_for_run
except ImportError:
    from project_config import load_runtime_state  # type: ignore
    from taskclient import find_task_id_for_run  # type: ignore


RUN_SUMMARY_MERGE_POLICY = {
    "active_tasks": "reconcile_only",
    "completed_tasks": "reconcile_only",
    "source_tasks": "append_dedup",
    "key_updates": "merge_rewrite",
    "cross_task_decisions": "merge_rewrite",
    "cross_task_risks": "merge_rewrite",
    "verification_overview": "append_dedup",
    "next_run_or_next_tasks": "merge_rewrite",
}

RUN_SUMMARY_LEGACY_CLEANUP_POLICY = {
    "mode": "explicit_maintenance_only",
    "target_fields": [
        "key_updates",
        "cross_task_decisions",
        "cross_task_risks",
        "next_run_or_next_tasks",
    ],
    "rewrite_rule": "humanize_and_strip_legacy_task_prefix",
}


def _git(cmd: list[str], cwd: Path) -> str | None:
    try:
        out = subprocess.check_output(cmd, cwd=str(cwd), stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return None


def _runtime_task_for_run(run_id: str) -> str | None:
    task_id = find_task_id_for_run(run_id)
    return task_id or None


def _normalize_list(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        raw = str(item).strip()
        if not raw:
            continue
        for part in raw.split(","):
            value = str(part).strip()
            if not value or value in seen:
                continue
            seen.add(value)
            result.append(value)
    return result


def _ensure_run_summary(reports_dir: Path, run_id: str, task_id: str) -> Path:
    run_summary = reports_dir / "run_summary.json"
    if run_summary.exists():
        return run_summary
    active_tasks = [task_id] if task_id else []
    payload = {
        "run_id": run_id,
        "status": "active",
        "run_goal": "",
        "active_tasks": active_tasks,
        "completed_tasks": [],
        "source_tasks": active_tasks,
        "merge_policy": dict(RUN_SUMMARY_MERGE_POLICY),
        "legacy_cleanup_policy": dict(RUN_SUMMARY_LEGACY_CLEANUP_POLICY),
        "key_updates": [],
        "cross_task_decisions": [],
        "cross_task_risks": [],
        "verification_overview": [],
        "next_run_or_next_tasks": [],
        "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    run_summary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return run_summary


def _load_run_summary(run_summary_path: Path) -> dict[str, Any]:
    payload = json.loads(run_summary_path.read_text(encoding="utf-8"))
    return _sync_merge_policy(payload)


def _save_run_summary(run_summary_path: Path, payload: dict[str, Any]) -> None:
    payload = _sync_merge_policy(payload)
    payload["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_summary_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_task_payload(task_json_file: Path) -> dict[str, Any]:
    return json.loads(task_json_file.read_text(encoding="utf-8"))


def _status_is_completed(status: str) -> bool:
    return str(status).strip().lower() in {"completed", "done"}


def _status_is_active(status: str) -> bool:
    return str(status).strip().lower() in {"active", "draft", "in_progress", "pending_ack", "acknowledged"}


def _append_prefixed(items: list[str], prefix: str) -> list[str]:
    values: list[str] = []
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        values.append(f"{prefix}: {text}")
    return values


def _append_dedup(items: list[str], new_items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in list(items) + list(new_items):
        value = str(item).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _sync_merge_policy(payload: dict[str, Any]) -> dict[str, Any]:
    current = dict(payload.get("merge_policy", {}) or {})
    payload["merge_policy"] = {**RUN_SUMMARY_MERGE_POLICY, **current}
    cleanup_policy = dict(payload.get("legacy_cleanup_policy", {}) or {})
    payload["legacy_cleanup_policy"] = {
        **RUN_SUMMARY_LEGACY_CLEANUP_POLICY,
        **cleanup_policy,
    }
    return payload


def _field_merge_mode(payload: dict[str, Any], field: str) -> str:
    return str(dict(payload.get("merge_policy", {}) or {}).get(field, RUN_SUMMARY_MERGE_POLICY.get(field, "append_dedup"))).strip()


def _rewrite_task_items_as_run_level(task_id: str, items: list[str]) -> list[str]:
    rewritten: list[str] = []
    prefix = f"{task_id}:"
    for item in items:
        value = str(item).strip()
        if not value:
            continue
        if value.startswith(prefix):
            value = value[len(prefix):].strip()
        value = _humanize_summary_item(value)
        if value:
            rewritten.append(value)
    return _canonicalize_run_level_items(rewritten)


def _merge_append_dedup_field(payload: dict[str, Any], field: str, task_id: str, items: list[str]) -> None:
    payload[field] = _append_dedup(
        list(payload.get(field, []) or []),
        _append_prefixed(items, task_id),
    )


def _merge_rewrite_field(payload: dict[str, Any], field: str, task_id: str, items: list[str]) -> None:
    payload[field] = _append_dedup(
        list(payload.get(field, []) or []),
        _rewrite_task_items_as_run_level(task_id, items),
    )


def _merge_task_summary_field(payload: dict[str, Any], field: str, task_id: str, items: list[str]) -> None:
    mode = _field_merge_mode(payload, field)
    if mode == "merge_rewrite":
        _merge_rewrite_field(payload, field, task_id, items)
        return
    if mode == "append_dedup":
        _merge_append_dedup_field(payload, field, task_id, items)
        return
    if mode == "reconcile_only":
        return


def _take_non_empty(items: list[str], limit: int) -> list[str]:
    values = [str(item).strip() for item in items if str(item).strip()]
    return values[:limit]


def _humanize_summary_item(text: str) -> str:
    value = str(text).strip()
    if not value:
        return ""
    prefixes = (
        "task-integrated-multi-role-runtime-chain: ",
        "task-run-summary-writeback-entry: ",
        "task-",
    )
    if value.startswith(prefixes[0]):
        value = value[len(prefixes[0]):]
    elif value.startswith(prefixes[1]):
        value = value[len(prefixes[1]):]
    if value.startswith(prefixes[2]):
        value = value[len(prefixes[2]):]
    value = value.replace("run_summary.json", "run summary")
    value = value.replace("tools/evidence.py", "evidence tool")
    value = value.replace("test_gate", "test gate")
    return value.strip(" -")


def _canonicalize_run_level_items(items: list[str]) -> list[str]:
    merged_roles: list[str] = []
    result: list[str] = []
    for item in items:
        value = str(item).strip()
        if not value:
            continue
        merged_match = re.fullmatch(r"(run-main|dev|test|arch) summary merged", value)
        if merged_match:
            merged_roles.append(merged_match.group(1))
            continue
        if value == "test gate=blocked":
            value = "test gate remains blocked"
        elif value == "test gate=passed":
            value = "test gate has passed"
        elif "all three real summaries are preserved" in value:
            value = "integrated multi-role runtime summaries are preserved and produce an explainable test gate state"
        result.append(value)
    if merged_roles:
        normalized_roles = [role for role in ("run-main", "dev", "test", "arch") if role in set(merged_roles)]
        if len(normalized_roles) >= 2:
            result.append("multi-role runtime summaries are now preserved at run level")
        else:
            result.append(f"{normalized_roles[0]} summary is now preserved at run level")
    return _append_dedup([], result)


def _dedupe_run_level_risks(items: list[str]) -> list[str]:
    """Prefer the most specific blocked-gate risk line over a generic duplicate."""
    deduped = _append_dedup([], items)
    blocked_variants = [item for item in deduped if str(item).strip().startswith("test gate remains blocked")]
    if len(blocked_variants) <= 1:
        return deduped
    most_specific = max(blocked_variants, key=lambda item: (len(str(item).strip()), str(item)))
    result: list[str] = []
    for item in deduped:
        value = str(item).strip()
        if value.startswith("test gate remains blocked") and value != most_specific:
            continue
        result.append(value)
    return result


def _build_baseline_ready_summary(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    run_goal = str(payload.get("run_goal", "")).strip()
    status = str(payload.get("status", "")).strip()
    active_tasks = [str(item).strip() for item in list(payload.get("active_tasks", []) or []) if str(item).strip()]
    key_updates = [_humanize_summary_item(item) for item in _take_non_empty(list(payload.get("key_updates", []) or []), 3)]
    decisions = [_humanize_summary_item(item) for item in _take_non_empty(list(payload.get("cross_task_decisions", []) or []), 2)]
    risks = [_humanize_summary_item(item) for item in _take_non_empty(list(payload.get("cross_task_risks", []) or []), 2)]
    next_steps = [_humanize_summary_item(item) for item in _take_non_empty(list(payload.get("next_run_or_next_tasks", []) or []), 2)]
    key_updates = [item for item in key_updates if item]
    decisions = [item for item in decisions if item]
    risks = [item for item in risks if item]
    next_steps = [item for item in next_steps if item]
    if run_goal:
        lines.append(f"Run goal: {run_goal}.")
    if status:
        lines.append(f"Run status: {status}.")
    if active_tasks:
        lines.append(f"Active tasks: {', '.join(active_tasks)}.")
    if key_updates:
        lines.append("Stable updates:")
        lines.extend([f"- {item}" for item in key_updates])
    if decisions:
        lines.append("Stable decisions:")
        lines.extend([f"- {item}" for item in decisions])
    if risks:
        lines.append("Open risks:")
        lines.extend([f"- {item}" for item in risks])
    if next_steps:
        lines.append("Next steps:")
        lines.extend([f"- {item}" for item in next_steps])
    return "\n".join(lines).strip()


def _normalize_legacy_run_summary_fields(payload: dict[str, Any]) -> dict[str, Any]:
    cleanup_policy = dict(payload.get("legacy_cleanup_policy", {}) or {})
    target_fields = list(cleanup_policy.get("target_fields", []) or [])
    for field in target_fields:
        items = list(payload.get(field, []) or [])
        payload[field] = _canonicalize_run_level_items(
            [_humanize_summary_item(item) for item in items]
        )
        if field == "cross_task_risks":
            payload[field] = _dedupe_run_level_risks(list(payload.get(field, []) or []))
    payload["legacy_cleanup_last_applied_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return payload


def _get_reports_dir(repo: Path, run_id: str) -> Path:
    reports_dir = repo / "reports" / run_id
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


def _iter_run_task_payloads(repo: Path, run_id: str) -> list[dict[str, Any]]:
    tasks_dir = repo / "TASKS"
    payloads: list[dict[str, Any]] = []
    for task_path in sorted(tasks_dir.glob("TASK-*.json")):
        payload = _load_task_payload(task_path)
        if str(payload.get("run_id", "")).strip() != str(run_id).strip():
            continue
        payloads.append(payload)
    return payloads


def _reconcile_run_task_lists(payload: dict[str, Any], task_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    active_tasks: list[str] = []
    completed_tasks: list[str] = []
    source_tasks: list[str] = list(payload.get("source_tasks", []) or [])
    for task_payload in task_payloads:
        task_id = str(task_payload.get("task_id", "")).strip()
        status = str(task_payload.get("status", "")).strip()
        if not task_id:
            continue
        source_tasks.append(task_id)
        if _status_is_completed(status):
            completed_tasks.append(task_id)
            continue
        if _status_is_active(status):
            active_tasks.append(task_id)
    payload["source_tasks"] = _normalize_list(source_tasks)
    payload["completed_tasks"] = _normalize_list(completed_tasks)
    payload["active_tasks"] = [
        item for item in _normalize_list(active_tasks)
        if item not in set(payload["completed_tasks"])
    ]
    payload["status"] = "completed" if not payload["active_tasks"] else "active"
    return payload


def _show_run_summary(repo: Path, run_id: str) -> dict[str, Any]:
    reports_dir = _get_reports_dir(repo, run_id)
    task_id = os.getenv("TASK_ID") or _runtime_task_for_run(run_id) or ""
    run_summary_path = _ensure_run_summary(reports_dir, run_id, task_id)
    return _load_run_summary(run_summary_path)


def _set_run_summary(
    repo: Path,
    run_id: str,
    status: str,
    run_goal: str,
    active_tasks: list[str],
    completed_tasks: list[str],
    source_tasks: list[str],
    key_updates: list[str],
    cross_task_decisions: list[str],
    cross_task_risks: list[str],
    verification_overview: list[str],
    next_run_or_next_tasks: list[str],
) -> dict[str, Any]:
    reports_dir = _get_reports_dir(repo, run_id)
    runtime_task_id = os.getenv("TASK_ID") or _runtime_task_for_run(run_id) or ""
    run_summary_path = _ensure_run_summary(reports_dir, run_id, runtime_task_id)
    payload = _load_run_summary(run_summary_path)
    if str(status).strip():
        payload["status"] = str(status).strip()
    if str(run_goal).strip():
        payload["run_goal"] = str(run_goal).strip()
    if active_tasks:
        payload["active_tasks"] = _normalize_list(active_tasks)
    if completed_tasks:
        payload["completed_tasks"] = _normalize_list(completed_tasks)
    if source_tasks:
        payload["source_tasks"] = _normalize_list(source_tasks)
    if key_updates:
        payload["key_updates"] = _normalize_list(key_updates)
    if cross_task_decisions:
        payload["cross_task_decisions"] = _normalize_list(cross_task_decisions)
    if cross_task_risks:
        payload["cross_task_risks"] = _normalize_list(cross_task_risks)
    if verification_overview:
        payload["verification_overview"] = _normalize_list(verification_overview)
    if next_run_or_next_tasks:
        payload["next_run_or_next_tasks"] = _normalize_list(next_run_or_next_tasks)
    _save_run_summary(run_summary_path, payload)
    return payload


def _merge_task_summary(repo: Path, run_id: str, task_json_file: str) -> dict[str, Any]:
    task_path = (repo / str(task_json_file).strip()).resolve()
    if not task_path.is_file():
        raise FileNotFoundError(f"task json file not found: {task_json_file}")
    task_payload = _load_task_payload(task_path)
    task_id = str(task_payload.get("task_id", "")).strip()
    task_status = str(task_payload.get("status", "")).strip()
    task_summary = dict(task_payload.get("task_summary", {}) or {})

    reports_dir = _get_reports_dir(repo, run_id)
    run_summary_path = _ensure_run_summary(reports_dir, run_id, task_id)
    payload = _load_run_summary(run_summary_path)

    payload["source_tasks"] = _normalize_list(list(payload.get("source_tasks", []) or []) + [task_id])
    if task_status == "completed":
        payload["completed_tasks"] = _normalize_list(list(payload.get("completed_tasks", []) or []) + [task_id])
        payload["active_tasks"] = [item for item in _normalize_list(list(payload.get("active_tasks", []) or [])) if item != task_id]
    elif task_id:
        payload["active_tasks"] = _normalize_list(list(payload.get("active_tasks", []) or []) + [task_id])

    _merge_task_summary_field(payload, "key_updates", task_id, list(task_summary.get("key_updates", []) or []))
    _merge_task_summary_field(payload, "cross_task_decisions", task_id, list(task_summary.get("decisions", []) or []))
    _merge_task_summary_field(
        payload,
        "cross_task_risks",
        task_id,
        list(task_summary.get("risks", []) or []) +
        list((task_summary.get("gap_summary", {}) or {}).get("open_gaps", []) or []),
    )
    payload["cross_task_risks"] = _dedupe_run_level_risks(list(payload.get("cross_task_risks", []) or []))
    _merge_task_summary_field(payload, "verification_overview", task_id, list(task_summary.get("verification", []) or []))
    _merge_task_summary_field(payload, "next_run_or_next_tasks", task_id, list(task_summary.get("next_steps", []) or []))
    _save_run_summary(run_summary_path, payload)
    return payload


def _reconcile_run_summary(repo: Path, run_id: str) -> dict[str, Any]:
    reports_dir = _get_reports_dir(repo, run_id)
    runtime_task_id = os.getenv("TASK_ID") or _runtime_task_for_run(run_id) or ""
    run_summary_path = _ensure_run_summary(reports_dir, run_id, runtime_task_id)
    payload = _load_run_summary(run_summary_path)
    task_payloads = _iter_run_task_payloads(repo, run_id)
    payload = _reconcile_run_task_lists(payload, task_payloads)
    _save_run_summary(run_summary_path, payload)
    return payload


def _compact_run_summary(repo: Path, run_id: str) -> dict[str, Any]:
    reports_dir = _get_reports_dir(repo, run_id)
    runtime_task_id = os.getenv("TASK_ID") or _runtime_task_for_run(run_id) or ""
    run_summary_path = _ensure_run_summary(reports_dir, run_id, runtime_task_id)
    payload = _load_run_summary(run_summary_path)
    payload["baseline_ready_summary"] = _build_baseline_ready_summary(payload)
    _save_run_summary(run_summary_path, payload)
    return payload


def _normalize_run_summary(repo: Path, run_id: str) -> dict[str, Any]:
    reports_dir = _get_reports_dir(repo, run_id)
    runtime_task_id = os.getenv("TASK_ID") or _runtime_task_for_run(run_id) or ""
    run_summary_path = _ensure_run_summary(reports_dir, run_id, runtime_task_id)
    payload = _load_run_summary(run_summary_path)
    payload = _normalize_legacy_run_summary_fields(payload)
    payload["baseline_ready_summary"] = _build_baseline_ready_summary(payload)
    _save_run_summary(run_summary_path, payload)
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--run-summary", action="store_true")
    ap.add_argument("--set-run-summary", action="store_true")
    ap.add_argument("--merge-task-summary", action="store_true")
    ap.add_argument("--reconcile-run-summary", action="store_true")
    ap.add_argument("--compact-run-summary", action="store_true")
    ap.add_argument("--normalize-run-summary", action="store_true")
    ap.add_argument("--task-json-file", default="")
    ap.add_argument("--status", default="")
    ap.add_argument("--run-goal", default="")
    ap.add_argument("--active-task", action="append", default=[])
    ap.add_argument("--completed-task", action="append", default=[])
    ap.add_argument("--source-task", action="append", default=[])
    ap.add_argument("--key-update", action="append", default=[])
    ap.add_argument("--cross-task-decision", action="append", default=[])
    ap.add_argument("--cross-task-risk", action="append", default=[])
    ap.add_argument("--verification-overview", action="append", default=[])
    ap.add_argument("--next-run-or-task", action="append", default=[])
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]
    if args.run_summary:
        print(json.dumps(_show_run_summary(repo, args.run_id), indent=2, ensure_ascii=False))
        return 0
    if args.set_run_summary:
        print(
            json.dumps(
                _set_run_summary(
                    repo,
                    args.run_id,
                    str(args.status),
                    str(args.run_goal),
                    list(args.active_task),
                    list(args.completed_task),
                    list(args.source_task),
                    list(args.key_update),
                    list(args.cross_task_decision),
                    list(args.cross_task_risk),
                    list(args.verification_overview),
                    list(args.next_run_or_task),
                ),
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0
    if args.merge_task_summary:
        task_json_file = str(args.task_json_file).strip()
        if not task_json_file:
            runtime = load_runtime_state()
            task_json_file = str(runtime.current_task_json_file).strip()
        print(json.dumps(_merge_task_summary(repo, args.run_id, task_json_file), indent=2, ensure_ascii=False))
        return 0
    if args.reconcile_run_summary:
        print(json.dumps(_reconcile_run_summary(repo, args.run_id), indent=2, ensure_ascii=False))
        return 0
    if args.compact_run_summary:
        print(json.dumps(_compact_run_summary(repo, args.run_id), indent=2, ensure_ascii=False))
        return 0
    if args.normalize_run_summary:
        print(json.dumps(_normalize_run_summary(repo, args.run_id), indent=2, ensure_ascii=False))
        return 0

    reports_dir = _get_reports_dir(repo, args.run_id)
    task_id = os.getenv("TASK_ID") or _runtime_task_for_run(args.run_id) or ""

    meta = {
        "run_id": args.run_id,
        "task_id": task_id,
        "stop_reason": os.getenv("STOP_REASON") or "",
        "commands_run": [],
        "artifacts": [],
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "cwd": str(repo),
        "user": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
        "host": platform.node(),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "git_commit": _git(["git", "rev-parse", "HEAD"], repo),
        "git_branch": _git(["git", "branch", "--show-current"], repo),
        "note": "generated by tools/evidence.py",
    }

    (reports_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = reports_dir / "summary.md"
    if not summary.exists():
        summary.write_text(
            f"# Summary\n\nRUN_ID: `{args.run_id}`\n\n"
            "## What changed\n- \n\n"
            "## Commands / Outputs\n- \n\n"
            "## Notes\n- \n",
            encoding="utf-8",
        )

    decision = reports_dir / "decision.md"
    if not decision.exists():
        decision.write_text(
            f"# Decision\n\nRUN_ID: `{args.run_id}`\n\n"
            "## Why\n- \n\n"
            "## Options considered\n- \n\n"
            "## Risks / Rollback\n- \n",
            encoding="utf-8",
        )

    run_summary = _ensure_run_summary(reports_dir, args.run_id, task_id)

    print(f"OK: wrote {reports_dir/'meta.json'}")
    print(f"OK: ensured {summary}")
    print(f"OK: ensured {decision}")
    print(f"OK: ensured {run_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
