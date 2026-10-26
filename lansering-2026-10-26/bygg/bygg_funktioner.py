# Bygger prototypen Funktioner med tre perspektiv: python3 -I bygg.py (i mappen prototyp-perspektiv).
# Innehåll: formagor_publika.py (149 funktioner, kopia av innehållsförslagets data) och perspektiv.py
# (tre perspektiv med grupper, ingresser och flöden). Skriver:
#   funktioner.html   besökarens sida, utan utvecklingsstatus, FM-källor och interna noter
#   kontroll.html     intern kontrollsida: status, FM-källa, not och grupp per perspektiv för varje rad
#   funktioner.json   samma data maskinläsbart
# Kopia av 5515 (godkänd och låst) med lanseringslagret, 25 okt 2026: python3 -I bygg/bygg_funktioner.py i mappen lansering-2026-10-26.
# Sidhuvud och sidfot kommer från gemensamt.py. Inget är publicerat.
#
# Sök och navigering omgjorda 26 okt 2026 (Adams uppdrag via Codex, med mandat att gå ett steg längre):
#   - ett enda perspektivval i en sticky banner direkt under sökningen, med hjälprad och gemensam undertext;
#     de tre stora perspektivkorten och den upprepade knappraden är borta
#   - sökträffarna som en avgränsad panel under sökfältet, grupperade per område i valt perspektiv
#   - bannern bär återvägarna: "Till områdesöversikten", aktuellt område och "Till sökträffarna (n)"
#   - områdesvyn har ingen egen brödsmula, sökspår eller tillbaka-länk längre; grannarna längst ned finns kvar
# Samma kväll (Adams justering): vanliga sökningar i en förslagsyta som visas när sökfältet får fokus, perspektivvalet
#   centrerat, och perspektivets förklaring med den gemensamma undertexten i en utfällning vid knappen i stället för
#   permanenta hjälprader.
# Skiss med produktutsnitt: SAEFUR_SKISS=1 lägger in figurer ur utsnitt.py i de funktioner som har ett utsnitt,
# och SAEFUR_UT pekar ut en annan målmapp. Ordinarie bygge (bygg_alla.py) sätter inget av detta.
import json
import os
import sys
from collections import Counter
from pathlib import Path

KALLA = Path(__file__).resolve().parent.parent
ROT = Path(os.environ["SAEFUR_UT"]).resolve() if os.environ.get("SAEFUR_UT") else KALLA
SKISS = os.environ.get("SAEFUR_SKISS") == "1"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from formagor_publika import FORMAGOR, OMRADEN, STATUS, GRANSER  # noqa: E402
from perspektiv import PERSPEKTIV, VISA_GRANSER  # noqa: E402
from bakgrund import BILDER, GRUPPBILD, VAXLING_SEK  # noqa: E402
from utsnitt import UTSNITT  # noqa: E402

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemensamt import LOGIN, EB, MENY, LANSERING, huvud, sidfot, skissrad, avslut_sektion, FORETAG  # noqa: E402

# ---------- Kontroller ----------
ids = [x["id"] for x in FORMAGOR]
assert len(ids) == len(set(ids)), "dubbla funktions-id"
alla = set(ids)
fm_av = {x["id"]: x for x in FORMAGOR}
for x in FORMAGOR:
    for h in x["hor"]:
        assert h in alla, (x["id"], h)
for p in PERSPEKTIV:
    gids = [gr["id"] for gr in p["grupper"]]
    assert len(gids) == len(set(gids)), ("dubbla grupp-id", p["id"])
    sedda = Counter()
    for gr in p["grupper"]:
        gr["alla_ids"] = gr["ids"] + [i for _, lista in gr["delar"] for i in lista]
        assert bool(gr["ids"]) != bool(gr["delar"]), ("antingen ids eller delar", p["id"], gr["id"])
        for i in gr["alla_ids"]:
            assert i in alla, ("okänt id", p["id"], gr["id"], i)
            sedda[i] += 1
        for n in gr["nasta"]:
            assert n in gids and n != gr["id"], ("okänd nasta", p["id"], gr["id"], n)
    saknas = alla - set(sedda)
    dubbla = [i for i, n in sedda.items() if n > 1]
    assert not saknas, (p["id"], "saknar", sorted(saknas))
    assert not dubbla, (p["id"], "dubbelt", sorted(dubbla))
    for fl in p["floden"]:
        assert len(fl["steg"]) == 4, (p["id"], fl["rubrik"])
        for i, _ in fl["steg"]:
            assert i in alla, (p["id"], i)

# Bakgrund: varje bild finns, varje grupp i varje perspektiv har en bild
bild_nycklar = {k for k, _, _ in BILDER}
for k, fil, _ in BILDER:
    assert (KALLA / "bilder" / fil).is_file(), ("saknad bild", fil)
if SKISS:
    for fid, u in UTSNITT.items():
        assert fid in alla, ("utsnitt för okänd funktion", fid)
        assert (KALLA / "bilder" / "utsnitt" / u["fil"]).is_file(), ("saknat utsnitt", u["fil"])
for p in PERSPEKTIV:
    for gr in p["grupper"]:
        assert GRUPPBILD[p["id"]].get(gr["id"]) in bild_nycklar, ("saknad gruppbild", p["id"], gr["id"])

# Grupp per funktion och perspektiv
grupp_for = {p["id"]: {i: gr["id"] for gr in p["grupper"] for i in gr["alla_ids"]} for p in PERSPEKTIV}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------- Funktionsrader (en gång, flyttas av JavaScript in i aktivt perspektiv) ----------
def utsnitt(x):
    # Bara i skissen: ett skarpt, läsbart utsnitt ur produkten med bildtext, går att förstora.
    u = UTSNITT.get(x["id"]) if SKISS else None
    if not u:
        return ""
    return f'''<figure class="utsnitt">
      <button type="button" class="utsnitt-bild" data-forstora aria-label="Förstora bilden: {esc(u["alt"])}">
        <img src="bilder/utsnitt/{u["fil"]}" alt="{esc(u["alt"])}" width="{u["bredd"]}" height="{u["hojd"]}" loading="lazy">
        <span class="lupp" aria-hidden="true">Förstora</span>
      </button>
      <figcaption><b>Ur SAEFUR:</b> {esc(u["text"])} <span class="demo">Exempelföretag med demodata.</span></figcaption>
    </figure>'''


def rad(x):
    hor = ""
    if x["hor"]:
        hor = '<p class="hor">Hör ihop med: ' + ", ".join(
            f'<a href="#{h}" data-fm="{h}">{esc(fm_av[h]["namn"])}</a>' for h in x["hor"]) + "</p>"
    return f'''<details class="fm" id="{x["id"]}">
  <summary><span class="namn">{esc(x["namn"])}</span></summary>
  <div class="inner">
    <p class="vad">{esc(x["vad"])}</p>
    <p class="nytta">{esc(x["nytta"])}</p>
    {utsnitt(x)}
    {hor}
    <p class="meta"><a class="lank" href="#{x["id"]}" data-kopiera="{x["id"]}">Länk till den här funktionen</a><span class="plats" data-plats></span></p>
  </div>
</details>'''


forrad = "".join(rad(x) for x in FORMAGOR)


# ---------- Perspektiv ----------
def gruppkort(p, gr):
    # Korta exempel som går att skanna (perspektiv.py, fältet ex); fullständiga funktionsnamn finns i gruppen.
    ex_t = " · ".join(gr["ex"])
    return f'''<li><a class="gkort" href="?p={p["id"]}&amp;g={gr["id"]}" data-g="{gr["id"]}">
      <b>{esc(gr["namn"])}</b><span class="rub">{esc(gr["rubrik"])}</span><span class="ex">{esc(ex_t)}</span><span class="pil" aria-hidden="true">→</span></a></li>'''


def flode(p, fl):
    steg = "".join(f'<li><a href="#{i}" data-fm="{i}">{esc(t)}</a></li>' for i, t in fl["steg"])
    return f'<div class="flode"><h3>{esc(fl["rubrik"])}</h3><ol>{steg}</ol></div>'


def grupp(p, gr, k):
    gav = {x["id"]: x for x in p["grupper"]}
    namn = esc(gr["namn"])
    if gr["delar"]:
        lista = "".join(
            f'<h3 class="del">{esc(r)}</h3><div class="lista-fm" data-ids="{" ".join(i)}"></div>' for r, i in gr["delar"])
    else:
        lista = f'<div class="lista-fm" data-ids="{" ".join(gr["ids"])}"></div>'
    nasta = " · ".join(f'<a href="?p={p["id"]}&amp;g={n}" data-g="{n}">{esc(gav[n]["namn"])}</a>' for n in gr["nasta"])
    fore = p["grupper"][k - 1] if k > 0 else None
    efter = p["grupper"][k + 1] if k + 1 < len(p["grupper"]) else None
    fore_h = f'<a class="granne" href="?p={p["id"]}&amp;g={fore["id"]}" data-g="{fore["id"]}"><small>Föregående</small>{esc(fore["namn"])}</a>' if fore else "<span></span>"
    efter_h = f'<a class="granne hoger" href="?p={p["id"]}&amp;g={efter["id"]}" data-g="{efter["id"]}"><small>Nästa</small>{esc(efter["namn"])}</a>' if efter else "<span></span>"
    return f'''
<section class="grupp" id="g-{p["id"]}-{gr["id"]}" data-g="{gr["id"]}" hidden>
  <div class="wrap">
    <div class="omrade">
      <div class="omr-huvud">
        <p class="etikett">{namn}</p>
        <h2>{esc(gr["rubrik"])}</h2>
        <p class="vem"><b>Vem:</b> {esc(gr["vem"])}</p>
        <p class="nasta">Leder vidare till {nasta}</p>
      </div>
      <div class="text">
        <p class="ingress-omr">{esc(gr["ingress"])}</p>
        {lista}
      </div>
    </div>
    <div class="grannar">{fore_h}<a class="tillbaka mitten" href="?p={p["id"]}" data-till="oversikt">Till områdesöversikten</a>{efter_h}</div>
  </div>
</section>'''


def perspektiv(p):
    kort = "".join(gruppkort(p, gr) for gr in p["grupper"])
    floden = "".join(flode(p, fl) for fl in p["floden"])
    granser = "".join(f"<li><b>{esc(a)}</b> {esc(b)}</li>" for a, b in GRANSER[:VISA_GRANSER])
    grupper = "".join(grupp(p, gr, k) for k, gr in enumerate(p["grupper"]))
    return f'''
<section class="p" id="p-{p["id"]}" data-p="{p["id"]}" hidden>
  <div class="oversikt">
    <div class="wrap">
      <div class="p-huvud">
        <p class="etikett">{esc(p["namn"])}</p>
        <h2 class="rubrik">{esc(p["rubrik"])}</h2>
        <p class="ingress">{esc(p["intro"])}</p>
        <p class="vem"><b>Vem:</b> {esc(p["vem"])}</p>
      </div>
      <div class="floden">{floden}</div>
      <p class="etikett omr-etikett" id="omr-{p["id"]}">Område för område</p>
      <ul class="gkort-lista">{kort}</ul>
      <div class="granser">
        <h3>Det här gör er partner, med underlag från SAEFUR</h3>
        <ul class="lista ute">{granser}</ul>
      </div>
    </div>
  </div>
  <div class="grupper">{grupper}</div>
</section>'''


# ---------- Data till JavaScript ----------
data = dict(
    perspektiv=[dict(id=p["id"], namn=p["namn"], kort=p["kort"], beskrivning=p["beskrivning"],
                     grupper=[dict(id=gr["id"], namn=gr["namn"], ids=gr["alla_ids"]) for gr in p["grupper"]]) for p in PERSPEKTIV],
    funktioner=[dict(id=x["id"], namn=x["namn"], sok=x["sok"], nytta=x["nytta"]) for x in FORMAGOR],
    granser=[dict(namn=a, text=b) for a, b in GRANSER],
    bilder=[k for k, _, _ in BILDER], gruppbild=GRUPPBILD, vaxling=VAXLING_SEK,
)

nav = "".join(f'<a href="{h}">{t}</a>' for h, t in MENY).replace('">Funktioner', '" aria-current="page">Funktioner')
exempel = ["fakturera", "offert", "leverans", "schema", "lagerplatser", "löneunderlag", "ÄTA", "SIE4"]
chips = "".join(f'<button type="button" class="chip" data-q="{esc(e)}">{esc(e)}</button>' for e in exempel)
UNDERTEXT = "Samma SAEFUR i alla tre. Perspektivet väljer ordningen, och innehållet är detsamma."
segment = "".join(
    f'<button type="button" class="seg-knapp" data-p="{p["id"]}" aria-pressed="false" aria-controls="p-{p["id"]}" aria-describedby="besk-{p["id"]}"><span class="lang">{esc(p["namn"])}</span><span class="kort">{esc(p["kort"])}</span></button>'
    for p in PERSPEKTIV)
# Förklaringarna för skärmläsare; den synliga utfällningen (#hjalp) fylls av JavaScript och är dold för dem.
beskrivningar = "".join(f'<span id="besk-{p["id"]}" hidden>{esc(p["beskrivning"])} {esc(UNDERTEXT)}</span>' for p in PERSPEKTIV)
sektioner = "".join(perspektiv(p) for p in PERSPEKTIV)
bakgrund = "".join(
    f'<img src="bilder/{fil}" alt="" data-bild="{k}"{" class=\"aktiv\"" if i == 0 else " loading=\"lazy\""}>'
    for i, (k, fil, _) in enumerate(BILDER))

html = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Funktioner | SAEFUR</title>
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="funktioner.css">
<link rel="stylesheet" href="lansering.css">
</head>
<body class="med-bakgrund">
<div class="bakgrund" aria-hidden="true">{bakgrund}</div>
{skissrad()}

{huvud("funktioner.html", fast=False)}

<main>
<section class="hero sida">
  <div class="wrap hero-text">
    <h1>Funktioner</h1>
    <p class="lead">Hitta det som hjälper er i vardagen. Se hur SAEFUR fungerar när du driver företaget själv, när ni delar på arbetet eller när flera avdelningar samverkar. Söker du en viss funktion når du den direkt.</p>
    <div class="sokyta" id="sokyta">
      <form class="sok" role="search" onsubmit="return false">
        <label for="q" class="visually-hidden">Sök funktion</label>
        <input id="q" type="text" placeholder="Sök en funktion, till exempel fakturera, schema eller lagerplatser" autocomplete="off" spellcheck="false" aria-controls="resultat sokforslag" aria-expanded="false">
        <button type="button" class="rensa" id="rensa" hidden aria-label="Rensa sökningen">×</button>
      </form>
      <div id="resultat" class="resultat" role="region" aria-label="Sökträffar" tabindex="-1" hidden></div>
      <div class="sokforslag" id="sokforslag" role="group" aria-labelledby="sokforslag-rubrik" hidden><p class="sokforslag-rubrik" id="sokforslag-rubrik">Vanliga sökningar</p><div class="sokforslag-chips">{chips}</div></div>
    </div>
  </div>
</section>

<div class="stang-vakt" aria-hidden="true"></div>
<div class="stang" id="stang">
  <div class="wrap">
    <div class="stang-rad">
      <nav class="kontext vanster" aria-label="Var du är" hidden>
        <a class="knapp-tillbaka" href="?p={PERSPEKTIV[0]["id"]}" data-till="oversikt" id="till-oversikt"><span class="pil" aria-hidden="true">←</span><span class="lang">Till områdesöversikten</span><span class="kort">Översikten</span></a>
        <span class="har"><span class="etik">Område</span><b id="spar-har"></b></span>
      </nav>
      <div class="seg" role="group" aria-label="Perspektiv">{segment}</div>
      <nav class="kontext hoger" aria-label="Sökningen" hidden>
        <a class="knapp-traffar" href="#q" data-visa-traffar id="till-traffar"><span class="lang">Till sökträffarna</span><span class="kort">Sökträffarna</span> <span id="traff-antal"></span></a>
      </nav>
    </div>
    <div class="utfall" id="hjalp" aria-hidden="true" hidden><p class="hjalp"></p><p class="under">{UNDERTEXT}</p></div>
    {beskrivningar}
  </div>
</div>

<div id="vy">{sektioner}</div>

<div id="forrad" hidden>
  <noscript><style>#forrad{{display:block;padding:40px 0}}</style><div class="wrap"><p class="ingress">De tre perspektiven visas med JavaScript. Här är alla funktioner i en lista.</p></div></noscript>
  <div class="wrap lista-fm">{forrad}</div>
</div>

<section class="avslut">
  <div class="wrap">
    <h2>SAEFUR lanseras i höst.</h2>
    <p class="lead" style="margin-left:auto;margin-right:auto">Anmäl ert företag till Early Bird så meddelar vi er så snart ni kan börja använda SAEFUR. Som Early Bird får ni 20 % rabatt på licenserna de första sex månaderna efter provperioden.</p>
    <div class="actions"><a class="btn stor" href="{EB}">Anmäl ditt företag till Early Bird</a></div>
  </div>
</section>
</main>

{sidfot()}

<script id="data" type="application/json">{json.dumps(data, ensure_ascii=False)}</script>
<dialog class="forstoring" id="forstoring" aria-label="Förstorad bild">
  <button type="button" class="stang-bild" data-stang-bild aria-label="Stäng">×</button>
  <img src="" alt="">
  <p class="bildtext"></p>
</dialog>
<script src="funktioner.js"></script>
</body>
</html>
'''
(ROT / "funktioner.html").write_text(html, encoding="utf-8")

# ---------- Intern kontrollsida ----------
omr_namn = {o["id"]: o["namn"] for o in OMRADEN}
tot = Counter(x["status"] for x in FORMAGOR)
rader = []
for x in FORMAGOR:
    platser = " · ".join(
        f'{p["kort"]}: {next(gr["namn"] for gr in p["grupper"] if gr["id"] == grupp_for[p["id"]][x["id"]])}' for p in PERSPEKTIV)
    rader.append(f'<tr class="{x["status"]}"><td>{esc(omr_namn[x["omrade"]])}</td><td><a href="funktioner.html#{x["id"]}">{esc(x["namn"])}</a><br><code>{x["id"]}</code></td>'
                 f'<td>{STATUS[x["status"]]}</td><td>{", ".join(x["fm"])}</td><td>{esc(x["not_"])}</td><td>{esc(platser)}</td></tr>')
storlek = "".join(
    f'<li><b>{esc(p["namn"])}</b>: ' + ", ".join(f'{esc(gr["namn"])} {len(gr["alla_ids"])}' for gr in p["grupper"]) + "</li>" for p in PERSPEKTIV)
kontroll = f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kontroll: Funktioner mot förmågekartan (intern)</title>
<style>
body{{font:15px/1.5 -apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;margin:32px;color:#1b2537;background:#fff}}
h1{{font-size:24px;margin:0 0 8px}} p{{max-width:860px}} table{{border-collapse:collapse;width:100%;font-size:14px;margin-top:24px}}
th,td{{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid #e3e7ee}} th{{background:#f3f5f8;position:sticky;top:0}}
code{{font-size:12px;color:#6b7893}} tr.kommer td:nth-child(3){{color:#b57a12;font-weight:600}} tr.avtal td:nth-child(3){{color:#8a5a00;font-weight:600}}
ul{{max-width:960px}} li{{margin:6px 0}}
</style></head><body>
<h1>Kontrollsida: Funktioner mot förmågekartan</h1>
<p>Intern sida, aldrig publik. Besökarens sida (<a href="funktioner.html">funktioner.html</a>) visar ingen statusetikett; sedan 26 oktober står planerade funktioner och väntande anslutningar beskrivna i texten vid funktionen. Här står för varje rad status enligt förmågekartan v54 (avstämd 25 oktober 2026), FM-källa, intern not och var raden ligger i de tre perspektiven, så att publiceringskontrollen kan göras rad för rad.</p>
<p>Totalt {len(FORMAGOR)} rader: {tot["finns"]} finns i dag, {tot["kommer"]} kommer, {tot["avtal"]} väntar på avtal. "Finns i dag" betyder antagen i deployrutinen, och driftversionen ska bekräftas före publicering (behovslistans E11).</p>
<h2 style="font-size:18px;margin-top:32px">Bakgrundsbilder</h2>
<p>Produktfångster ur v3:s bildmapp, bara vyer med diagram, tabeller, mätare eller foton. Alla med exempelföretaget Nordanå Kök &amp; Inredning AB. Kontrollerade 25 oktober: exempelpersoner, example-adresser, inga personnummer. HR och Företaget saknar fångst i nuvarande design.</p>
<ul>{"".join(f"<li><b>{k}</b> ({fil}): {esc(t)}</li>" for k, fil, t in BILDER)}</ul>
<h2 style="font-size:18px;margin-top:32px">Gruppstorlekar per perspektiv</h2>
<ul>{storlek}</ul>
<table><thead><tr><th>Produktområde</th><th>Funktion</th><th>Status</th><th>Förmågekartan</th><th>Intern not</th><th>Grupp per perspektiv</th></tr></thead>
<tbody>{"".join(rader)}</tbody></table>
</body></html>
'''
(ROT / "kontroll-funktioner.html").write_text(kontroll, encoding="utf-8")

(ROT / "funktioner.json").write_text(json.dumps(dict(
    datum="2026-10-25", kalla="Hantis-main/scripts/framdrift/formagor.mjs v54",
    perspektiv=[dict(id=p["id"], namn=p["namn"], grupper=[dict(id=gr["id"], namn=gr["namn"], rubrik=gr["rubrik"], ids=gr["alla_ids"]) for gr in p["grupper"]]) for p in PERSPEKTIV],
    funktioner=[dict(x) for x in FORMAGOR]), ensure_ascii=False, indent=1), encoding="utf-8")

print(f"Byggt funktioner.html, kontroll-funktioner.html, funktioner.json: {len(FORMAGOR)} funktioner, "
      + ", ".join(f'{p["kort"]} {len(p["grupper"])} grupper' for p in PERSPEKTIV))
