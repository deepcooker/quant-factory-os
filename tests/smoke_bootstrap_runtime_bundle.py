from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FILES = [
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
SCHEMA_FILES = [
    "schemas/clarified_job.schema.json",
    "schemas/corrected_job.schema.json",
    "schemas/task_plan.schema.json",
    "schemas/merge_result.schema.json",
    "schemas/learning_baseline_snapshot.schema.json",
    "schemas/test_worker_result.schema.json",
    "schemas/defect_triage_result.schema.json",
]


def main() -> None:
    target = Path("/tmp/demo-bootstrap-runtime-bundle")
    if target.exists():
        shutil.rmtree(target)

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/bootstrap_experiment_project.py",
            str(target),
            "--with-core-skills",
            "--with-runtime-bundle",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr

    result = json.loads(proc.stdout)
    assert result["ok"] is True
    assert result["bootstrap_mode"] == "runtime-bundle"
    assert result["validation"]["skills_non_empty"] is True
    assert result["validation"]["skills_paths_exist"] is True
    assert result["validation"]["runtime_bundle_files_exist"] is True
    assert result["validation"]["runtime_bundle_schemas_exist"] is True
    assert result["validation"]["bootstrap_manifest_present"] is True

    for rel in RUNTIME_FILES:
        assert (target / rel).exists(), rel

    for rel in SCHEMA_FILES:
        assert (target / rel).exists(), rel

    manifest = json.loads((target / "bootstrap_manifest.json").read_text(encoding="utf-8"))
    assert manifest["bootstrap_mode"] == "runtime-bundle"
    assert set(manifest["copied_runtime_files"]) == set(RUNTIME_FILES)
    assert set(manifest["copied_schema_files"]) == set(SCHEMA_FILES)
    assert manifest["copied_skills"]

    config = json.loads((target / "tools" / "project_config.json").read_text(encoding="utf-8"))
    assert config["skills"]
    print("SMOKE_BOOTSTRAP_RUNTIME_BUNDLE_OK")


if __name__ == "__main__":
    main()
