import os
import subprocess
import sys
import tempfile


def run_a9(args):
    return subprocess.run(
        [sys.executable, "tools/run_a9.py", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_run_a9_fails_when_root_missing():
    missing = os.path.join(tempfile.gettempdir(), "a9_missing_dir_zzz")
    run_id = "run-test-a9-missing"
    res = run_a9(["--run-id", run_id, "--a9-root", missing])
    assert res.returncode != 0
    assert "a9 root not found" in (res.stdout + res.stderr)
    log_path = os.path.join("reports", run_id, "a9_stdout.log")
    assert os.path.exists(log_path)
    os.remove(log_path)
    try:
        os.rmdir(os.path.join("reports", run_id))
    except OSError:
        pass


def test_run_a9_succeeds_with_temp_root():
    run_id = "run-test-a9-ok"
    with tempfile.TemporaryDirectory() as temp_root:
        os.makedirs(os.path.join(temp_root, "dummy"), exist_ok=True)
        res = run_a9(["--run-id", run_id, "--a9-root", temp_root])
        assert res.returncode == 0, res.stderr
        log_path = os.path.join("reports", run_id, "a9_stdout.log")
        assert os.path.exists(log_path)
        with open(log_path, "r", encoding="utf-8") as handle:
            content = handle.read()
        assert "a9-root" in content
        os.remove(log_path)
        try:
            os.rmdir(os.path.join("reports", run_id))
        except OSError:
            pass
