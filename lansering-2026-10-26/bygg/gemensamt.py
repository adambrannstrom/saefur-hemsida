# Gemensamt lanseringslager för alla sidor i lansering-2026-10-26. Sidhuvud, sidfot, uppmaningar och mottagningens adress.
# Byggskripten importerar härifrån så att ordvalen (Early Bird, Inloggning för betatest, Lansering hösten 2026) står på ett ställe.
# 27 okt: menynamnet Funktioner blev "Vad ni kan göra" och Pilotinloggning blev "Inloggning för betatest" (Adams uppdrag);
# sidans adress funktioner.html och klassen pilot är oförändrade.
# Godkända mappar (v4, 5515, 5516, 5517) är orörda; detta är en separat kopia med lanseringslagret.

import os

LOGIN = "https://saefur.com/sv/login"
EB = "early-bird.html"
BETATEST = "betatest.html"
INLOGG = "Inloggning för betatest"
LANSERING = "Lansering hösten 2026"
FORETAG = "AT Interactive Design AB"
ORGSATE = "org.nr 559556-4393, säte Rättvik"

# Mottagningens adress (A:s POST-väg för Early Bird-anmälan). Tom tills A har byggt och Tobbe har bekräftat adressen.
# Standard är samma adress som produkten (Caddy). Prov mot A:s provinstans: EARLY_BIRD_MOTTAGNING=http://localhost:3988/api/early-bird. Tom adress gör att formuläret säger öppet att anslutningen saknas och ingenting skickas. Se ../09_publicering_och_anslutning.md.
MOTTAGNING = os.environ.get("EARLY_BIRD_MOTTAGNING", "/api/early-bird")

MENY = [("funktioner.html", "Vad ni kan göra"), ("media.html", "Media"), ("priser.html", "Priser"), ("om.html", "Om SAEFUR")]


def lansering_band():
    return (f'<div class="lansering"><div class="wrap"><span>{LANSERING}</span>'
            f'<a href="{EB}">Anmäl ditt företag till Early Bird</a></div></div>')


def skissrad(extra=""):
    return ('<div class="skissrad">Granskningsversion med lanseringslager, 25 oktober 2026 · lokalt, inget publicerat · '
            'Early Bird-formuläret skickar först när mottagningen är ansluten'
            f'{extra} · <a href="intern.html">intern översikt</a></div>')


def huvud(aktiv, fast=True):
    # fast: huvudmenyn fastnar i överkant vid rullning. Funktioner anger fast=False, eftersom sidan har en egen
    # fastnande perspektivmeny och två fastnande rader skulle ta för mycket av skärmen.
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == aktiv else ""}>{t}</a>' for h, t in MENY)
    panel = "".join(f'<a href="{h}">{t}</a>' for h, t in MENY)
    return f'''{lansering_band()}
<div class="huvudrad{' fast' if fast else ''}">
<header class="wrap head">
  <a class="brand" href="index.html">SAEFUR</a>
  <nav class="nav" aria-label="Huvudmeny">{nav}</nav>
  <div class="right">
    <a class="loggain pilot" href="{LOGIN}">{INLOGG}</a>
    <a class="btn mjuk" href="{EB}"{' aria-current="page"' if aktiv == EB else ''}>Early Bird</a>
    <details class="meny"><summary>Meny</summary>
      <div class="panel">{panel}<a href="{EB}">Early Bird</a><a href="{LOGIN}">{INLOGG}</a></div>
    </details>
  </div>
</header>
</div>'''


def sidfot(orgnr=ORGSATE):
    # Sidfotens menyrad borttagen 26 okt på Adams besked; huvudmenyn finns överst på varje sida.
    return f'''<footer class="fot">
  <div class="wrap">
    <div class="rad">
      <div><span class="brand">SAEFUR</span>Affärssystem för kunder, arbete, leveranser och ekonomi. {LANSERING}.</div>
    </div>
    <p class="liten">Support: info@saefur.com · {FORETAG}, {orgnr}</p>
  </div>
</footer>'''


def avslut_sektion():
    return f'''<section class="avslut">
  <div class="wrap">
    <h2>Börja där ni behöver överblick.</h2>
    <p class="lead" style="margin-left:auto;margin-right:auto">{LANSERING}. När SAEFUR öppnar kan ni börja med det område som behöver ordning först och lägga till fler i er egen takt. Early Bird ger 20 % rabatt på licenserna i sex månader.</p>
    <div class="actions"><a class="btn stor" href="{EB}">Anmäl ditt företag till Early Bird</a></div>
    <p class="mikro">Frågor eller en genomgång först? Skriv till info@saefur.com. Vill ni börja före lanseringen? <a class="textlank" href="{BETATEST}">Läs om betatestet</a></p>
  </div>
</section>'''
