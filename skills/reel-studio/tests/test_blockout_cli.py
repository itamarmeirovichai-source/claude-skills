"""blockout.py command line: --help and argument errors work (with or without Blender installed)."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "blockout.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=120)


def test_help_exits_zero_and_documents_options():
    r = run("--help")
    assert r.returncode == 0, r.stderr
    for opt in ("spec", "out", "--res", "--fps", "--preview"):
        assert opt in r.stdout


def test_bad_resolution_is_an_argument_error():
    r = run("spec.json", "out.mp4", "--res", "540by960")
    assert r.returncode == 2 and "540x960" in r.stderr


def test_missing_arguments_and_missing_spec(tmp_path):
    assert run().returncode == 2
    r = run(str(tmp_path / "nope.json"), str(tmp_path / "o.mp4"))
    assert r.returncode == 2 and "spec not found" in r.stderr
