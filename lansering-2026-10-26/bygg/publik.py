# Publik utgåva: python3 -I bygg/publik.py i mappen lansering-2026-10-26. Skriver ../publik-2026-10-26/.
# Samma sidor som granskningsversionen, utan granskningsraden och utan interna sidor (intern.html, kontroll-*.html).
# Rör inga markeringar: prickade (bekrafta) och gula (forslag) påståenden rapporteras, så att de tas bort först när respektive uppgift är verifierad.
# Stoppar (exit 1) om MOTTAGNING är tom eller om en intern länk blivit kvar.
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemensamt import MOTTAGNING  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
UT = ROT.parent / "publik-2026-10-26"
SIDOR = ["index.html", "media.html", "funktioner.html", "priser.html", "om.html", "early-bird.html"]
STILAR_SKRIPT = ["site.css", "lansering.css", "funktioner.css", "priser.css", "om.css", "funktioner.js", "priser.js", "om.js", "early-bird.js", "funktioner.json"]

if not MOTTAGNING:
    sys.exit("STOPP: MOTTAGNING är tom.")
if UT.exists():
    shutil.rmtree(UT)
UT.mkdir()
shutil.copytree(ROT / "bilder", UT / "bilder")
for f in STILAR_SKRIPT:
    shutil.copy2(ROT / f, UT / f)

kvar = {}
for s in SIDOR:
    t = (ROT / s).read_text(encoding="utf-8")
    t, n = re.subn(r'<div class="skissrad">.*?</div>\n?', "", t, flags=re.S)
    if n != 1:
        sys.exit(f"STOPP: {s} saknar granskningsraden exakt en gång ({n}).")
    if re.search(r"intern\.html|kontroll-[a-z]+\.html|localhost|127\.0\.0\.1", t):
        sys.exit(f"STOPP: {s} har intern länk eller lokal adress.")
    (UT / s).write_text(t, encoding="utf-8")
    kvar[s] = (len(re.findall(r'class="bekrafta', t)), len(re.findall(r'class="[^"]*\bforslag\b', t)))

print(f"Publik utgåva i {UT}")
print("Kvarvarande markeringar (prickade, gula) per sida:")
for s, (b, f) in kvar.items():
    print(f"  {s}: {b}, {f}")
