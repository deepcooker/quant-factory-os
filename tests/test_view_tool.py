import os
import shutil
import stat
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VIEW_TOOL = REPO_ROOT / "tools" / "view.sh"
TMP_DIR = REPO_ROOT / ".tmp_test_view"


def run_cmd(*args, env=None):
    return subprocess.run(
        list(args),
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


class ViewToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TMP_DIR.mkdir(exist_ok=True)
        VIEW_TOOL.chmod(VIEW_TOOL.stat().st_mode | stat.S_IXUSR)

    @classmethod
    def tearDownClass(cls):
        if TMP_DIR.exists():
            shutil.rmtree(TMP_DIR)

    def test_direct_execution_and_python_invocation_both_work(self):
        sample = TMP_DIR / "sample.txt"
        sample.write_text("a\nb\nc\n", encoding="utf-8")

        direct = run_cmd(str(VIEW_TOOL), str(sample), "--from", "2", "--to", "3")
        py_call = run_cmd("python3", str(VIEW_TOOL), str(sample), "--from", "2", "--to", "3")

        self.assertEqual(direct.returncode, 0)
        self.assertEqual(py_call.returncode, 0)
        self.assertEqual(direct.stdout, "b\nc\n")
        self.assertEqual(py_call.stdout, "b\nc\n")

    def test_legacy_lines_argument_is_supported(self):
        sample = TMP_DIR / "legacy.txt"
        sample.write_text("1\n2\n3\n4\n", encoding="utf-8")

        result = run_cmd("python3", str(VIEW_TOOL), str(sample), "--lines", "2:3")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "2\n3\n")

    def test_find_and_context_return_line_numbers(self):
        sample = TMP_DIR / "find.txt"
        sample.write_text("zero\nalpha\nbeta\ngamma\n", encoding="utf-8")

        result = run_cmd(str(VIEW_TOOL), str(sample), "--find", "beta", "--context", "1")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "2\n3\n4\n")

    def test_blocks_paths_outside_repo(self):
        outside = Path("/tmp/view_tool_outside_repo.txt")
        outside.write_text("outside\n", encoding="utf-8")
        try:
            result = run_cmd("python3", str(VIEW_TOOL), str(outside), "--from", "1", "--to", "1")
            self.assertEqual(result.returncode, 1)
            self.assertIn("path must be inside repo root", result.stdout)
        finally:
            outside.unlink(missing_ok=True)

    def test_denylist_blocks_and_override_allows(self):
        sample = TMP_DIR / "blocked.txt"
        sample.write_text("blocked\n", encoding="utf-8")
        denylist = REPO_ROOT / ".codex_read_denylist"
        original = denylist.read_text(encoding="utf-8") if denylist.exists() else None
        try:
            denylist.write_text(".tmp_test_view/blocked.txt\n", encoding="utf-8")

            blocked = run_cmd(str(VIEW_TOOL), str(sample), "--from", "1", "--to", "1")
            self.assertEqual(blocked.returncode, 1)
            self.assertIn("blocked by .codex_read_denylist", blocked.stderr)

            env = os.environ.copy()
            env["CODEX_READ_DENYLIST_ALLOW"] = "1"
            allowed = run_cmd(
                "python3",
                str(VIEW_TOOL),
                str(sample),
                "--from",
                "1",
                "--to",
                "1",
                env=env,
            )
            self.assertEqual(allowed.returncode, 0)
            self.assertEqual(allowed.stdout, "blocked\n")
            self.assertIn("override enabled", allowed.stderr)
        finally:
            if original is None:
                denylist.unlink(missing_ok=True)
            else:
                denylist.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
