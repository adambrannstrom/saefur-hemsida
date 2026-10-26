# Produktutsnitt i fördjupningen: skiss 2026-10-26, bara i skissbygget (SAEFUR_SKISS=1), aldrig i ordinarie bygge.
# Ett utsnitt per funktion: fil i bilder/utsnitt/ (beskuren ur samma produktfångster som bakgrunden,
# exempelföretaget Nordanå Kök & Inredning AB, demodata), bredd och höjd i pixlar, alt-text och bildtext.
# Beskärningen görs av bygg/skiss_produktutsnitt.py med sips ur bilder/prod-*.jpg (källa, offset och storlek nedan).

UTSNITT = {
    "faktura-ur-arbete": dict(
        fil="utsnitt-projekt-att-fakturera.jpg", kalla="prod-projekt-foton.jpg", x=400, y=20, bredd=990, hojd=400,
        alt="Projektet 2026-P2 Köksrenovering Björkvägen 12 i SAEFUR: alla fem aktiviteter är klara, projektet är markerat Att fakturera, och knappen Fakturera leder vidare.",
        text="Projektets huvud när arbetet är klart. Fem av fem aktiviteter är klara, projektet står som Att fakturera och knappen Fakturera skapar fakturan ur det godkända arbetet."),
    "plock-skanning": dict(
        fil="utsnitt-lager-plock-inkommande.jpg", kalla="prod-lager.jpg", x=1080, y=700, bredd=720, hojd=372,
        alt="Lagerkön i SAEFUR: Att plocka visar order 2026-A21 till Restaurang Hamnkrogen AB med 1 av 3 rader plockade, och Inkommande visar inköpsorder 2026-P5 från Vitvarugrossen AB som väntas.",
        text="Lagerkön. Under Att plocka ligger ordern med en av tre rader plockade och knappen Plocka. Under Inkommande väntar en inköpsorder med Ta emot."),
}
