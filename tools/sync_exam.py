#!/usr/bin/env python3
"""
Sync learning exam grader for both Codex CLI and web GPT onboarding.

Design goal:
- Test thought-layer alignment and actionable continuity, not rote Q/A.
- Produce deterministic pass/fail output with auditable details.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_RUBRIC = Path("SYNC/EXAM_RUBRIC.json")


@dataclass
class CheckResult:
    check_id: str
    title: str
    passed: bool
    weight: int
    reason: str
    section: str


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise ValueError(f"invalid json root in {path}")
    return obj


def parse_sections(md_text: str) -> dict[str, str]:
    """
    Parse markdown sections by `## <title>`.
    """
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw in md_text.splitlines():
        line = raw.rstrip("\n")
        m = re.match(r"^\s*##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return ""


def check_text(section_text: str, spec: dict[str, Any]) -> tuple[bool, str]:
    min_len = int(spec.get("min_len", 1))
    if len(section_text.strip()) < min_len:
        return False, f"section too short (<{min_len})"

    keywords = [str(x) for x in spec.get("keywords", [])]
    if not keywords:
        return True, "ok"

    keyword_mode = str(spec.get("keyword_mode", "any")).lower()
    lower_text = section_text.lower()
    hits = [k for k in keywords if k.lower() in lower_text]
    if keyword_mode == "all":
        if len(hits) != len(keywords):
            missing = [k for k in keywords if k not in hits]
            return False, f"missing keywords: {', '.join(missing)}"
        return True, "ok"

    if not hits:
        return False, f"missing any keyword from: {', '.join(keywords)}"
    return True, "ok"


def check_command(section_text: str, spec: dict[str, Any]) -> tuple[bool, str]:
    line = first_nonempty_line(section_text)
    if not line:
        return False, "empty command"

    line = re.sub(r"^[-*]\s*", "", line).strip()
    line = re.sub(r"^(命令|command)\s*[:：]\s*", "", line, flags=re.IGNORECASE).strip()
    line = line.strip("`").strip()

    patterns = [str(x) for x in spec.get("patterns", [])]
    if not patterns:
        patterns = [r"^(tools/|\.\/tools/|make )"]
    for pat in patterns:
        if re.search(pat, line):
            return True, "ok"
    return False, f"command does not match expected patterns: {line}"


def evaluate(answer_sections: dict[str, str], rubric: dict[str, Any]) -> dict[str, Any]:
    checks = rubric.get("checks", [])
    if not isinstance(checks, list) or not checks:
        raise ValueError("rubric checks is empty")

    pass_score = int(rubric.get("pass_score", 80))
    results: list[CheckResult] = []
    total_weight = 0
    gained_weight = 0
    hard_failed = False

    for spec in checks:
        check_id = str(spec["id"])
        title = str(spec.get("title", check_id))
        section = str(spec["section"])
        check_type = str(spec.get("type", "text"))
        required = bool(spec.get("required", True))
        weight = int(spec.get("weight", 10))

        total_weight += weight
        section_text = answer_sections.get(section, "").strip()
        if not section_text:
            passed = False
            reason = "missing section"
        elif check_type == "command":
            passed, reason = check_command(section_text, spec)
        else:
            passed, reason = check_text(section_text, spec)

        if passed:
            gained_weight += weight
        if required and not passed:
            hard_failed = True

        results.append(
            CheckResult(
                check_id=check_id,
                title=title,
                passed=passed,
                weight=weight,
                reason=reason,
                section=section,
            )
        )

    score = 0.0
    if total_weight > 0:
        score = round((gained_weight / total_weight) * 100.0, 2)

    failed_checks = [
        {
            "id": r.check_id,
            "title": r.title,
            "section": r.section,
            "weight": r.weight,
            "reason": r.reason,
        }
        for r in results
        if not r.passed
    ]

    passed = (score >= pass_score) and (not hard_failed)
    return {
        "passed": passed,
        "score": score,
        "pass_score": pass_score,
        "total_weight": total_weight,
        "gained_weight": gained_weight,
        "failed_checks": failed_checks,
        "checks": [
            {
                "id": r.check_id,
                "title": r.title,
                "section": r.section,
                "passed": r.passed,
                "weight": r.weight,
                "reason": r.reason,
            }
            for r in results
        ],
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Grade sync learning exam answers.")
    p.add_argument("--answer-file", required=True, help="Answer markdown file path.")
    p.add_argument(
        "--rubric-file",
        default=str(DEFAULT_RUBRIC),
        help="Rubric json file path. Default: SYNC/EXAM_RUBRIC.json",
    )
    p.add_argument(
        "--output-file",
        default="",
        help="Optional output json file path. If omitted, prints only.",
    )
    p.add_argument("--run-id", default="", help="Optional RUN_ID to include in output.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    answer_file = Path(args.answer_file)
    rubric_file = Path(args.rubric_file)

    if not answer_file.exists():
        print(f"ERROR: answer file not found: {answer_file}", file=sys.stderr)
        return 2
    if not rubric_file.exists():
        print(f"ERROR: rubric file not found: {rubric_file}", file=sys.stderr)
        return 2

    try:
        rubric = load_json(rubric_file)
        answer_sections = parse_sections(answer_file.read_text(encoding="utf-8"))
        result = evaluate(answer_sections, rubric)
    except Exception as e:  # pragma: no cover
        print(f"ERROR: grading failed: {e}", file=sys.stderr)
        return 2

    payload = {
        "schema": "sync_exam_result.v1",
        "run_id": args.run_id or "",
        "answer_file": str(answer_file),
        "rubric_file": str(rubric_file),
        **result,
    }

    print(f"SYNC_EXAM_PASS: {str(payload['passed']).lower()}")
    print(f"SYNC_EXAM_SCORE: {payload['score']}")
    if payload["failed_checks"]:
        print("SYNC_EXAM_FAILED_CHECKS:")
        for item in payload["failed_checks"]:
            print(f"- {item['id']}: {item['reason']}")

    if args.output_file:
        out = Path(args.output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"SYNC_EXAM_OUTPUT: {out}")

    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
