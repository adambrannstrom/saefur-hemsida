# Start och Media med lanseringslagret (kopia av v4:s bygg.py, 25 okt 2026): python3 -I bygg/bygg_start_media.py i mappen lansering-2026-10-26.
# Funktioner, Priser och Om byggs av egna skript ur de godkända prototyperna. Gemensamt sidhuvud och sidfot i gemensamt.py.
# Sidhuvud, sidfot och skissrad är gemensamma; varje sida har sitt eget innehåll nedan.
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemensamt import LOGIN, EB, MENY, LANSERING, huvud, sidfot, skissrad, avslut_sektion, FORETAG  # noqa: E402


def sida(fil, titel, innehall, skript="", bakgrund=""):
    html = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titel}</title>
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="lansering.css">
</head>
<body{' class="med-bakgrund"' if bakgrund else ''}>
{bakgrund}{skissrad()}

{huvud(fil)}

<main>
{innehall}
</main>

{sidfot()}
{skript}
</body>
</html>
'''
    (ROT / fil).write_text(html, encoding="utf-8")


AVSLUT = avslut_sektion()

# ---------- Startsidan ----------
STEG = [
    ("01", "Överenskommet", "Kunden svarar på offerten via en länk.", "ut-lofte.jpg",
     "Offert markerad som godkänd, med timpris och uppskattat belopp"),
    ("02", "Genomfört", "Tid, material och foton följer uppdraget.", "prod-telefon.jpg",
     "Ett uppdrag i telefonen med rapporterad tid, foton och material"),
    ("03", "Fakturerat", "Fakturan bygger på underlaget, och betalningen följs upp.", "ut-betalt.jpg",
     "Fakturaöversikt med belopp kvar att betala och en påminnelse som väntar på godkännande"),
    ("04", "Överlämnat", "Redovisningspartnern får periodens underlag.", "ut-overlamnat.jpg",
     "Perioden före överlämning, med listan över det som behöver kompletteras"),
]
steg = "".join(f'''
      <li>
        <span class="punkt" aria-hidden="true"></span>
        <p class="nr">{n}</p>
        <h2>{h}</h2>
        <p class="kort">{t}</p>
        <div class="bild"><img src="bilder/{b}" alt="{a}"></div>
      </li>''' for n, h, t, b, a in STEG)

# Bakgrund bakom hela startsidan: situationsbilder som växlar. Första bilden visas direkt.
# Rörlig media: lägg <video autoplay muted loop playsinline poster="bilder/sit-ensam.jpg"><source src="..." type="video/mp4"></video>
# först i .bakgrund när filmen finns, och ta bort bilderna. Stilen täcker redan video.
BAKGRUNDSBILDER = [
    ("sit-ensam.jpg", "Hantverkare med telefonen vid servicebilen"),
    ("sit-kundmote.jpg", "Kundmöte utanför fastigheten"),
    ("sit-lager.jpg", "Plock i lagret"),
    ("sit-projekt.jpg", "Projektgenomgång över ritningen"),
    ("sit-team.jpg", "Teamet vid datorn"),
]
BAKGRUND = '<div class="bakgrund" aria-hidden="true">' + "".join(
    f'<img src="bilder/{b}" alt=""{" class=\"aktiv\"" if k == 0 else ""} title="{t}">' for k, (b, t) in enumerate(BAKGRUNDSBILDER)
) + "</div>\n"

VAXLA = '''<script>
// Växlar bakgrundsbild var åttonde sekund. Står stilla om besökaren har bett om minskad rörelse.
(function () {
  var bilder = document.querySelectorAll('.bakgrund img');
  if (bilder.length < 2 || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var i = 0;
  setInterval(function () {
    bilder[i].classList.remove('aktiv');
    i = (i + 1) % bilder.length;
    bilder[i].classList.add('aktiv');
  }, 8000);
})();
</script>'''

sida("index.html", "SAEFUR | Ett system för hela företaget", f'''<section class="hero">
  <div class="wrap hero-text">
    <h1>Ett system för<br><span>hela företaget.</span></h1>
    <p class="lead">SAEFUR samlar kunder, arbete, leveranser och ekonomi för projekt, tjänster, varor och löpande avtal. Ni ser vad som är överenskommet, genomfört, fakturerat och betalt, och kan fördela ansvaret och samtidigt följa helheten.</p>
    <div class="actions">
      <a class="btn stor" href="{EB}">Anmäl ditt företag till Early Bird</a>
      <a class="textlank" href="funktioner.html">Se hur SAEFUR fungerar</a>
    </div>
    <p class="mikro">{LANSERING}. Early Bird ger 20 % rabatt på licenserna i sex månader. <a class="textlank" href="early-bird.html#villkor">Villkor</a></p>
  </div>
</section>

<section class="kedja" aria-label="Från överenskommelse till överlämnat underlag i fyra steg">
  <div class="wrap">
    <ol class="steg">{steg}
    </ol>
    <p class="vidare"><a class="textlank" href="funktioner.html">Allt ni kan göra i SAEFUR</a> · <a class="textlank" href="funktioner.html?p=sjalv&amp;g=kunden-gor-sin-del">Så följer kunden arbetet</a></p>
  </div>
</section>''', VAXLA, BAKGRUND)

# ---------- Områden (rubrikerna ger Media-filmernas titlar; själva Funktioner-sidan byggs av bygg_funktioner.py) ----------
# Texterna bygger på v3:s områdessidor och produktens förmågekarta (avstämd 25 oktober 2026).
OMRADEN = [
    ("kunder", "Kunder", "Se kundens läge och låt en kollega ta vid.",
     "Kundkortet samlar kontaktpersoner, historik, offerter, avtal, beställningar, pågående arbete och fakturor. Löften och kundärenden sparas med ansvarig och återkopplingsdatum, och kundservice lyfter fram löften i fara, restorder utan besked och förfallen återkoppling. Via en personlig kundlänk ser kunden det som rör den egna affären, medan interna anteckningar och marginaler stannar hos er.",
     ["Kundregister och kontaktpersoner", "Kundhistorik", "Löften och återkopplingsdatum", "Kundärenden med ansvarig", "Kundservice", "Kundlänk", "Offerter, avtal och fakturor på kunden", "Obetalda belopp per kund"]),
    ("forsaljning", "Försäljning", "Följ affären från första kontakt till överenskommelse.",
     "Affärsmöjligheterna samlas på kunden med bedömt värde, sannolikhet och läge i försäljningen. Varje möjlighet har en ansvarig och ett nästa steg, och uppföljningen sparas i kundens historik. När erbjudandet är klart går affären vidare till offert, avtal, leverans och faktura, utan att något registreras om.",
     ["Affärsmöjligheter", "Bedömt värde och sannolikhet", "Läge i försäljningen", "Nästa kontakt och ansvarig", "Uppföljning i kundhistoriken", "Vidare till offert"]),
    ("offerter", "Offerter", "Skicka en offert och låt kunden svara via en länk.",
     "Offerten beskriver omfattning och pris och hör ihop med kund, kontaktperson och affär. Den skickas via en personlig offertlänk där kunden godkänner, avböjer eller lämnar motförslag, och svaret sparas på offerten. En accepterad offert blir grunden för avtalet, och tillägg under uppdraget blir nya ändringsförslag med pris som kunden tar ställning till.",
     ["Omfattning och pris", "Offertlänk", "Accept, avböjt och motförslag", "Avtal från accepterad offert", "Ändringsförslag med pris", "Koppling till affär och projekt"]),
    ("projekt", "Projekt", "Följ projektets kostnader och det som återstår att fakturera.",
     "Projektet byggs upp med projektmallar, aktiviteter, beroenden och Gantt, och utföraren ser sin dagsplan. Tid, resor och material registreras på aktiviteten i telefonen, med foton som dokumentation. ÄTA hålls samlade med pris, utförarens klarmarkering och beställarens godkännande är separata steg, och projektkostnad och marginal syns medan arbetet pågår.",
     ["Projektmallar och aktiviteter", "Beroenden och Gantt", "Dagsplan", "Tid, resor och material", "Fotodokumentation", "ÄTA", "Kundens godkännande", "Underleverantörer", "Projektkostnad och marginal", "Underlag till fakturering"]),
    ("fakturering", "Fakturering", "Fakturera arbetet och följ betalningen.",
     "Fakturaunderlaget hämtas från registrerat arbete och registrerade leveranser, och varje fakturarad går att följa till underlaget bakom den. Periodfakturor från löpande avtal, betalningsplaner och delbetalningar hanteras i samma flöde. Kunden betalar med Swish eller kort via fakturans betallänk. Påminnelser och dröjsmålskrav förbereds av systemet och skickas först när du godkänner.",
     ["Fakturaunderlag från arbete och leverans", "Periodfakturor", "Betalningsplaner och delbetalningar", "Granskning och godkännande", '<span class="bekrafta">Swish-QR</span> och kort', "Betalningsstatus", "Påminnelser och dröjsmålskrav", "Kreditering med spårbart underlag"]),
    ("ekonomi", "Ekonomi", "Följ resultatet medan månaden pågår.",
     "Ekonomin bygger på det som registreras i verksamheten varje dag. Du följer resultat och marginal per kund och projekt, skiljer utfört från fakturerat och betalt, och ser kommande utbetalningar i leverantörsfakturorna. Nästa ekonomiska steg visas bredvid lägesbilden, med kostnader att fördela och betalningar att stämma av, och perioden kontrolleras före överlämning till byrån.",
     ["Resultat och marginal", "Kostnad per affär och projekt", "Likviditetsbild", "Ekonomiska avvikelser", "Kostnadsfördelning", "Betalningsavstämning", "Periodkontroll", '<span class="bekrafta">SIE4 och läsplats för byrån</span>', ("Bankkoppling och likviditetsprognos", "kommer")]),
    ("leverantorer", "Leverantörer", "Följ inköpet från beställning till leverantörsfaktura.",
     "Avtal och prislistor samlas på leverantören, och inköpsordern anger antal och pris per rad. Varumottag registreras helt eller delvis, och leverantörsfakturan stäms av mot inköpsordern rad för rad, även vid delleveranser. Kostnaden knyts till projektet eller aktiviteten där den hör hemma. En underentreprenör som också använder SAEFUR fakturerar er direkt, och varje företag behåller sina interna uppgifter.",
     ["Leverantörsregister", "Avtal och prislistor", "Inköpsorder", "Hela och delvisa varumottag", "Avstämning mot inköpsorder", "Leverantörsfakturor och kvitton", "Attest", "Samarbete mellan företag"]),
    ("lager", "Lager &amp; artiklar", "Se lagersaldot innan ni lovar en leverans.",
     "Artikelregistret samlar artikelnummer, förpackningsenheter, streckkoder och GTIN, priser och leverantörer. Saldot visas tillsammans med reservationer och inkommande varor, så att säljaren vet vad som går att lova. Plock med skanning, delleveranser och restorder registreras per orderrad, med fraktsedel och leveransbesked till kunden.",
     ["Artikelregister", "Förpackningsenheter", "Streckkoder och GTIN", "Saldo och reservationer", "Inventering och partier", "Plock och skanning", "Delleveranser och restorder", "Fraktsedel och leveransbesked", ("Fraktbokning via fraktpartner", "kommer")]),
    ("hr", "HR", "Samla schema, frånvaro och löneunderlag.",
     "Anställningsuppgifter, avtalsmallar och handlingar samlas på personen, och organisationsöverblicken visar vem som ansvarar för vad. Tidrapportering, närvaro, frånvaro, utlägg och resor registreras på medarbetaren, och tiden kan samtidigt höra till ett projekt. Månadens löneunderlag samlas för lönepartnern, som sköter lönekörningen.",
     ["Anställningar och organisation", "Avtalsmallar", "Personalakt", "Roller och behörighet", "Tidrapportering och närvaro", "Frånvaro och ledighet", "Utlägg och resor", "Löneunderlag per månad"]),
    ("byran", "Byrån och lönepartnern", "Lämna periodens underlag till redovisningspartnern.",
     "Kundfakturor, leverantörsfakturor, kvitton och betalningar lämnas som SIE4-fil per period. Före överlämning visar SAEFUR vad som saknas eller är ofullständigt, så att kunden kompletterar innan byrån frågar. Byrån får en läsplats utan att räknas som en plats i kundens företag, och lönepartnern får löneunderlaget per månad. Bokslut, deklaration och lönekörning stannar hos er partner.",
     ["SIE4 per period", "Verifikat", "Periodkontroll", "Saknas eller ofullständigt", '<span class="bekrafta">Läsplats för byrån</span>', "Löneunderlag till lönepartnern"]),
]


# ---------- Media ----------
# Fyll i youtube med filmens id (delen efter v= i adressen) när filmen är publicerad.
FILMER = [
    ("Kom igång", [
        ("Ett system för hela företaget", "Introduktion till SAEFUR", ""),
        ("Från offert till byrån", "Överenskommet, genomfört, fakturerat och överlämnat", ""),
    ]),
    ("Område för område", [
        (n.replace("&amp;", "&amp;"), h, "") for _, n, h, *_ in OMRADEN
    ]),
]


def film(titel, text, yt):
    if yt:
        yta = f'<button class="yta" type="button" data-youtube="{yt}" aria-label="Spela filmen {titel}"><img src="https://i.ytimg.com/vi/{yt}/hqdefault.jpg" alt="" loading="lazy"><span class="spela"></span></button>'
        status = ""
    else:
        yta = '<div class="yta vantar"><span class="spela" aria-hidden="true"></span></div>'
        status = '<span class="status">Filmen läggs ut här när den är klar</span>'
    return f'<figure class="film">{yta}<figcaption><h3>{titel}</h3><p>{text}</p>{status}</figcaption></figure>'


media = "".join(f'''
<section class="sektion{" band" if k % 2 else ""}">
  <div class="wrap">
    <h2 class="rubrik">{rubrik}</h2>
    <div class="filmer">{"".join(film(*f) for f in lista)}</div>
  </div>
</section>''' for k, (rubrik, lista) in enumerate(FILMER))

SPELA = '''<script>
// Laddar YouTube först när besökaren klickar, via youtube-nocookie.
document.querySelectorAll('.yta[data-youtube]').forEach(function (knapp) {
  knapp.addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + knapp.dataset.youtube + '?autoplay=1&rel=0';
    f.allow = 'autoplay; encrypted-media; picture-in-picture';
    f.allowFullscreen = true;
    f.title = knapp.getAttribute('aria-label');
    knapp.replaceChildren(f);
  });
});
</script>'''

sida("media.html", "Media | SAEFUR", f'''<section class="hero sida">
  <div class="wrap hero-text">
    <h1>Media</h1>
    <p class="lead">Korta filmer om hur SAEFUR fungerar, från helheten till varje område. Börja med introduktionen och fördjupa dig sedan där du behöver.</p>
    <p class="mikro">Filmerna publiceras här och på <span class="bekrafta">SAEFURs YouTube-kanal</span> när de är klara.</p>
  </div>
</section>
<div style="height:48px"></div>
{media}
{AVSLUT}''', SPELA)

print("Byggt:", "index.html, media.html")
