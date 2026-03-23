from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "templates" / "experiment_project"
CORE_SKILLS = {
    "learn_baseline": ".agents/skills/learn-baseline/SKILL.md",
    "project_coach": ".agents/skills/project-coach/SKILL.md",
    "run_manager": ".agents/skills/run-manager/SKILL.md",
    "test_worker": ".agents/skills/test-worker/SKILL.md",
}
RUNTIME_BUNDLE_FILES = [
    "tools/main.py",
    "tools/app.py",
    "tools/project_config.py",
    "tools/common_helpers.py",
    "tools/result_schema.py",
    "tools/view.sh",
    "tools/init.py",
    "tools/gitclient.py",
    "tools/sync_tools.py",
    "core/schema_utils.py",
    "tests/run_gate.py",
]
RUNTIME_BUNDLE_SCHEMAS = [
    "clarified_job.schema.json",
    "corrected_job.schema.json",
    "task_plan.schema.json",
    "merge_result.schema.json",
    "learning_baseline_snapshot.schema.json",
    "test_worker_result.schema.json",
    "defect_triage_result.schema.json",
]


def slugify(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "experiment-project"


def render_template(text: str, project_id: str, project_name: str, project_root: str) -> str:
    return (
        text.replace("__PROJECT_ID__", project_id)
        .replace("__PROJECT_NAME__", project_name)
        .replace("__PROJECT_ROOT__", project_root)
    )


def write_if_missing(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def copy_file(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def get_git_commit() -> str | None:
    git_head = REPO_ROOT / ".git" / "HEAD"
    if not git_head.exists():
        return None
    head = git_head.read_text(encoding="utf-8").strip()
    if head.startswith("ref: "):
        ref = head.split(" ", 1)[1].strip()
        ref_path = REPO_ROOT / ".git" / ref
        if ref_path.exists():
            return ref_path.read_text(encoding="utf-8").strip() or None
        return None
    return head or None


def bootstrap(
    target_root: Path,
    project_name: str | None = None,
    with_core_skills: bool = False,
    with_runtime_bundle: bool = False,
) -> dict:
    target_root = target_root.resolve()
    project_name = project_name or target_root.name
    project_id = slugify(project_name)

    created_dirs = []
    created_files = []
    copied_runtime_files = []
    copied_schemas = []
    copied_skills = []

    required_dirs = [
        target_root / "docs",
        target_root / "tools",
        target_root / ".agents" / "skills",
        target_root / "schemas",
        target_root / "state",
        target_root / "reports",
        target_root / "artifacts",
        target_root / "logs",
    ]
    for directory in required_dirs:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(directory))

    template_map = {
        TEMPLATE_ROOT / "AGENTS.md.tmpl": target_root / "AGENTS.md",
        TEMPLATE_ROOT / "project_config.json.tmpl": target_root / "tools" / "project_config.json",
        TEMPLATE_ROOT / "docs" / "PROJECT_GUIDE.md.tmpl": target_root / "docs" / "PROJECT_GUIDE.md",
        TEMPLATE_ROOT / "docs" / "WORKFLOW.md.tmpl": target_root / "docs" / "WORKFLOW.md",
        TEMPLATE_ROOT / "docs" / "NEXT_STEPS.md.tmpl": target_root / "docs" / "NEXT_STEPS.md",
    }

    for src, dst in template_map.items():
        rendered = render_template(
            src.read_text(encoding="utf-8"),
            project_id=project_id,
            project_name=project_name,
            project_root=str(target_root),
        )
        if write_if_missing(dst, rendered):
            created_files.append(str(dst))

    config_path = target_root / "tools" / "project_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if with_core_skills:
        config["skills"] = dict(CORE_SKILLS)
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        for rel_path in CORE_SKILLS.values():
            src_skill_md = REPO_ROOT / rel_path
            skill_dir_name = src_skill_md.parent.name
            dst_dir = target_root / ".agents" / "skills" / skill_dir_name
            if not dst_dir.exists():
                shutil.copytree(src_skill_md.parent, dst_dir)
            copied_skills.append(str(dst_dir.relative_to(target_root)))

    if with_runtime_bundle:
        for rel_path in RUNTIME_BUNDLE_FILES:
            src = REPO_ROOT / rel_path
            dst = target_root / rel_path
            copy_file(src, dst)
            copied_runtime_files.append(rel_path)
        for schema_name in RUNTIME_BUNDLE_SCHEMAS:
            src = REPO_ROOT / "schemas" / schema_name
            dst = target_root / "schemas" / schema_name
            copy_file(src, dst)
            copied_schemas.append(f"schemas/{schema_name}")

    bootstrap_mode = "skeleton"
    if with_core_skills and with_runtime_bundle:
        bootstrap_mode = "runtime-bundle"
    elif with_core_skills:
        bootstrap_mode = "runnable"

    manifest = {
        "source_repo": str(REPO_ROOT),
        "source_commit": get_git_commit(),
        "bootstrap_mode": bootstrap_mode,
        "copied_skills": copied_skills,
        "copied_runtime_files": copied_runtime_files,
        "copied_schema_files": copied_schemas,
        "generated_at": target_root.stat().st_mtime if target_root.exists() else None,
    }
    manifest_path = target_root / "bootstrap_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    created_files.append(str(manifest_path))

    validation = {
        "docs_present": all((target_root / rel).exists() for rel in ["AGENTS.md", "docs/PROJECT_GUIDE.md", "docs/WORKFLOW.md"]),
        "skills_dir_present": (target_root / ".agents" / "skills").exists(),
        "schemas_dir_present": (target_root / "schemas").exists(),
        "state_dir_present": (target_root / "state").exists(),
        "project_config_parse_ok": isinstance(config, dict),
        "skills_non_empty": bool(config.get("skills")),
        "skills_paths_exist": all((target_root / rel).exists() for rel in config.get("skills", {}).values()) if config.get("skills") else False,
        "runtime_bundle_files_exist": all((target_root / rel).exists() for rel in copied_runtime_files) if with_runtime_bundle else True,
        "runtime_bundle_schemas_exist": all((target_root / rel).exists() for rel in copied_schemas) if with_runtime_bundle else True,
        "bootstrap_manifest_present": manifest_path.exists(),
    }

    return {
        "ok": all(validation.values()),
        "target_root": str(target_root),
        "project_id": project_id,
        "project_name": project_name,
        "bootstrap_mode": bootstrap_mode,
        "created_dirs": created_dirs,
        "created_files": created_files,
        "copied_skills": copied_skills,
        "copied_runtime_files": copied_runtime_files,
        "copied_schema_files": copied_schemas,
        "validation": validation,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target_root")
    parser.add_argument("--project-name", default=None)
    parser.add_argument("--with-core-skills", action="store_true")
    parser.add_argument("--with-runtime-bundle", action="store_true")
    args = parser.parse_args()

    result = bootstrap(
        Path(args.target_root),
        project_name=args.project_name,
        with_core_skills=args.with_core_skills,
        with_runtime_bundle=args.with_runtime_bundle,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
