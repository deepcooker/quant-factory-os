#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
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
    return json.loads(run_summary_path.read_text(encoding="utf-8"))


def _save_run_summary(run_summary_path: Path, payload: dict[str, Any]) -> None:
    payload["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_summary_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _get_reports_dir(repo: Path, run_id: str) -> Path:
    reports_dir = repo / "reports" / run_id
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--run-summary", action="store_true")
    ap.add_argument("--set-run-summary", action="store_true")
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
