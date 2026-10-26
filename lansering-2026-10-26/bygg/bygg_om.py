# Bygger Om SAEFUR-prototypen: python3 -I bygg.py i mappen prototyp-om. 2026-10-25 sen kväll.
#
#   om.html         besökarens sida: varför SAEFUR finns, tankarna bakom, fyra principer, det vi lovar, företaget, avslut
#   kontroll.html   intern sida: varje påstående med läge och källa
#
# Sidan är ett textförslag för Adams granskning. Den skiljer tre lägen:
#   omärkt text              = belagt i produkt, broschyr eller dokument, eller Adams eget besked
#   prickad understrykning   = bekräftas mot driftversionen eller kompletteras före publicering (klassen bekrafta)
#   (ingen gul märkning här: sidan innehåller inga öppna affärsvillkor)
# Sidhuvud, sidfot och stil följer v4 (../../v4-lattare-2026-10-25/). Bakgrund: tre egna fotografier (sedan 26 okt) med samma
# rörelse som den godkända prissidan (port 5516). Ingen person nämns vid namn.
# Kopia med lanseringslagret, 25 okt 2026: python3 -I bygg/bygg_om.py i mappen lansering-2026-10-26. Sidhuvud och sidfot från gemensamt.py.
from pathlib import Path
import json
import re

ROT = Path(__file__).resolve().parent.parent
FUNKTIONER = "funktioner.html"
PRISER = "priser.html"
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemensamt import LOGIN, EB, MENY, LANSERING, huvud, sidfot, skissrad, avslut_sektion, FORETAG, ORGSATE  # noqa: E402

# ---------- Bakgrund: tre egna fotografier, byte 26 okt 2026 (Adams besked: Priser och Om ska inte dela bilder) ----------
# Original _v2 (PNG 1672 x 941) i Documents/Codex/.../SAEFUR_prisbilder, orörda. Webbkopior som JPEG i bilder/.
# Fjärde fältet är beskärningspunkt på dator, femte på mobil.
BILDER = [
    ("samarbete", "foto-11-huvudkontor-samarbete.jpg", "Kollegor stämmer av vid en skärm", "50% 45%", "74% 45%"),
    ("arbetsmiljo", "foto-12-huvudkontor-arbetsmiljo.jpg", "Vardagligt arbete på ett mindre, modernt huvudkontor", "50% 50%", "62% 50%"),
    ("personalmote", "foto-13-huvudkontor-personalmote.jpg", "Fem kollegor diskuterar runt ett mötesbord", "50% 45%", "52% 45%"),
]
VAXLING_SEK = 9

# ---------- Påståenden och läge ----------
# läge: "belagt" (omärkt; källa i dokument, broschyr eller kod), "besked" (omärkt; Adams eget besked 25 okt),
#       "bekrafta" (prickad understrykning; bekräftas mot driftversionen eller kompletteras före publicering)
P = [
    # id, läge, text som den står på sidan (eller sammandrag), källa, kvar att göra
    ("kundservice", "belagt",
     "Efter många år med ansvar för kundservice vet vi att utebliven, försenad eller felaktig information är en av de största orsakerna till missnöjda kunder.",
     "Adams redaktionella riktlinjer (citerade i omtag-2026-10-25/01_analys.md avsnitt 5). Erfarenhetsutsaga från avsändaren, ingen studie.",
     "Inget. Orden verksamhet och ledning ur v3:s utkast är borttagna eftersom de saknar belägg utöver utkastet."),
    ("leta", "belagt",
     "Samlad information ger tillbaka den tid som annars går åt till att leta, påminna, föra över och stämma av.",
     "SAEFUR Nuläge och konkurrensbenchmark 18 okt 2026 (Sälj-mappen): kundvärdet beskrivs som det arbete som försvinner: leta efter underlag, påminna, registrera om, stämma av.",
     "Inget."),
    ("en-gang", "belagt",
     "En uppgift registreras en gång, där den uppstår, och följer sedan med från överenskommelsen med kunden, genom arbetet, till fakturan och vidare till underlaget hos redovisningspartnern.",
     "Broschyr 1 (okt 2026) principen Registrera en gång; Produktöversikt sept 2026 avsnitt 1.",
     "Inget."),
    ("insyn", "belagt",
     "Varje person får den insyn och befogenhet som uppgiften kräver. Förtroliga uppgifter, som anställningshandlingar och marginaler, är förbehållna dem som har ansvaret för dem, och den som leder kan följa helheten.",
     "Förmågekartan: rättigheter per person (FM-205), anställningshandlingar bakom uttrycklig rättighet (FM-257), marginal efter part och rättighet (FM-172). Ersätter den avvisade formuleringen om den enda som vet (Adams besked 26 okt).",
     "Inget."),
    ("halla-ihop", "belagt",
     "Läget, nästa steg och handlingen på samma ställe.",
     "Egen sammanfattning av känslan i Hantis-main/docs/04_PRODUCT/UX_FEELING_BRIEF.md (maj 2026). Det tidigare citatet är ersatt enligt ordspärren 26 okt.",
     "Inget."),
    ("fyra-fragor", "besked",
     "Fyra frågor som varje vy prövas mot: förstå läget, se nästa steg, agera där du är, låt uppgiften följa med.",
     "Begriplighet, hanterbarhet och meningsfullhet ur UX-briefen (känsla av sammanhang). B12 i beslutsunderlaget och Adams besked 25 okt: tanken kvar, begreppet nämns aldrig. Hanterbarhet är delad i två frågor för att följa regeln om fyra led.",
     "Adam läser formuleringarna. Fråga 2 och 3 kan slås ihop om tre led godtas."),
    ("princip-1", "belagt", "Registrera en gång.", "Broschyr 1 okt 2026, Tre principer.", "Inget."),
    ("princip-2", "belagt", "Tydligt underlag. Medvetna beslut.", "Broschyr 1 okt 2026 (där: Fakta beslutar, människan attesterar), omformulerad 26 okt efter språkanalysen; produkten: förberedda påminnelser godkänns före utskick (FM-116), fakturautkast låses av en människa (FM-131).", "Broschyrerna har fortfarande det äldre namnet."),
    ("princip-3", "belagt", "Ni börjar med det ni behöver.", "Broschyr 1 okt 2026 (där: Ni möter det ni använder), omformulerad 26 okt; menyn visar områden efter användning och behörighet (FM-224).", "Broschyrerna har fortfarande det äldre namnet."),
    ("princip-4", "belagt", "Kunden ser det som berör kunden.",
     "Produktöversikt sept 2026, unik funktion 05: kundens länk med status, bilder, offerter och fakturor; interna siffror, marginaler och intern kommunikation stannar hos er. Fjärde principen enligt 02 och fråga 9 i 04 (fyra led).",
     "Adam avgör om fyra principer är bättre än tre (fråga 9)."),
    ("formagekarta", "belagt",
     "Beskrivningarna på webbplatsen följer produktens egen förmågekarta, som stäms av mot koden och driften.",
     "Hantis-main/scripts/framdrift/formagor.mjs; arbetssättet i innehållsförslaget 01 och 03.",
     "Inget. Sedan 26 okt står planerade funktioner och väntande anslutningar beskrivna vid respektive funktion på Funktioner (Adams uppdrag 26 okt)."),
    ("rakt-svar", "belagt", "Frågor om ert eget arbetssätt besvarar vi på info@saefur.com.",
     "Supportadressen är den enda belagda kontaktvägen (01_analys). Svarstid saknas (D5).", "Svarstid om Adam vill ange en."),
    ("i-drift", "besked", "SAEFUR körs i dag hos pilotföretag i Sverige.", "Ersätter \"i drift i Sverige\" från v4:s sidfot, som läser fel bredvid Lansering hösten 2026. Piloter är bekräftade i 08_lansering_early_bird_plan.md.", "Inget. Godkänd av Adam 25 okt 2026."),
    ("konto", "belagt", "När SAEFUR har öppnat skapar ni konto i webbläsaren.", "Verifierat 26 okt kväll mot driftversionen 509a79334: registreringen finns och spärren är driftsatt (/sv/register visar Registreringen är stängd). Meningen beskriver läget efter öppning, som sker på Adams besked.", "Inget."),
    ("sprak", "belagt", "Medarbetare kan använda systemet på 26 språk.",
     "Hantis-main/src/i18n/languages.ts 25 okt: 26 språk med status live (sv, nb, da, fi, is, fit, se, en, de, fr, es, it, pt-PT, pl, ro, uk, ru, tr, bg, hr, sr-Latn, bs, sq, el, lt, lv). Broschyr 1 säger också 26.",
     "Inget. Verifierat 26 okt kväll mot driftversionen 509a79334: LIVE_LOCALES har 26 språk (24 maskinöversatta, fit och se ogranskade enligt 9e012c6bb)."),
    ("inloggning", "belagt", "Inloggning med BankID, e-post eller passkey med Face ID eller Touch ID.",
     "Hantis-main/src: login-form.tsx (passkeys), bankid/bankid-verify-client.tsx (BankID). Står i v4 sedan v3.",
     "Inget. Verifierat 26 okt kväll mot driftversionen 509a79334: inloggningssidan i drift har BankID, e-post och passkey."),
    ("bolaget", "besked",
     "Bakom SAEFUR står AT Interactive Design AB, ett svenskt aktiebolag med kontor i Rättvik och Stockholm.",
     "Adams besked 25 okt sen kväll. Namnformen AT Interactive Design används också i Sälj-mappens dokument (sept 2026). Formen AT Interaktiv Design AB var fel och är rättad i v4, Priser och bevarade kopior.",
     "Inget."),
    ("1991", "besked",
     "Bolaget grundades första gången 1991. Fokus har varit detsamma då som nu: att göra det enklare för företagare att vara effektiva i sin vardag.",
     "Adams besked 25 okt sen kväll. Inget dokument i Sälj- eller marknadsmapparna nämner årtalet.",
     "Inget, om Adam står för uppgiften. Årtalet kan styrkas med Bolagsverkets registerutdrag."),
    ("varumarken", "besked", "AT Interactive Design och SAEFUR är helägda svenska varumärken.",
     "Adams besked 25 okt sen kväll.", "Inget."),
    ("ingen-person", "besked", "Ingen person nämns vid namn på sidan.",
     "Adams besked 25 okt sen kväll. Ersätter avsändarstycket i v3 och v4 (D1, D2 utgår).", "Inget."),
    ("orgnr", "besked", "Org.nr 559556-4393, säte Rättvik (sidfoten).",
     "Adams besked 25 okt 2026: AT Interactive Design AB, org.nr 559556-4393, säte Rättvik. Kontoren i Rättvik och Stockholm är en separat uppgift.",
     "Inget."),
    ("support", "belagt", "Support: info@saefur.com.", "Enda belagda supportadressen (01_analys, v4).", "Inget."),
]
LAGE_NAMN = {"belagt": "Belagt i dokument, broschyr eller kod", "besked": "Adams besked 25 oktober", "bekrafta": "Bekräftas eller kompletteras före publicering"}
LAGE_KLASS = {"belagt": "", "besked": "", "bekrafta": "bekrafta"}

for fil in {b for _, b, *_ in BILDER}:
    assert (ROT / "bilder" / fil).is_file(), f"saknar bild {fil}"

# Språkreglerna i publik text (varning i bygget)
FORBJUDET = (" inte ", "faktisk", "riktig", "verklig", "skav", "den enda som vet", "—", "–", "personal")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def m(pid, text=None):
    """Text med rätt märkning enligt läget i P. Omärkt om läget är belagt eller besked."""
    lage = next(l for i, l, *_ in P if i == pid)
    kl = LAGE_KLASS[lage]
    text = text if text is not None else next(t for i, _, t, *_ in P if i == pid)
    return f'<span class="{kl}" data-p="{pid}">{text}</span>' if kl else f'<span data-p="{pid}">{text}</span>'


bakgrund = '<div class="bakgrund" aria-hidden="true">' + "".join(
    f'<img src="bilder/{b}" alt="" data-bild="{k}" style="--pos:{pos};--pos-m:{posm}"{" class=\"aktiv\"" if i == 0 else " loading=\"lazy\""}>'
    for i, (k, b, _, pos, posm) in enumerate(BILDER)) + "</div>"

nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == "om.html" else ""}>{t}</a>' for h, t in MENY)
panel = "".join(f'<a href="{h}">{t}</a>' for h, t in MENY)

DATA = {"bilder": [k for k, *_ in BILDER], "vaxling": VAXLING_SEK}

# ---------- Texterna ----------
FRAGOR = [
    ("01", "Förstå läget",
     "Det som visas går att förstå direkt: vad som är klart, vad som pågår, vad som väntar och vad som är försenat. Varje siffra hör ihop med det arbete den kommer ifrån."),
    ("02", "Se nästa steg",
     "Systemet förbereder nästa handling, som offerten, påminnelsen, fakturan eller attesten. Du ser vad som väntar på dig och kan ta det i tur och ordning."),
    ("03", "Agera där du är",
     "Det som behövs för att ta steget finns i samma vy. Den som står hos kunden registrerar arbetet och skickar det för godkännande direkt från telefonen."),
    ("04", "Låt uppgiften följa med",
     "Det som registreras används vidare. Tiden blir underlag för fakturan, fotot blir en del av dokumentationen, kvittot blir en post i periodens underlag och ett godkännande visar vad som är klart att fakturera."),
]
PRINCIPER = [
    ("princip-1", "Registrera en gång",
     "Det som händer i verksamheten registreras där det händer. Kunden, artikeln, tiden och leveransen följer sedan med till offerten, fakturan, lagersaldot och periodens underlag."),
    ("princip-2", "Tydligt underlag. Medvetna beslut.",
     "Systemet föreslår och förbereder, och människan fattar besluten. En förberedd påminnelse skickas när du har godkänt den, och ett fakturautkast blir faktura när du låser det."),
    ("princip-3", "Ni börjar med det ni behöver",
     "Lager, HR, projekt och samarbeten visas när verksamheten behöver dem. Systemet växer med företaget, och varje person ser de områden som hör till uppgiften."),
    ("princip-4", "Kunden ser det som berör kunden",
     "Kunden följer sin affär via personliga länkar, utan konto: offerten, arbetet, avtalet och fakturan. Marginaler och interna anteckningar stannar hos er."),
]

fragor = "".join(
    f'<li><span class="punkt" aria-hidden="true"></span><p class="nr">{n}</p><h3>{h}</h3><p>{t}</p></li>' for n, h, t in FRAGOR)
principer = "".join(f'<div><h3>{m(pid, h)}</h3><p>{t}</p></div>' for pid, h, t in PRINCIPER)

sida = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Om SAEFUR | SAEFUR</title>
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="om.css">
<link rel="stylesheet" href="lansering.css">
</head>
<body class="med-bakgrund">
{bakgrund}
{skissrad(' · <span class="bekrafta">prickad understrykning</span> = bekräftas före publicering')}

{huvud("om.html")}

<main>
<section class="hero sida">
  <div class="wrap hero-text">
    <h1>Fördela ansvaret.<br><span>Följ helheten.</span></h1>
    <p class="lead">SAEFUR hjälper er att samordna verksamheten. Varje medarbetare får relevant insyn och befogenhet för sin uppgift, och den som leder ser vad som är överenskommet, genomfört, fakturerat och betalt.</p>
  </div>
</section>

<section class="sektion varfor" id="varfor">
  <div class="wrap omrade">
    <div>
      <p class="etikett">Varför SAEFUR finns</p>
      <h2>När företaget växer behöver kunskapen kunna delas.</h2>
    </div>
    <div class="text">
      <p>I ett litet företag samlas mycket kunskap hos ägaren: vad som är lovat, vem som är hos vilken kund, vad som är levererat och vilken faktura som ska skickas. När fler blir inblandade behöver överenskommelser, beslut och underlag finnas där arbetet görs, så att kollegorna kan driva sitt arbete och underlaget kan uppdateras när dagen förändras.</p>
      <p>{m("kundservice")} {m("leta")}</p>
      <p>SAEFUR är byggt för att {m("en-gang", "en uppgift ska registreras en gång, där den uppstår, och sedan följa med: från överenskommelsen med kunden, genom arbetet, till fakturan och vidare till underlaget hos redovisningspartnern.")} {m("insyn")}</p>
    </div>
  </div>
</section>

<section class="sektion band" id="tankarna">
  <div class="wrap">
    <p class="etikett">Tankarna som präglar systemet</p>
    <h2 class="rubrik">{m("halla-ihop")}</h2>
    <p class="ingress">Så vill vi att det ska kännas att öppna SAEFUR en vanlig tisdag. {m("fyra-fragor", "Därför prövar vi varje vy i systemet mot fyra frågor.")}</p>
    <ol class="fragor-spar">{fragor}</ol>
  </div>
</section>

<section class="sektion" id="principer">
  <div class="wrap">
    <p class="etikett">Så är systemet byggt</p>
    <h2 class="rubrik">Fyra principer som styr produkten.</h2>
    <div class="principer fyra">{principer}</div>
  </div>
</section>

<section class="sektion band" id="lovar">
  <div class="wrap tva">
    <div>
      <p class="etikett">Det vi lovar</p>
      <h2 class="rubrik">Tydligt besked om vad som finns.</h2>
      <p class="ingress">{m("formagekarta")} Där en funktion är planerad eller väntar på en anslutning till bank, transportör eller myndighet står det vid funktionen. {m("rakt-svar")}</p>
    </div>
    <div>
      <p class="etikett">Läget i dag</p>
      <ul class="lista">
        <li>{m("i-drift")}</li>
        <li>{m("konto")} Ni kan lägga upp första kunden och skicka första offerten samma dag.</li>
        <li>{m("sprak")}</li>
        <li>{m("inloggning")}</li>
      </ul>
    </div>
  </div>
</section>

<section class="sektion" id="foretaget">
  <div class="wrap omrade">
    <div>
      <p class="etikett">Företaget</p>
      <h2>Samma fokus sedan 1991.</h2>
    </div>
    <div class="text">
      <p>{m("bolaget")} {m("1991")}</p>
      <p>{m("varumarken")} Utvecklingen och supporten har samma avsändare, och supporten nås på {m("support", "info@saefur.com.")}</p>
      <dl class="fakta">
        <div><dt>Bolag</dt><dd>AT Interactive Design AB</dd></div>
        <div><dt>Kontor</dt><dd>Rättvik och Stockholm</dd></div>
        <div><dt>Grundat</dt><dd>Första gången 1991</dd></div>
        <div><dt>Support</dt><dd><a href="mailto:info@saefur.com">info@saefur.com</a></dd></div>
      </dl>
    </div>
  </div>
</section>

{avslut_sektion()}
</main>

{sidfot(ORGSATE + " · kontor i Rättvik och Stockholm")}
<script id="data" type="application/json">{json.dumps(DATA, ensure_ascii=False)}</script>
<script src="om.js"></script>
</body>
</html>
'''
(ROT / "om.html").write_text(sida, encoding="utf-8")

# Språkkontroll av den publika sidan (text utanför taggar)
publik = re.sub(r"<script.*?</script>", "", sida, flags=re.S)
publik = re.sub(r"<[^>]+>", " ", publik).lower()
varningar = [f for f in FORBJUDET if f in publik]
if varningar:
    print("VARNING, publik text innehåller:", varningar)
# Säkerställ att ingen person nämns vid namn
for namn in ("adam", "brännström", "tobbe"):
    assert namn not in publik, f"personnamn på sidan: {namn}"

# ---------- Intern kontrollsida ----------
KONTROLL_CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;margin:0;padding:32px;background:#f5f6f8;color:#1b2537;font-size:15px;line-height:1.5}
h1{margin:0 0 8px} h2{margin:40px 0 12px;font-size:20px} p{max-width:860px}
table{border-collapse:collapse;width:100%;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px #0001}
th,td{text-align:left;vertical-align:top;padding:10px 14px;border-bottom:1px solid #e6e9ee} th{background:#eef1f6;font-size:13px;letter-spacing:.04em;text-transform:uppercase}
td:nth-child(2){width:34%} code{font-size:13px;background:#eef1f6;padding:2px 6px;border-radius:6px}
.belagt th{background:#dff3e6} .besked th{background:#e4e9f7} .bekrafta th{background:#fbecc9}
.bild{display:flex;gap:16px;flex-wrap:wrap} .bild figure{margin:0;width:260px} .bild img{width:100%;border-radius:8px;display:block} .bild figcaption{font-size:13px;color:#4a5668;margin-top:6px}
a{color:#1b2537}
"""


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
<title>Kontroll: Om SAEFUR (intern)</title>
<style>{KONTROLL_CSS}</style>
</head>
<body>
<h1>Kontroll: Om SAEFUR</h1>
<p>Intern sida, aldrig publik. Besökarens sida (<a href="om.html">om.html</a>) är ett textförslag. Här står varje påstående med sitt läge, källa och vad som är kvar. Lägena styr märkningen via <code>P</code> i <code>bygg.py</code>: omärkt text är belagd i dokument, broschyr eller kod, eller är Adams eget besked; prickad understrykning bekräftas mot driftversionen eller kompletteras före publicering. Sidan har inga öppna affärsvillkor och därför ingen gul märkning.</p>
<p>Belagt: {antal["belagt"]} · Adams besked: {antal["besked"]} · Bekräftas eller kompletteras: {antal["bekrafta"]}</p>
<p>Avsikten med sidan: förklara varför SAEFUR finns och vilka tankar som präglar systemet, utan att upprepa Funktioner och utan teorigenomgång. Begreppet känsla av sammanhang (B12) nämns aldrig; dess tre delar bär avsnittet "Tankarna som präglar systemet" som fyra frågor. Ingen person nämns vid namn (bygget stoppar om ett namn smyger in).</p>

<h2>Belagt i dokument, broschyr eller kod (omärkt på sidan)</h2>
<table class="belagt"><thead><tr><th>Id</th><th>Påstående</th><th>Källa</th><th>Kvar</th></tr></thead><tbody>{rader("belagt")}</tbody></table>

<h2>Adams besked 25 oktober (omärkt på sidan)</h2>
<table class="besked"><thead><tr><th>Id</th><th>Påstående</th><th>Källa</th><th>Kvar</th></tr></thead><tbody>{rader("besked")}</tbody></table>

<h2>Bekräftas eller kompletteras före publicering (prickad understrykning)</h2>
<table class="bekrafta"><thead><tr><th>Id</th><th>Påstående</th><th>Källa</th><th>Krävs för att ta bort märkningen</th></tr></thead><tbody>{rader("bekrafta")}</tbody></table>

<h2>Lämnat utanför sidan, och varför</h2>
<table><tbody>
<tr><td>Avsändarstycke med namn, porträtt och bakgrund (D1, D2).</td><td>Adams besked 25 okt: ingen person nämns vid namn.</td></tr>
<tr><td>Begreppet känsla av sammanhang och forskarens namn (D3, B12).</td><td>Tanken kvar som fyra frågor, begreppet utelämnat enligt Adams besked.</td></tr>
<tr><td>Listan "Finns i dag / Kommer" från v3 och v4.</td><td>Ingen samlad lista. Sedan 26 okt beskrivs planerade funktioner och väntande anslutningar vid respektive funktion på Funktioner.</td></tr>
<tr><td>Målgruppstal (30 till 50, 1 till 100, 15 till 80).</td><td>Fråga 8 i 04 är obesvarad. Sidan beskriver det lilla företaget som växer utan tal.</td></tr>
<tr><td>Dokument till kund på sex språk.</td><td>Broschyr 1 säger att offert, avtal och faktura ställs ut på svenska; koden har sex dokumentspråk. Motstridigt, därför utelämnat.</td></tr>
<tr><td>Pilotkunder, kundomdömen, siffror om användning.</td><td>Saknar belägg (01_analys, strategirapporten).</td></tr>
<tr><td>Specialister, partner, byråer vid namn (D4).</td><td>Ingen har godkänt att nämnas.</td></tr>
<tr><td>Supportens svarstid (D5).</td><td>Saknas.</td></tr>
</tbody></table>

<h2>Bakgrundsbilder</h2>
<p>Tre egna fotografier sedan 26 oktober (tidigare samma sex som prissidan). Original _v2 orörda i Documents/Codex, webbkopior som JPEG i <code>bilder/</code>. Växling var {VAXLING_SEK}:e sekund, samma drift och toning som prissidan, stilla vid minskad rörelse. Beskärningspunkt per bild i listan <code>BILDER</code> i <code>bygg/bygg_om.py</code>.</p>
<div class="bild">{"".join(f'<figure><img src="bilder/{b}" alt=""><figcaption>{esc(t)} · dator {pos}, mobil {posm}</figcaption></figure>' for _, b, t, pos, posm in BILDER)}</div>
</body>
</html>
'''
(ROT / "kontroll-om.html").write_text(kontroll, encoding="utf-8")
print("byggt om.html och kontroll-om.html;", len(P), "påståenden;", antal)
