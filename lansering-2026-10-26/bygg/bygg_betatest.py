# Betatestsidan: python3 -I bygg/bygg_betatest.py i mappen lansering-2026-10-26. 2026-10-27 (Adams uppdrag).
#
#   betatest.html   vad betatestet är, vad som ingår, omfattningen och hur man anmäler intresse
#
# Det finns ingen mottagning för betatestanmälan i produkten (Early Bird-mottagningen tar bara e-post, företagsnamn och
# källa, och portalen ger pilotgodkännande per adress). Intresseanmälan går därför som ett mejl till info@saefur.com,
# skrivet i besökarens eget e-postprogram. Sidan säger att anmälan är skickad först när mejlet är skickat; ingenting
# sparas av sidan. Ett formulär med urval kräver ett tekniskt uppdrag hos A (se sprakgranskning/LOGG.md, 27 okt).
# Early Bird är ett separat erbjudande. Om betatestanmälan också ska ge Early Bird väntar på Adams beslut.
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemensamt import EB, LOGIN, INLOGG, BETATEST, huvud, sidfot, skissrad, FORETAG  # noqa: E402

ROT = Path(__file__).resolve().parent.parent

INGAR = [
    ("Hjälp att komma igång", "Vi går igenom upplägget med er och hjälper er att lägga upp företaget, användarna och de första kunderna."),
    ("Stöd kring integrationer", "Vi hjälper er med de anslutningar som finns i dag, som underlaget till redovisningsbyrån, och berättar vilka som är på väg."),
    ("Synpunkter som påverkar utvecklingen", "Ni lämnar synpunkter direkt till oss som utvecklar SAEFUR, och vi väger in dem när vi prioriterar."),
    ("Nära kontakt", "Ni når oss på info@saefur.com, och vi stämmer av med er hur arbetet går under betatestet."),
]
OMFATTNING = [
    "Betatestet gäller SAEFUR som standardprodukt. Vi hjälper er att välja inställningar och områden som passar ert arbetssätt.",
    "Era synpunkter vägs in i den gemensamma produkten, som alla företag använder. Lösningar som byggs för ett enskilt företag ingår inte.",
    "Anslutningar till bank och transportör väntar på avtal och beskrivs som planerade tills de är på plats.",
    "Platserna är få. Vi väljer företag så att olika branscher och storlekar finns med, och kontaktar dem som väljs ut.",
]
UPPGIFTER = ["Företagets namn och bransch", "Hur många ni är i företaget", "Vad ni vill använda SAEFUR till", "Vilka system ni använder i dag"]

AMNE = "Intresseanmälan till betatestet"
KROPP = "\n".join([
    "Hej SAEFUR,", "", "Vi vill anmäla intresse för betatestet.", "",
    "Företagets namn:", "Bransch:", "Antal i företaget:", "Det vi vill använda SAEFUR till:", "System vi använder i dag:",
    "Kontaktperson och telefon:", "",
])
MAILTO = f"mailto:info@saefur.com?subject={quote(AMNE)}&body={quote(KROPP)}"

ingar = "".join(f"<li><b>{h}</b><span>{t}</span></li>" for h, t in INGAR)
omfattning = "".join(f"<li>{t}</li>" for t in OMFATTNING)
uppgifter = "".join(f"<li>{t}</li>" for t in UPPGIFTER)

sida = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Betatest | SAEFUR</title>
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="lansering.css">
</head>
<body>
{skissrad(' · intresseanmälan via e-post, ingen mottagning i produkten')}
{huvud(BETATEST)}

<main>
<section class="hero sida">
  <div class="wrap hero-text">
    <span class="markning">Före lanseringen</span>
    <h1>Börja tidigt<br><span>med nära stöd.</span></h1>
    <p class="lead">Före lanseringen väljer vi ut ett fåtal företag som börjar använda SAEFUR i sitt arbete. Vi vill ha med företag från olika branscher och med olika antal anställda. De som väljs ut får hjälp att komma igång, och deras synpunkter påverkar hur SAEFUR utvecklas.</p>
  </div>
</section>

<section class="sektion">
  <div class="wrap eb-grid">
    <div>
      <p class="etikett">Det här ingår</p>
      <ol class="eb-tre">{ingar}</ol>
    </div>

    <div class="eb-form" id="anmal" role="region" aria-labelledby="bt-rubrik">
      <h2 id="bt-rubrik">Anmäl intresse</h2>
      <div class="eb-text">
        <p>Skriv till info@saefur.com och berätta kort om företaget:</p>
      </div>
      <ul class="lista">{uppgifter}</ul>
      <a class="btn stor" href="{MAILTO}">Skriv en intresseanmälan</a>
      <p class="mikro">Knappen öppnar ett mejl i ditt e-postprogram med frågorna ifyllda. Anmälan är skickad när du har skickat mejlet.</p>
      <p class="mikro">Vi använder uppgifterna i mejlet för urvalet till betatestet och för att kontakta er. Personuppgiftsansvarig: {FORETAG}.</p>
      <p class="mikro">Redan med i betatestet? <a class="textlank" href="{LOGIN}">{INLOGG}</a></p>
    </div>
  </div>
</section>

<section class="sektion band" id="omfattning">
  <div class="wrap eb-grid">
    <div>
      <p class="etikett">Omfattning</p>
      <h2 class="rubrik">Så långt räcker betatestet.</h2>
    </div>
    <ul class="lista">{omfattning}</ul>
  </div>
</section>

<section class="sektion" id="early-bird">
  <div class="wrap eb-grid">
    <div>
      <p class="etikett">Early Bird</p>
      <h2 class="rubrik">Ett eget erbjudande.</h2>
    </div>
    <div class="eb-text">
      <p>Early Bird är för er som vill få besked när SAEFUR öppnar. Som Early Bird får företaget 20 % rabatt på licenserna i sex månader enligt villkoren. Anmälan till Early Bird görs separat.</p>
      <p><a class="textlank" href="{EB}">Early Bird, villkor och anmälan</a></p>
    </div>
  </div>
</section>
</main>

{sidfot()}
</body>
</html>
'''
(ROT / "betatest.html").write_text(sida, encoding="utf-8")

# Språkkontroll av den publika sidan (text utanför taggar). "ingår inte" i omfattningen är en nödvändig avgränsning.
FORBJUDET = ("faktisk", "riktig", "verklig", "skav", "—", "–", "personal", "pilot")
publik = re.sub(r"<script.*?</script>", "", sida, flags=re.S)
publik = re.sub(r"<[^>]+>", " ", publik).lower()
varningar = [f for f in FORBJUDET if f in publik]
if varningar:
    print("VARNING, publik text innehåller:", varningar)
print("Byggt betatest.html")
