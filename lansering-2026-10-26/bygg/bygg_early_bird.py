# Early Bird-sidan och den interna översikten: python3 -I bygg/bygg_early_bird.py i mappen lansering-2026-10-26. 2026-10-25.
#
#   early-bird.html   erbjudandet, villkoren (Adams godkända text), formulär mot A:s mottagning, hur uppgifterna används
#   intern.html       intern översikt: sidor, kontrollsidor, anslutningens läge. Aldrig publik.
#
# Formuläret skickar bara till MOTTAGNING i gemensamt.py. Är adressen tom säger sidan öppet att anslutningen saknas och
# ingenting skickas eller sparas. Bekräftelse visas bara när mottagningen själv svarar att anmälan är mottagen.
# Villkorstexten är Adams godkända (25 okt natt) och står ordagrant; den undantas från språkkontrollen, eftersom
# "ingår inte" och "kan inte kombineras" är villkorets egna ord.
import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemensamt import LANSERING, EB, LOGIN, MOTTAGNING, BETATEST, INLOGG, huvud, sidfot, skissrad, FORETAG  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
# Texten och versionen (2026-10-25.1) är A:s i Hantis-main (launch.earlyBird.consent); A sparar versionen, webben skickar den inte.
SAMTYCKE = "När du anmäler dig sparar vi uppgifterna enligt nedan. En anmälan ger inte tillgång till systemet."

VILLKOR = [
    "20 % rabatt på grundproduktens licenser och extra användarlicenser i sex månader från första betalda abonnemangsperioden efter provperioden.",
    "Rabatten avser ordinarie licenspriser vid abonnemangsstart.",
    "Tillägg, tjänster och engångsavgifter ingår inte.",
    "Ett företag per anmälan.",
    "Abonnemanget ska starta inom 90 dagar efter lanseringsbeskedet.",
    "Kan inte kombineras med Founding Customer eller andra introduktionserbjudanden.",
    "Anmälan ger inte tillgång till betatestet.",  # 27 okt: pilot blev betatest i besökarens text, villkoret i sak oförändrat
]
villkor = "".join(f"<li>{v}</li>" for v in VILLKOR)

DATA = {"mottagning": MOTTAGNING}

sida = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Early Bird | SAEFUR</title>
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="lansering.css">
</head>
<body>
{skissrad()}
{huvud(EB)}

<main>
<section class="hero sida">
  <div class="wrap hero-text">
    <span class="markning">{LANSERING}</span>
    <h1>Få besked när<br><span>SAEFUR öppnar.</span></h1>
    <p class="lead">Anmäl ditt företag till Early Bird och få 20 % rabatt på licenserna i sex månader enligt villkoren nedan. Vi skickar en bekräftelse till din e-postadress och hör av oss när det går att börja.</p>
  </div>
</section>

<section class="sektion">
  <div class="wrap eb-grid">
    <div>
      <p class="etikett">Erbjudandet</p>
      <ol class="eb-tre">
        <li><b>20 % rabatt</b><span>på licenserna i sex månader.</span></li>
        <li><b>Från första betalda perioden</b><span>efter provperioden.</span></li>
        <li><b>Start inom 90 dagar</b><span>efter att vi har meddelat att SAEFUR öppnat.</span></li>
      </ol>
      <p class="not"><a class="textlank" href="#villkor">Alla villkor</a></p>
    </div>

    <form class="eb-form" id="eb-form" novalidate aria-labelledby="eb-rubrik">
      <h2 id="eb-rubrik">Anmäl ditt företag</h2>
      <p class="eb-ej-ansluten" id="eb-ej-ansluten" hidden>Anmälan är inte ansluten ännu. Formuläret skickar ingenting och ingenting sparas förrän mottagningen är på plats.</p>
      <div class="eb-falt">
        <label for="eb-epost">E-postadress</label>
        <input id="eb-epost" name="email" type="email" autocomplete="email" inputmode="email" required maxlength="254">
        <p class="eb-fel" id="eb-epost-fel" role="alert" hidden></p>
      </div>
      <div class="eb-falt">
        <label for="eb-foretag">Företagets namn <span class="frivilligt">(frivilligt)</span></label>
        <input id="eb-foretag" name="company" type="text" autocomplete="organization" maxlength="200">
      </div>
      <div class="eb-falt eb-fang" aria-hidden="true">
        <label for="eb-webb">Lämna tomt</label>
        <input id="eb-webb" name="website" type="text" tabindex="-1" autocomplete="off">
      </div>
      <p class="mikro eb-samtycke-text">{SAMTYCKE}</p>
      <button class="btn stor" type="submit" id="eb-skicka">Anmäl ditt företag</button>
      <div class="eb-status" id="eb-status" role="status" aria-live="polite" tabindex="-1" hidden></div>
      <p class="mikro">Redan med i betatestet? <a class="textlank" href="{LOGIN}">{INLOGG}</a></p>
    </form>
  </div>
</section>

<section class="sektion band" id="villkor">
  <div class="wrap eb-grid">
    <div>
      <p class="etikett">Villkor</p>
      <h2 class="rubrik">Early Bird i korthet.</h2>
    </div>
    <ul class="lista villkor">{villkor}</ul>
  </div>
</section>

<section class="sektion" id="uppgifter">
  <div class="wrap eb-grid">
    <div>
      <p class="etikett">Dina uppgifter</p>
      <h2 class="rubrik">Så används e-postadressen.</h2>
    </div>
    <div class="eb-text">
      <p>Vi sparar e-postadressen och, om du anger det, företagets namn. Vi använder dem enbart för att bekräfta anmälan, meddela när SAEFUR öppnar och ge företaget rabatten.</p>
      <p>Efter anmälan skickar vi ett mejl till adressen du angav. Bekräfta anmälan med länken i mejlet, så gäller den. Vill du bli borttagen räcker ett mejl till info@saefur.com.</p>
      <p><span data-p="gallring">En anmälan som inte bekräftas raderas efter 30 dagar. Har du bekräftat och inte blivit kund raderas den 120 dagar efter att vi har skickat lanseringsbeskedet till dig. Blir du kund raderas anmälan när rabattperioden är slut och rabatten är korrekt registrerad. Ditt kundkonto och dina bokföringsuppgifter berörs inte.</span></p>
      <p class="not">Personuppgiftsansvarig: {FORETAG}.</p>
    </div>
  </div>
</section>

<section class="sektion band" id="betatest">
  <div class="wrap eb-grid">
    <div>
      <p class="etikett">Betatest</p>
      <h2 class="rubrik">Vill ni börja före lanseringen?</h2>
    </div>
    <div class="eb-text">
      <p>Före lanseringen väljer vi ut ett fåtal företag från olika branscher och med olika antal anställda som börjar använda SAEFUR i sitt arbete. De får hjälp att komma igång, stöd kring integrationer och möjlighet att lämna synpunkter som påverkar utvecklingen.</p>
      <p>Betatestet är ett eget erbjudande med en egen intresseanmälan. <a class="textlank" href="{BETATEST}">Läs om betatestet</a></p>
    </div>
  </div>
</section>
</main>

{sidfot()}
<script id="data" type="application/json">{json.dumps(DATA, ensure_ascii=False)}</script>
<script src="early-bird.js"></script>
</body>
</html>
'''
(ROT / "early-bird.html").write_text(sida, encoding="utf-8")

# Språkkontroll av den publika sidan (text utanför taggar), utom villkorstexten
FORBJUDET = (" inte ", "faktisk", "riktig", "verklig", "skav", "—", "–", "personal")
publik = re.sub(r"<script.*?</script>", "", sida, flags=re.S)
publik = re.sub(r'<ul class="lista villkor">.*?</ul>', "", publik, flags=re.S)
publik = re.sub(r'<p class="eb-ej-ansluten".*?</p>', "", publik, flags=re.S)  # statusmeddelandet är en systemtext, inte marknadstext
publik = re.sub(r"<[^>]+>", " ", publik).lower()
varningar = [f for f in FORBJUDET if f in publik]
if varningar:
    print("VARNING, publik text innehåller:", varningar)
if not MOTTAGNING:
    print("OBS: MOTTAGNING är tom. Formuläret skickar ingenting. Ansluts när A:s adress är bekräftad av Tobbe.")

# ---------- Intern översikt ----------
sidor = [("index.html", "Start"), ("funktioner.html", "Funktioner (5515)"), ("media.html", "Media"), ("priser.html", "Priser (5516)"),
         ("om.html", "Om SAEFUR (5517)"), ("early-bird.html", "Early Bird (ny)"), ("betatest.html", "Betatest (27 okt, intresseanmälan via e-post)")]
kontroll = [("kontroll-funktioner.html", "Funktioner mot förmågekartan"), ("kontroll-priser.html", "Priser, påstående för påstående"),
            ("kontroll-om.html", "Om SAEFUR, påstående för påstående")]
anslutning = (f"<code>{MOTTAGNING}</code>" if MOTTAGNING else "<b>Saknas.</b> Formuläret skickar ingenting och säger det öppet.")
intern = f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Intern översikt: lansering</title>
<style>
body{{font:15px/1.55 -apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;margin:32px;color:#1b2537;background:#f5f6f8;max-width:920px}}
h1{{margin:0 0 8px}} h2{{margin:32px 0 10px;font-size:19px}} code{{background:#eef1f6;padding:2px 6px;border-radius:6px;font-size:13px}} li{{margin:5px 0}}
</style></head><body>
<h1>Intern översikt: lanseringsversionen</h1>
<p>Aldrig publik. Lokal granskningsversion 25 oktober 2026. De godkända mapparna (v4, 5515, 5516, 5517) är orörda; här finns kopior med lanseringslagret.</p>
<h2>Sidor</h2>
<ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in sidor)}</ul>
<h2>Kontrollsidor</h2>
<ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in kontroll)}</ul>
<h2>Anslutning till A:s mottagning</h2>
<p>Adress i <code>bygg/gemensamt.py</code> (<code>MOTTAGNING</code>): {anslutning}</p>
<p>Gränssnittet webben förväntar sig, publiceringsförslaget och frågorna till Tobbe och A står i <code>../09_publicering_och_anslutning.md</code> (i innehållsförslagsmappen).</p>
<h2>Prickat och öppet på Early Bird-sidan</h2>
<ul>
<li>Gallring: principen är godkänd av Adam (30 dagar obekräftad, 120 dagar efter skickat lanseringsbesked, kund efter avslutad och korrekt registrerad rabattperiod). Gallringen är byggd hos A (DEC-454, belägg per anmälan) men inte driftsatt; texten är prickad tills den är det. Kundregeln kan inte uppfyllas förrän Early Bird-rabatten är byggd. Se <code>../innehallsforslag-2026-10-25/10_radering_och_anslutning_med_A.md</code>.</li>
<li>Samtyckestexten och dess version är A:s (<code>2026-10-25.1</code>); webben skickar ingen version.</li>
</ul>
</body></html>
'''
(ROT / "intern.html").write_text(intern, encoding="utf-8")
print("Byggt early-bird.html och intern.html")
