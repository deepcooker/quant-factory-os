import subprocess
import tempfile
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_view_find(path: Path, pattern: str, context: int = 0):
    cmd = ["tools/view.sh", str(path), "--find", pattern, "--context", str(context)]
    return subprocess.run(cmd, text=True, capture_output=True)


def write_repo_sample(content: str) -> Path:
    root = repo_root()
    tmp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete=False, dir=root
    )
    try:
        tmp.write(content)
        tmp.flush()
        return Path(tmp.name)
    finally:
        tmp.close()


def test_view_find_hits():
    sample = write_repo_sample("alpha\nbravo\ncharlie\nbravo\n")

    try:
        result = run_view_find(sample, "bravo")
    finally:
        sample.unlink(missing_ok=True)

    assert result.returncode == 0
    assert result.stdout.strip().splitlines() == ["2", "4"]


def test_view_find_miss():
    sample = write_repo_sample("alpha\nbravo\ncharlie\n")

    try:
        result = run_view_find(sample, "delta")
    finally:
        sample.unlink(missing_ok=True)

    assert result.returncode == 1
    assert "No matches for pattern" in result.stdout
