# Bakgrund med produktfångster i långsam rörelse. Variant 2026-10-25 kväll, inget publicerat.
#
# Urval enligt Adams besked: bara fångster med diagram, tabeller, progresslinjer, faktarutor eller foton,
# inga rena textvyer. Bortvalda jämfört med varianten utan rörelse: Bokföring, Kundkort, Kundens följlänk,
# Aktivitet, Offert och Telefonen (text utan grafik). De äldre högupplösta fångsterna (Försäljning, Leverantörer
# med flera i rotmappens bilder/) är i en tidigare design och används inte.
#
# BILDER: nyckel, fil i bilder/, kort beskrivning (bara för kontrollsidan, aldrig synlig).
# Alla fångster visar exempelföretaget Nordanå Kök & Inredning AB med exempelpersoner och
# example-adresser, hämtade ur v3:s bildmapp. HR och Företaget saknar fångst i nuvarande design;
# Idag-vyn visar båda som rutor och får stå för bredden.
#
# GRUPPBILD: vilken bild som visas när en grupp är öppen, per perspektiv. I översikten växlar
# bilderna långsamt i ordningen nedan. Bilden driver alltid långsamt, även när den står stilla i en grupp.
# Vid minskad rörelse stannar både växling och drift.

BILDER = [
    ("idag", "prod-idag.jpg", "Idag: rutor per område med tal och stapel"),
    ("ekonomi", "prod-ekonomi.jpg", "Ekonomi: marginalmätare, lönsamhetstabell, nästa steg"),
    ("lager", "prod-lager.jpg", "Lager: tillgångsstapel, lagerrörelser per månad, tabeller"),
    ("fakturor", "prod-fakturor.jpg", "Fakturor: obetalt efter ålder som stapel, tabell"),
    ("kundservice", "prod-kundservice.jpg", "Kundservice: fördelningsstapel, stopp och avvikelser"),
    ("samarbeten", "prod-samarbeten.jpg", "Samarbeten: rutor, månatligt utfall som diagram"),
    ("projekt", "prod-projekt-foton.jpg", "Projekt: fototidslinje och meddelanden"),
]

GRUPPBILD = {
    "sjalv": dict(**{"fa-jobbet": "idag", "kunderna": "kundservice", "gora-jobbet": "projekt", "branschkrav": "projekt",
                     "material": "lager", "fa-betalt": "fakturor", "kunden-gor-sin-del": "projekt", "byran": "ekonomi",
                     "ta-hjalp": "samarbeten", "telefonen": "idag", "nar-ni-blir-fler": "idag"}),
    "team": dict(salja="idag", kunderna="kundservice", planera="projekt", ute="projekt", branschkrav="projekt",
                 material="lager", kontoret="fakturor", medarbetarna="idag", **{"kunden-deltar": "projekt"},
                 samarbeten="samarbeten", plattform="idag"),
    "avdelningar": dict(forsaljning="idag", kundservice="kundservice", projekt="projekt", kvalitet="projekt",
                        lager="lager", inkop="lager", ekonomi="ekonomi", hr="idag", ledning="ekonomi",
                        kund="projekt", partner="samarbeten", alla="idag"),
}

VAXLING_SEK = 9      # sekunder mellan bilderna i översikten
