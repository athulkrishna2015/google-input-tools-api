import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import inputtools


def test_convert_malayalam():
    c = inputtools.convert("namaskaram", itc="ml-t-i0-und", num=3)
    assert c.top is not None
    assert "നമസ്കാരം" in c.candidates
    assert len(c.candidates) >= 1


def test_itc_for():
    assert inputtools.itc_for("hindi") == "hi-t-i0-und"
    assert inputtools.itc_for("chinese") == "pinyin"
    assert inputtools.itc_for("ml-t-i0-und") == "ml-t-i0-und"


def test_cli_top():
    r = subprocess.run([str(ROOT / "inputtools"), "ente", "pere"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "എന്റെ" in r.stdout


def test_cli_all():
    r = subprocess.run([str(ROOT / "inputtools"), "-a", "-n", "2", "namaskaram"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    assert len(lines) >= 2


def test_cli_lang():
    r = subprocess.run([str(ROOT / "inputtools"), "--lang", "hindi", "namaste"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "नमस्ते" in r.stdout


def test_server():
    proc = subprocess.Popen([sys.executable, str(ROOT / "server.py")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    try:
        with urllib.request.urlopen("http://localhost:8080/health", timeout=5) as r:
            assert json.loads(r.read())["status"] == "ok"
        with urllib.request.urlopen("http://localhost:8080/convert?text=namaste&lang=hindi", timeout=10) as r:
            data = json.loads(r.read())
            assert data["top"] == "नमस्ते"
        # POST
        req = urllib.request.Request(
            "http://localhost:8080/convert",
            data=json.dumps({"text": "namaskaram", "lang": "malayalam", "num": 2}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            assert "നമസ്കാരം" in data["candidates"]
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    # run as simple script
    tests = [test_convert_malayalam, test_itc_for, test_cli_top, test_cli_all, test_cli_lang, test_server]
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as e:
            print("FAIL", t.__name__, "::", repr(e))
            sys.exit(1)
    print("ALL TESTS PASSED")
