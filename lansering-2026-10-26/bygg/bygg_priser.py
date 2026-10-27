# Bygger Priser-prototypen: python3 -I bygg.py i mappen prototyp-priser. 2026-10-25.
#
#   priser.html     besökarens sida: staffling, räknare, licensprincip, "Så börjar det", fyra frågor, avslut
#   kontroll.html   intern sida: varje påstående med läge (beslutat/belagt, öppet affärsvillkor, bekräftas i produkten)
#
# Prismodellen är Adams arbetsförslag, aldrig beslutad prislista. Sidan skiljer tre lägen:
#   omärkt text              = fattat beslut eller belagt faktum
#   gul märkning (.forslag)  = öppet affärsvillkor, väntar på Adams beslut
#   prickad understrykning   = affärsavsikt som bekräftas i produkten före publicering (klassen bekrafta)
# Kopia av 5516 (godkänd och låst) med lanseringslagret, 25 okt 2026: python3 -I bygg/bygg_priser.py i mappen lansering-2026-10-26.
# Sidhuvud och sidfot kommer från gemensamt.py. Bolagsnamnet är rättat till AT Interactive Design AB.
# 27 okt (Adams uppdrag): förklaringen av intervallen med räkneexempel ur STAFFEL, en mening om nyttan med ett samlat system,
# licensens definition, rubriken "Så kommer ni igång." och betatest i stället för pilot. Priser och räkneregler oförändrade.
from pathlib import Path
import json

ROT = Path(__file__).resolve().parent.parent
FUNKTIONER = "funktioner.html"
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemensamt import LOGIN, EB, BETATEST, INLOGG, MENY, LANSERING, huvud, sidfot, skissrad, avslut_sektion, FORETAG  # noqa: E402

# ---------- Prismodell (arbetsförslag) ----------
STAFFEL = [("Första licensen", 1, 1, 995), ("Användare 2 till 10", 2, 10, 229), ("Användare 11 till 30", 11, 30, 179),
           ("Användare 31 till 60", 31, 60, 149), ("Användare 61 till 120", 61, 120, 129), ("Användare 121 och uppåt", 121, None, 99)]
EXEMPEL = (1, 10, 30)
STANDARD_ANTAL = 12
SNABBVAL = (1, 5, 12, 30, 60, 120)

# ---------- Bakgrund: fem fotografier i Adams ordning 25 okt (original i Documents/Codex/.../SAEFUR_prisbilder, orörda) ----------
# 26 okt: bilden med bilen ("På väg till kund", foto-01-pa-vag-till-kund.jpg) borttagen på Adams besked; filen ligger kvar i bilder/.
# Webbkopior i bilder/: JPEG 1672 x 941 ur originalens PNG. Fjärde fältet är beskärningspunkt (object-position) på dator,
# femte på mobil där bilden beskärs hårt till stående format; båda som "x y". Rörelse, övertoning och växling är oförändrade.
BILDER = [
    ("arbetsplats", "foto-02-mindre-foretagets-arbetsplats.jpg", "Det mindre företagets arbetsplats", "50% 50%", "50% 50%"),
    ("kontorslandskap", "foto-03-kontorslandskap.jpg", "Kontorslandskap", "50% 50%", "44% 50%"),
    ("praktisk", "foto-04-kontor-och-praktisk-verksamhet.jpg", "Kontor och praktisk verksamhet", "50% 50%", "52% 50%"),
    ("mote", "foto-05-gemensamt-mote.jpg", "Gemensamt möte", "50% 50%", "64% 50%"),
    ("styrelse", "foto-06-styrelsemote.jpg", "Styrelsemöte", "50% 45%", "52% 45%"),
]
VAXLING_SEK = 9

# ---------- Påståenden och läge: styr märkningen på sidan och den interna kontrollsidan ----------
# läge: "beslut" (fattat beslut eller belagt faktum, omärkt), "forslag" (öppet affärsvillkor, gul märkning),
#       "avsikt" (affärsavsikt som bekräftas i produkten, prickad understrykning)
P = [
    # id, läge, text som den står på sidan (eller sammandrag), källa, vad som krävs för att ta bort märkningen
    ("pris-niva", "forslag", "Första licensen 995 kr per månad, därefter 229, 179, 149, 129 och 99 kr per person i fallande intervall.",
     "Adams arbetsförslag 25 okt; beslutsunderlag v4 avsnitt 3", "Adams prisbeslut."),
    ("pris-intervall", "forslag", "Varje intervall har sitt eget pris, som gäller användarna i just det intervallet. När företaget får fler användare behåller de tidigare användarna sitt intervallpris.",
     "Arbetsförslag, kontrollräknat (1: 995, 10: 3 056, 30: 6 636)", "Adams prisbeslut om stafflingsprincipen."),
    ("moms", "forslag", "Priser exklusive moms.", "B10, rekommenderat: exklusive moms med tydlig rad, standard mot företag", "Adams bekräftelse."),
    ("grundprodukt", "forslag", "Grundprodukten omfattar hela kedjan från kund och projekt till ekonomi. Valbara tillägg redovisas här när de är beslutade.",
     "Adams inriktning: grundprodukt med valbara tillägg; B8: ingen lista förrän beslutad", "Beslut om vilka tillägg som finns och vad de kostar."),
    ("roller", "forslag", "Inga rollskillnader i pris; samma pris för alla personer.", "B6, rekommenderat: inga i första prislistan", "Adams bekräftelse. Står bara underförstått på sidan."),
    ("andring", "forslag", "Antalet personer kan ändras månad för månad.", "B7, rekommenderat: antal aktiva licenser på debiteringsdagen; P: vad abonnemangsflödet klarar",
     "Adams beslut om räknedag, och kontroll av abonnemangsflödet."),
    ("samlat", "beslut", "Alla i företaget arbetar i samma system, med samma kunder, offerter, tider och fakturor, och periodens underlag till redovisningsbyrån tas fram ur det som redan är registrerat.",
     "Start och Om (kundkortet med offerter, arbete och fakturor; fakturaunderlag ur registrerat arbete; SIE4 per period med lista över det som saknas, FM-källor i kontroll-funktioner.html). Adams uppdrag 27 okt.", "Inget."),
    ("licens", "avsikt", "En licens är en person med eget konto i företaget. Kundens länk, byråns läsplats och samarbetspartner i andra företag ingår utan kostnad.",
     "B5 och B3, allt affärsunderlag sedan augusti; B4 kundens länk är starkast belagd", "Adams bekräftelse av principen; P: byråns läsplats i drift (E7)."),
    ("avtal-ingar", "avsikt", "Bankkoppling och fraktbokning ingår i grundprodukten när de är på plats, utan extra kostnad från SAEFUR.",
     "Affärsavsikt enligt innehållsförslaget 02", "Adams bekräftelse. Funktionerna själva väntar på avtal."),
    ("early-bird", "beslut", "Anmäl er före lanseringen hösten 2026 och få 20 % rabatt på licenserna i sex månader. Anmälan ger ingen plats i betatestet.",
     "Adams godkända villkor 25 okt natt (08_lansering_early_bird_plan.md och Adams svar); fullständiga villkor på early-bird.html", "Belagt."),
    ("konto", "beslut", "När SAEFUR har öppnat skapar ni konto i webbläsaren.",
     "Verifierat 26 okt kväll mot driftversionen 509a79334: registreringen finns och spärren är driftsatt (/sv/register visar Registreringen är stängd); öppning sker efter Adams uttryckliga besked", "Inget."),
    ("prov-30", "avsikt", "Ni har 30 dagar att prova, och ingenting debiteras under tiden.",
     "B9+P9: provperiod sätts i dag per avtal utan fast längd", "P9: att självregistrering ger 30 dagar automatiskt, och vad som händer dag 31."),
    ("kort", "avsikt", "Kortuppgifter lämnas vid registreringen.", "B9+P9: kort kan registreras i förväg i produkten; att det begärs vid registrering är avsikt",
     "P9: att registreringsflödet begär kort."),
    ("besked", "avsikt", "Ni får besked om beloppet sju dagar före varje dragning.",
     "Förhandsbesked finns i appens meddelanden; debitering av SAEFURs egna abonnemang är avstängd i produktion", "P9: att SAEFUR kan debitera egna abonnemang."),
    ("bindning", "avsikt", "Abonnemanget löper per månad och sägs upp till periodens slut.", "B1, v3:s utkast; beslut saknas", "Adams beslut om bindningstid."),
    ("export", "avsikt", "Ni exporterar era egna uppgifter: kunder, fakturor, SIE-filer och dokument.",
     "B2+P: SIE4 och kundregister dokumenterade; fakturor, dokument och projekt kontrolleras", "P: vilka exporter som finns, och hur länge kontot är läsbart efter uppsägning."),
    ("betalning", "avsikt", "Månadsvis med sparat kort.", "B9+P9", "Samma som besked och kort."),
    ("kundlank", "avsikt", "Kundens länk ingår utan kostnad, och kunden använder den utan eget konto.", "B4, starkast belagda principen", "Adams bekräftelse, formell."),
    ("utanfor", "beslut", "Ligger utanför: bokslut och deklaration, lönekörning, kassaregister, personalliggare i byggherrens system.",
     "Produktgränser enligt förmågekartan och Funktioner-prototypen", "Belagt."),
    ("uppmaning", "beslut", "Anmäl dig till Early Bird. Frågor eller en genomgång först: info@saefur.com.", "Adams besked 25 okt natt: registreringsuppmaningarna leder till Early Bird", "Beslutat."),
    ("avsandare", "beslut", "AT Interactive Design AB, org.nr 559556-4393, säte Rättvik.", "Adams besked 25 okt 2026", "Inget."),
    ("founding", "beslut", "Founding Customer visas aldrig på prissidan.", "B14, Adams besked", "Beslutat."),
]
LAGE_NAMN = {"beslut": "Fattat beslut eller belagt", "forslag": "Öppet affärsvillkor, arbetsförslag", "avsikt": "Affärsavsikt, bekräftas i produkten"}
LAGE_KLASS = {"beslut": "", "forslag": "forslag", "avsikt": "bekrafta"}


def kr(n):
    return f"{n:,}".replace(",", " ") + " kr"


def pris(antal):
    return sum(p * max(0, min(antal, hi or antal) - lo + 1) for _, lo, hi, p in STAFFEL)


assert pris(1) == 995 and pris(10) == 3056 and pris(30) == 6636, "stafflingen räknar fel"
assert pris(60) == 3056 + 20 * 179 + 30 * 149 and pris(121) == pris(120) + 99

# Räkneexemplet under stafflingen: tio användare, sedan den elfte. Beloppen räknas ur STAFFEL.
_, _, _, P1 = STAFFEL[0]
_, _, HI2, P2 = STAFFEL[1]
_, _, _, P3 = STAFFEL[2]
EXEMPEL_TEXT = (f"Exempel: Med tio användare betalar ni {kr(P1)} för första licensen och {kr(P2)} för var och en av de nio andra, "
                f"{kr(pris(HI2))} i månaden. Den elfte användaren hör till nästa intervall och kostar {kr(P3)}. "
                f"De tio första behåller sina priser, och ni betalar {kr(pris(HI2 + 1))} i månaden.")
assert HI2 == 10 and pris(11) == 3235

for fil in {b for _, b, *_ in BILDER}:
    assert (ROT / "bilder" / fil).is_file(), f"saknar bild {fil}"

# Kontroll av språkreglerna i publik text (bara en varning i bygget).
FORBJUDET = (" inte ", "faktisk", "riktig", "verklig", "skav", "—", "–")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def m(pid, text=None):
    """Text med rätt märkning enligt läget i P. Omärkt om läget är beslut."""
    lage = next(l for i, l, *_ in P if i == pid)
    kl = LAGE_KLASS[lage]
    text = text if text is not None else next(t for i, _, t, *_ in P if i == pid)
    return f'<span class="{kl}" data-p="{pid}">{text}</span>' if kl else f'<span data-p="{pid}">{text}</span>'


staffel = "".join(
    f'<li data-lo="{lo}" data-hi="{hi or ""}"><span>{t}</span><em class="antal-i" aria-live="off"></em><b>{kr(p)}</b></li>'
    for t, lo, hi, p in STAFFEL)
exempel = "".join(
    f'<button type="button" class="ex" data-n="{n}"><p>{n} användare</p><b>{kr(pris(n))}</b><p>per månad</p></button>'
    for n in EXEMPEL)
snabb = "".join(f'<button type="button" class="chip" data-n="{n}">{n}</button>' for n in SNABBVAL)
bakgrund = '<div class="bakgrund" aria-hidden="true">' + "".join(
    f'<img src="bilder/{b}" alt="" data-bild="{k}" style="--pos:{pos};--pos-m:{posm}"{" class=\"aktiv\"" if i == 0 else " loading=\"lazy\""}>'
    for i, (k, b, _, pos, posm) in enumerate(BILDER)) + "</div>"

DATA = {"steg": [[lo, hi or 0, p] for _, lo, hi, p in STAFFEL], "bilder": [k for k, *_ in BILDER], "vaxling": VAXLING_SEK, "standard": STANDARD_ANTAL}

sida = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Priser | SAEFUR</title>
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="priser.css">
<link rel="stylesheet" href="lansering.css">
</head>
<body class="med-bakgrund">
{bakgrund}
{skissrad(' · <span class="forslag">gul märkning</span> = affärsvillkor som väntar på beslut · <span class="bekrafta">prickad understrykning</span> = bekräftas i produkten')}

{huvud("priser.html")}

<main>
<section class="hero sida">
  <div class="wrap hero-text">
    <span class="markning">Arbetsförslag till prislista, ej beslutat</span>
    <h1>Priset följer<br><span>antalet användare.</span></h1>
    <p class="lead">{m("samlat")} {m("pris-niva", "Första licensen kostar 995 kr per månad. Varje ytterligare användare kostar mindre ju fler ni är.")} {m("moms")}</p>
  </div>
</section>

<section class="sektion rakna" id="rakna">
  <div class="wrap pris-topp">
    <div class="staffel-del">
      <p class="etikett">Så räknas priset</p>
      <ul class="staffel" id="staffel">{staffel}</ul>
      <p class="not">{m("pris-intervall", "Priserna gäller per användare och månad. Varje intervall har sitt eget pris, som gäller användarna i just det intervallet. När företaget får fler användare behåller de tidigare användarna sitt intervallpris, och de nya användarna får priset i sitt intervall.")}</p>
      <p class="not">{m("pris-niva", EXEMPEL_TEXT)}</p>
    </div>
    <div class="raknare" id="raknare">
      <div class="raknare-huvud">
        <label for="antal">Hur många användare har ni?</label>
        <div class="falt"><input id="antal" type="number" min="1" max="2000" value="{STANDARD_ANTAL}" inputmode="numeric" aria-describedby="summa"><span>användare</span></div>
      </div>
      <input id="glid" type="range" min="1" max="150" value="{STANDARD_ANTAL}" aria-label="Antal användare" aria-controls="antal">
      <div class="snabb" aria-label="Snabbval">{snabb}</div>
      <p class="summa" id="summa">{kr(pris(STANDARD_ANTAL))} <small>per månad, exklusive moms</small></p>
      <p class="iord" id="iord"></p>
      <ol class="delar" id="delar" aria-label="Uppdelning per intervall"></ol>
      <p class="snitt" id="snitt"></p>
      <p class="mikro">Utan tillägg. {m("andring", "Antalet kan ändras månad för månad.")}</p>
    </div>
  </div>
  <div class="wrap">
    <p class="etikett exempel-etikett">Tre exempel, tryck för att räkna</p>
    <div class="exempel">{exempel}</div>
  </div>
</section>

<section class="sektion band">
  <div class="wrap">
    <h2 class="rubrik">Vad en licens är.</h2>
    <p class="ingress">{m("licens")}</p>
    <div class="tva" style="margin-top:48px">
      <div>
        <h3 class="etikett">Ingår i grundprodukten</h3>
        <p class="ingress" style="margin-top:0">{m("grundprodukt", "Hela kedjan från kund och projekt till leverans och ekonomi, för alla användare i företaget.")} Vad var och en ser och gör styrs av behörigheten. <a class="textlank" href="{FUNKTIONER}">Se hur SAEFUR fungerar</a></p>
        <ul class="lista">
          <li>{m("grundprodukt", "Valbara tillägg redovisas här när de är beslutade.")}</li>
          <li>{m("avtal-ingar")}</li>
        </ul>
      </div>
      <div>
        <h3 class="etikett">Ligger utanför</h3>
        <ul class="lista ute">
          <li>Bokslut och deklaration. Redovisningsbyrån får underlaget.</li>
          <li>Lönekörning. Lönepartnern får underlaget.</li>
          <li>Kassaregister.</li>
          <li>Personalliggare i byggherrens system.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sektion" id="borja">
  <div class="wrap">
    <h2 class="rubrik">Så kommer ni igång.</h2>
    <p class="ingress">Ni lägger upp företaget på egen hand, och vi hjälper gärna till på info@saefur.com. Vill ni börja före lanseringen kan ni <a class="textlank" href="{BETATEST}">anmäla intresse för betatestet</a>. Det som står med prickad understrykning är avsikten för flödet och bekräftas i produkten före publicering.</p>
    <ol class="start-steg">
      <li><span class="punkt" aria-hidden="true"></span><p class="nr">01</p><h3>Early Bird</h3><p>{m("early-bird")} <a class="textlank" href="early-bird.html#villkor">Villkor och anmälan</a></p></li>
      <li><span class="punkt" aria-hidden="true"></span><p class="nr">02</p><h3>Konto och 30 dagar</h3><p>{m("konto")} {m("prov-30")}</p></li>
      <li><span class="punkt" aria-hidden="true"></span><p class="nr">03</p><h3>Kort</h3><p>{m("kort")} {m("betalning", "Därefter betalar ni månadsvis med sparat kort.")}</p></li>
      <li><span class="punkt" aria-hidden="true"></span><p class="nr">04</p><h3>Besked</h3><p>{m("besked")}</p></li>
    </ol>
  </div>
</section>

<section class="sektion band">
  <div class="wrap">
    <h2 class="rubrik">Fyra frågor om priset.</h2>
    <div class="fragor">
      <div><h3>Hur lång är bindningstiden?</h3><p>{m("bindning")}</p></div>
      <div><h3>Vad händer med våra uppgifter om vi slutar?</h3><p>{m("export")}</p></div>
      <div><h3>Hur betalar vi?</h3><p>{m("betalning")} {m("besked")}</p></div>
      <div><h3>Vad kostar kundens länk?</h3><p>{m("kundlank")}</p></div>
    </div>
  </div>
</section>

{avslut_sektion()}
</main>

{sidfot()}
<script id="data" type="application/json">{json.dumps(DATA, ensure_ascii=False)}</script>
<script src="priser.js"></script>
</body>
</html>
'''
(ROT / "priser.html").write_text(sida, encoding="utf-8")

# Språkkontroll av den publika sidan (text utanför taggar)
import re
publik = re.sub(r"<script.*?</script>", "", sida, flags=re.S)
publik = re.sub(r"<[^>]+>", " ", publik)
varningar = [f for f in FORBJUDET if f in publik]
if varningar:
    print("VARNING, publik text innehåller:", varningar)

# ---------- Intern kontrollsida ----------
def rader(lage):
    return "".join(
        f"<tr><td><code>{i}</code></td><td>{esc(t)}</td><td>{esc(k)}</td><td>{esc(v)}</td></tr>"
        for i, l, t, k, v in P if l == lage)

antal = {l: sum(1 for _, x, *_ in P if x == l) for l in LAGE_NAMN}
kontroll = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kontroll: Priser (intern)</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;margin:0;padding:32px;background:#f5f6f8;color:#1b2537;font-size:15px;line-height:1.5}}
h1{{margin:0 0 8px}} h2{{margin:40px 0 12px;font-size:20px}} p{{max-width:860px}}
table{{border-collapse:collapse;width:100%;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px #0001}}
th,td{{text-align:left;vertical-align:top;padding:10px 14px;border-bottom:1px solid #e6e9ee}} th{{background:#eef1f6;font-size:13px;letter-spacing:.04em;text-transform:uppercase}}
td:nth-child(2){{width:38%}} code{{font-size:13px;background:#eef1f6;padding:2px 6px;border-radius:6px}}
.beslut th{{background:#dff3e6}} .forslag th{{background:#fbecc9}} .avsikt th{{background:#e4e9f7}}
.bild{{display:flex;gap:16px;flex-wrap:wrap}} .bild figure{{margin:0;width:260px}} .bild img{{width:100%;border-radius:8px;display:block}} .bild figcaption{{font-size:13px;color:#4a5668;margin-top:6px}}
a{{color:#1b2537}}
</style>
</head>
<body>
<h1>Kontroll: Priser</h1>
<p>Intern sida, aldrig publik. Besökarens sida (<a href="priser.html">priser.html</a>) visar prismodellen som arbetsförslag. Här står varje påstående med sitt läge, källa och vad som krävs för att märkningen ska tas bort. Lägena styr märkningen på sidan via <code>P</code> i <code>bygg.py</code>: omärkt text är fattat beslut eller belagt faktum, gul märkning är ett öppet affärsvillkor, prickad understrykning är affärsavsikt som bekräftas i produkten (P9 i beslutsunderlaget).</p>
<p>Fattade beslut och belagt: {antal["beslut"]} · Öppna affärsvillkor: {antal["forslag"]} · Bekräftas i produkten: {antal["avsikt"]}</p>

<h2>Fattat beslut eller belagt faktum (omärkt på sidan)</h2>
<table class="beslut"><thead><tr><th>Id</th><th>Påstående</th><th>Källa</th><th>Kvar att göra</th></tr></thead><tbody>{rader("beslut")}</tbody></table>

<h2>Öppet affärsvillkor, arbetsförslag (gul märkning)</h2>
<table class="forslag"><thead><tr><th>Id</th><th>Påstående</th><th>Källa</th><th>Krävs för att ta bort märkningen</th></tr></thead><tbody>{rader("forslag")}</tbody></table>

<h2>Affärsavsikt som bekräftas i produkten (prickad understrykning)</h2>
<table class="avsikt"><thead><tr><th>Id</th><th>Påstående</th><th>Källa</th><th>Krävs för att ta bort märkningen</th></tr></thead><tbody>{rader("avsikt")}</tbody></table>

<h2>Verifierat i produkten i dag (ur innehållsförslaget 02 och beslutsunderlaget P9)</h2>
<table><tbody>
<tr><td>Registrering på saefur.com/sv/register finns men saknar spärr i drift; webben länkar dit inte. Inloggning på <a href="{LOGIN}">saefur.com/sv/login</a> finns kvar som diskret {INLOGG}.</td></tr>
<tr><td>Kort kan registreras i förväg.</td></tr>
<tr><td>Provperiod sätts per avtal, utan fast längd. 30 dagar vid självregistrering är avsikt.</td></tr>
<tr><td>Förhandsbesked sju dagar före dragning finns i appens meddelanden.</td></tr>
<tr><td>Debitering av SAEFURs egna abonnemang är avstängd i produktion. Betalflödet är därmed overifierat som helhet.</td></tr>
<tr><td>Produktionen kör en äldre version än main; allt som sägs om produkten bekräftas mot driftversionen före publicering.</td></tr>
</tbody></table>

<h2>Räkneexempel (kontrollräknade i bygget)</h2>
<table><thead><tr><th>Personer</th><th>Per månad, exkl. moms</th><th>Uppdelning</th></tr></thead><tbody>
{"".join(f"<tr><td>{n}</td><td>{kr(pris(n))}</td><td>{' + '.join(f'{max(0, min(n, hi or n) - lo + 1)} × {kr(p)}' for _, lo, hi, p in STAFFEL if min(n, hi or n) >= lo)}</td></tr>" for n in (1, 5, 10, 12, 30, 60, 120, 121, 200))}
</tbody></table>

<h2>Bakgrundsbilder</h2>
<p>Fem fotografier i Adams ordning 25 oktober (bilden med bilen borttagen 26 oktober), byte från produktfångsterna (kopia före bytet i <code>../prototyp-priser-sparad-fore-nya-bilder/</code>). Original orörda i Documents/Codex, webbkopior som JPEG i <code>bilder/</code>. Växling var {VAXLING_SEK}:e sekund, drift och övertoning enligt samma regler som på Funktioner, stilla vid minskad rörelse. Beskärningspunkt per bild för dator och mobil i listan <code>BILDER</code> i <code>bygg.py</code>.</p>
<div class="bild">{"".join(f'<figure><img src="bilder/{b}" alt=""><figcaption>{esc(t)} · dator {pos}, mobil {posm}</figcaption></figure>' for _, b, t, pos, posm in BILDER)}</div>
</body>
</html>
'''
(ROT / "kontroll-priser.html").write_text(kontroll, encoding="utf-8")
print("byggt priser.html och kontroll-priser.html;", len(P), "påståenden;", antal)
