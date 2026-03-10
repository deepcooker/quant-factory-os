#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TextIO

try:
    from tools.project_config import load_project_config, load_runtime_state
except Exception:  # pragma: no cover
    from project_config import load_project_config, load_runtime_state  # type: ignore


PROJECT_CONFIG = load_project_config()
DEFAULT_STEPS = ["init", "learn", "ready"]
ALL_STEPS = ["init", "learn", "ready", "orient", "choose", "council", "arbiter", "slice_task"]


@dataclass
class StepSpec:
    name: str
    command: list[str]
    note: str


class StepFailure(RuntimeError):
    """Raised when one orchestrated subprocess exits non-zero."""


class Logger:
    """Mirror every log line to stdout and to the run-scoped log file."""

    # 9001 中文：初始化统一日志器并打开 run 级日志文件。
    def __init__(self, log_file: Path) -> None:
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._fp = self.log_file.open("a", encoding="utf-8")
        self._lock = threading.Lock()

    # 9002 中文：关闭统一日志器文件句柄。
    def close(self) -> None:
        self._fp.close()

    # 9003 中文：输出单条统一格式日志。
    def _emit(self, level: str, message: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        line = f"{ts} | {level:<5} | {message}"
        with self._lock:
            print(line)
            self._fp.write(line + "\n")
            self._fp.flush()

    # 9004 中文：输出 INFO 级统一日志。
    def info(self, message: str) -> None:
        self._emit("INFO", message)

    # 9005 中文：输出 ERROR 级统一日志。
    def error(self, message: str) -> None:
        self._emit("ERROR", message)


# 9007 中文：解析总入口使用的 run_id。
def resolve_run_id(explicit: str) -> str:
    if explicit.strip():
        return explicit.strip()
    return load_runtime_state().current_run_id or f"run-{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}"


# 9008 中文：解析总入口使用的 project_id。
def resolve_project_id(explicit: str) -> str:
    if explicit.strip():
        return explicit.strip()
    return load_runtime_state().current_project_id or PROJECT_CONFIG.project_id


# 9009 中文：解析总入口要执行的步骤列表。
def parse_steps(raw: str) -> list[str]:
    value = raw.strip().lower()
    if not value or value == "default":
        return list(DEFAULT_STEPS)
    if value == "all":
        return list(ALL_STEPS)
    steps = [item.strip() for item in value.split(",") if item.strip()]
    unknown = [item for item in steps if item not in ALL_STEPS]
    if unknown:
        raise SystemExit(f"ERROR: unknown steps: {', '.join(unknown)}")
    return steps


# 9010 中文：把逻辑步骤翻译成具体 tools 命令。
def build_step_specs(args: argparse.Namespace, run_id: str, project_id: str) -> list[StepSpec]:
    """Map logical pipeline steps to concrete tools commands."""
    specs: list[StepSpec] = []
    for step in args.steps:
        if step == "init":
            specs.append(StepSpec("init", ["python3", "tools/init.py"], "diagnose workspace"))
        elif step == "learn":
            specs.append(StepSpec("learn", ["python3", "tools/learn.py", args.learn_profile], "sync project cognition"))
        elif step == "ready":
            specs.append(StepSpec("ready", ["python3", "tools/ready.py", f"RUN_ID={run_id}"], "gate the active run"))
        elif step == "orient":
            specs.append(StepSpec("orient", ["python3", "tools/orient.py", f"RUN_ID={run_id}", f"PROJECT_ID={project_id}"], "draft direction options"))
        elif step == "choose":
            if not args.choose_option:
                raise SystemExit("ERROR: step 'choose' requires --choose-option")
            specs.append(
                StepSpec(
                    "choose",
                    ["python3", "tools/choose.py", f"RUN_ID={run_id}", f"PROJECT_ID={project_id}", f"OPTION={args.choose_option}"],
                    "confirm a direction option",
                )
            )
        elif step == "council":
            specs.append(StepSpec("council", ["python3", "tools/council.py", f"RUN_ID={run_id}", f"PROJECT_ID={project_id}"], "run multi-role review"))
        elif step == "arbiter":
            specs.append(StepSpec("arbiter", ["python3", "tools/arbiter.py", f"RUN_ID={run_id}", f"PROJECT_ID={project_id}"], "converge execution contract"))
        elif step == "slice_task":
            specs.append(StepSpec("slice_task", ["python3", "tools/slice_task.py", f"RUN_ID={run_id}", f"PROJECT_ID={project_id}"], "write slice tasks"))
    return specs


# 9011 中文：逐行读取子进程输出并转成统一日志。
def stream_reader(stream: TextIO, logger: Logger, step_name: str, channel: str) -> None:
    """Forward every stdout/stderr line from a child process into the logger."""
    for raw in iter(stream.readline, ""):
        line = raw.rstrip("\n")
        logger.info(f"STEP_LINE[{step_name}][{channel}] {line if line else '<empty>'}")
    stream.close()


# 9012 中文：执行单个步骤并记录开始、结束、失败与逐行输出。
def run_step(spec: StepSpec, logger: Logger, dry_run: bool) -> None:
    """Run one step with start/end/fail logging plus per-line child output logging."""
    rendered = " ".join(spec.command)
    logger.info(f"STEP_START[{spec.name}] note={spec.note}")
    logger.info(f"STEP_CMD[{spec.name}] {rendered}")
    if dry_run:
        logger.info(f"STEP_SKIP[{spec.name}] dry-run=true")
        logger.info(f"STEP_DONE[{spec.name}] rc=0 dry-run=true")
        return

    process = subprocess.Popen(
        spec.command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert process.stdout is not None
    assert process.stderr is not None
    stdout_thread = threading.Thread(target=stream_reader, args=(process.stdout, logger, spec.name, "stdout"))
    stderr_thread = threading.Thread(target=stream_reader, args=(process.stderr, logger, spec.name, "stderr"))
    stdout_thread.start()
    stderr_thread.start()
    rc = process.wait()
    stdout_thread.join()
    stderr_thread.join()
    if rc != 0:
        logger.error(f"STEP_FAIL[{spec.name}] rc={rc}")
        raise StepFailure(f"{spec.name} failed with rc={rc}")
    logger.info(f"STEP_DONE[{spec.name}] rc=0")


# 9013 中文：构建总入口命令行解析器。
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified Python entrypoint for the tools pipeline.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run selected tools steps with unified logging.")
    run.add_argument("--run-id", default="", help="Explicit RUN_ID override.")
    run.add_argument("--project-id", default="", help="Explicit PROJECT_ID override.")
    run.add_argument("--steps", default="default", help="Comma list of steps or one of: default, all.")
    run.add_argument("--choose-option", default="", help="OPTION value for the choose step.")
    run.add_argument(
        "--learn-profile",
        default="-daily",
        choices=["-minimal", "-low", "-medium", "-high", "-xhigh", "-daily"],
        help="Reasoning profile passed to tools/learn.py.",
    )
    run.add_argument("--dry-run", action="store_true", help="Log commands without executing them.")
    run.add_argument("--log-file", default="", help="Explicit log file path.")
    return parser


# 9014 中文：执行总入口主流程，顺序编排各 tools 步骤。
def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "run":
        return 2

    args.steps = parse_steps(args.steps)
    run_id = resolve_run_id(args.run_id)
    project_id = resolve_project_id(args.project_id)
    log_file = Path(args.log_file) if args.log_file else Path(f"reports/{run_id}/orchestrator.log")
    logger = Logger(log_file)
    try:
        logger.info(f"ORCH_START run_id={run_id} project_id={project_id}")
        logger.info(f"ORCH_STEPS {','.join(args.steps)}")
        logger.info(f"ORCH_LOG_FILE {log_file}")
        for spec in build_step_specs(args, run_id, project_id):
            run_step(spec, logger, args.dry_run)
        logger.info("ORCH_DONE rc=0")
        return 0
    except StepFailure as exc:
        logger.error(f"ORCH_ABORT {exc}")
        return 1
    finally:
        logger.close()


if __name__ == "__main__":
    raise SystemExit(main())
