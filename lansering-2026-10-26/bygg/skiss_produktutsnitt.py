# Skiss 2026-10-26: funktionssidan med ett läsbart produktutsnitt i fördjupningen för de funktioner som har ett
# utsnitt i utsnitt.py. Skriver en separat mapp, ../skiss-produktutsnitt-2026-10-26/, med samma sidor, stilar,
# skript och bilder som granskningsversionen, men funktioner.html byggd med SAEFUR_SKISS=1.
# Kör: python3 -I bygg/skiss_produktutsnitt.py   i mappen lansering-2026-10-26. Visa: PORT=5523 node server.mjs i skissmappen.
# Beskärningen görs med sips (macOS) ur bilder/prod-*.jpg enligt kalla, x, y, bredd, hojd i utsnitt.py, till bilder/utsnitt/.
import os
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utsnitt import UTSNITT  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
UT = ROT.parent / "skiss-produktutsnitt-2026-10-26"
SIDOR = ["index.html", "media.html", "priser.html", "om.html", "early-bird.html", "intern.html"]
FILER = ["site.css", "lansering.css", "funktioner.css", "priser.css", "om.css", "funktioner.js", "priser.js", "om.js", "early-bird.js", "server.mjs"]

# Utsnitt ur produktfångsterna
for fid, u in UTSNITT.items():
    kalla, mal = ROT / "bilder" / u["kalla"], ROT / "bilder" / "utsnitt" / u["fil"]
    assert kalla.is_file(), kalla
    subprocess.run(["sips", "-c", str(u["hojd"]), str(u["bredd"]), "--cropOffset", str(u["y"]), str(u["x"]),
                    str(kalla), "--out", str(mal)], check=True, capture_output=True)
    print(f"utsnitt {fid}: {mal.name} {u['bredd']}x{u['hojd']} ur {u['kalla']} vid {u['x']},{u['y']}")

# Skissmappen: tom, fylls på nytt
if UT.exists():
    shutil.rmtree(UT)
UT.mkdir()
shutil.copytree(ROT / "bilder", UT / "bilder")
for f in FILER + SIDOR:
    shutil.copy2(ROT / f, UT / f)

# funktioner.html med utsnitten, byggd av det ordinarie byggskriptet
os.environ["SAEFUR_SKISS"] = "1"
os.environ["SAEFUR_UT"] = str(UT)
runpy.run_path(str(ROT / "bygg" / "bygg_funktioner.py"), run_name="__main__")

# Granskningsraden i skissen pekar ut att det är skissen
for s in ["funktioner.html"]:
    t = (UT / s).read_text(encoding="utf-8")
    t = t.replace("Granskningsversion med lanseringslager, 25 oktober 2026 ·", "Skiss med produktutsnitt i fördjupningen, 26 oktober 2026 · jämför med granskningsversionen på 5520 ·", 1)
    (UT / s).write_text(t, encoding="utf-8")

(UT / "START.md").write_text(f"""# Skiss: produktutsnitt i fördjupningen, 2026-10-26

Separat skiss, byggd ur lanseringsversionen med `python3 -I bygg/skiss_produktutsnitt.py` (i `lansering-2026-10-26/`).
Enda skillnaden mot granskningsversionen är figurerna i de funktioner som har ett utsnitt i `bygg/utsnitt.py`:
{", ".join(f"`{k}`" for k in UTSNITT)}. Inget är publicerat.

## Visa

```
cd {UT}
PORT=5523 node server.mjs
```

Exempel: http://127.0.0.1:5523/funktioner.html?p=team&g=kontoret&q=leverans#faktura-ur-arbete
och http://127.0.0.1:5523/funktioner.html?p=team&g=material&q=leverans#plock-skanning

Jämför med granskningsversionen: http://127.0.0.1:5520/funktioner.html (samma adresser, utan utsnitt).
Utsnitten beskärs med sips ur `bilder/prod-*.jpg` (exempelföretaget Nordanå Kök & Inredning AB, demodata) till `bilder/utsnitt/`.
Mappen skrivs om vid varje bygge; ändra i `bygg/utsnitt.py`, `bygg/bygg_funktioner.py`, `funktioner.css` och `funktioner.js`.
""", encoding="utf-8")
print(f"Skiss i {UT}")
