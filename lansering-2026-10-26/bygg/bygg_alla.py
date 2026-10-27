# Bygger hela lanseringsversionen: python3 -I bygg/bygg_alla.py i mappen lansering-2026-10-26.
import subprocess
import sys
from pathlib import Path

HAR = Path(__file__).resolve().parent
for skript in ("bygg_start_media.py", "bygg_funktioner.py", "bygg_priser.py", "bygg_om.py", "bygg_early_bird.py", "bygg_betatest.py"):
    print("==", skript)
    r = subprocess.run([sys.executable, "-I", str(HAR / skript)])
    if r.returncode:
        sys.exit(r.returncode)
