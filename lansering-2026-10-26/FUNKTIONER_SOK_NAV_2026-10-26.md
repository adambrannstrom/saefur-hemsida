# Funktioner: sök, perspektivval och återvägar, 26 oktober 2026

Lokalt, inget publicerat. Granskningsversion: http://127.0.0.1:5520/funktioner.html. Skiss med produktutsnitt: http://127.0.0.1:5523/funktioner.html (mappen `../skiss-produktutsnitt-2026-10-26/`).

## Beteende

**Perspektivvalet.** En enda kompakt kontroll (Jag driver företaget själv · Vi delar på arbetet · Vi har flera avdelningar) i den mörkblå bannern direkt under sökningen. Under knapparna en hjälprad som visar det valda perspektivets beskrivning, och vid hovring eller tangentbordsfokus det perspektiv som pekas på; därunder undertexten "Samma SAEFUR i alla tre. Perspektivet väljer ordningen, och innehållet är detsamma." Bannern fastnar vid sidans överkant och blir då kompakt (hjälpraderna fälls in, deras höjd reserveras som marginal så att innehållet står stilla). På mobil kortnamn: Själv · Delat arbete · Avdelningar.

**Sökpanelen.** Träffarna visas i en täckande panel under sökfältet och de vanliga sökorden: rubrik "13 träffar i 4 områden", träffarna grupperade under områdesrubriker i det valda perspektivets ordning, varje funktion som en egen rad med namn och en rad stödtext (funktionens nytta). Panelens höjd anpassas till skärmen; listan rullar inuti med toning och "Rulla för fler träffar". När panelen annars hamnar för långt ned lyfts sökområdet till skärmens överkant. Noll träffar ger ett besked med de vanliga sökorden och "Fråga oss". Enter öppnar första träffen, pil ned och upp flyttar mellan träffarna, Esc stänger och behåller ordet.

**Stängning.** Träffklick, klick eller tryck utanför sökområdet, fokus som lämnar sökområdet, Escape, eller att hela sökområdet (fält och sökord) rullat ovanför skärmen. Rullning inne i listan och skriptets egen rullning till sökområdet stänger inte. Klick eller fokus i fältet visar träffarna igen för det sparade ordet; Rensa tömmer fältet och sökningen.

**Återvägar i bannern.** I översikten: bara perspektivvalet och undertexten. I ett område eller en öppnad funktion: knappen "Till områdesöversikten" och en markering "Område · Kunden deltar". När en sökning med träffar finns sparad visas dessutom "Till sökträffarna (13)", som återöppnar samma sökning, lyfter sökområdet överst och sätter fokus på träffrubriken. "Till områdesöversikten" rullar till områdeskorten för valt perspektiv och behåller sökordet med panelen stängd. Brödsmulan, sökspåret och "Tillbaka till översikten" inne i området är borttagna; grannarna längst ned (Föregående · Till områdesöversikten · Nästa) finns kvar. Genvägen "Sök" i bannern är borta.

**Träffval.** Panelen stängs, området öppnas, funktionen expanderas med guldram, fokus flyttas till funktionens rubrik utan egen rullning, och sidan rullas så att funktionen ligger direkt under bannern (`scroll-padding-top` följer bannerns kompakta höjd).

**Adresser och historik.** Prioritet vid öppning och omladdning: adressen (`?p`, `&g`, `&q`, `#funktion`) går först, sedan sparat perspektiv i webbläsaren, sedan standardperspektivet. Sökordet skrivs i adressen medan man skriver. Ett träffklick gör posten före till "sökningen öppen", så att Bakåt återöppnar panelen; Framåt visar funktionen igen. Omladdning på en träff ger funktionen öppen med "Till sökträffarna (13)" i bannern. Direktlänkar till funktion, område och perspektiv fungerar som förut.

## Ett steg längre än uppdraget

- Bannern är generös i flödet (hjälprad och undertext) och kompakt när den fastnat, utan att innehållet hoppar.
- Varje träff har stödtext så att besökaren kan välja rätt innan klicket; områdesrubriken har antal.
- Pil ned och upp mellan träffarna; aktivt sökord markeras bland de vanliga sökorden.
- Noll träffar erbjuder de vanliga sökorden direkt i panelen.
- Områdesvyn har en navigering i stället för tre (banner i stället för brödsmula, sökspår och tillbaka-länk).

## Skissen: produktutsnitt i fördjupningen

Två funktioner i skissen, båda träffar på "leverans":
- **Faktura ur arbete och leverans** (Fakturering och ekonomi): projektets huvud ur produkten med "Alla aktiviteter är klara. Att fakturera. 5 av 5 klara" och knappen Fakturera. Visar att fakturan skapas ur det godkända arbetet, inte skrivs från ett tomt blad.
- **Plock med skanning, packning och avsändning** (Material, inköp och lager): lagerkön med Att plocka (order med 1 av 3 rader plockade) och Inkommande (inköpsorder som väntas, Ta emot). Visar vad "lagerkön" är.

Utsnitten är beskurna med sips ur samma produktfångster som bakgrunden (Nordanå Kök & Inredning AB, demodata, inga personnamn i utsnitten), ligger i en diskret mörk inramning med bildtext "Ur SAEFUR: …" och "Exempelföretag med demodata", har beskrivande alt-text och går att förstora i en dialog (Esc, stängknapp, klick utanför). Adresser: `?p=team&g=kontoret&q=leverans#faktura-ur-arbete` och `?p=team&g=material&q=leverans#plock-skanning` på 5523.

## Kontroller

`python3 -I bygg/bygg_alla.py` (bara den kända varningen " inte " i Adams gallringstext), `node granska.mjs` (inga fel, 161 interna länkar), `python3 -I sprakgranskning/kontrollera_sprak.py` (0 spärrar, 19 att bedöma, alla kända i Early Bird), `node prov-funktioner.mjs` (alla nio flöden på 1440 och 390 utan fel), `node prov-skiss-utsnitt.mjs` (förstoringen öppnas och stängs).

Skärmbilder: `skarmbilder/funktioner-2026-10-26/` (sökpanel, kompakt perspektivkontroll, öppnad funktion med återvägar, lång lista, noll träffar) och `skarmbilder/skiss-produktutsnitt-2026-10-26/` (dator och mobil, med förstoring).

## Avvägningar att besluta

1. "Till sökträffarna" lämnar området kvar under panelen (stänger man panelen står man överst på sidan med bannern som fortfarande visar området). Alternativet är att gå till översikten samtidigt.
2. Upplösningen på utsnitten är begränsad av fångsterna (1920 och 2400 px breda); på dator visas de i 686 px, så texten är läsbar men mjuk vid förstoring. Skarpare fångster ur demomiljön ger bättre resultat om utsnitt införs brett.
3. Stödtexten i träffarna är funktionens nytta, klippt till en rad. Vill du hellre ha rena namn tas en rad CSS bort.
4. Filen `bilder/foto-01-pa-vag-till-kund.jpg` ligger kvar i mappen men används inte längre; den följer med i en publik utgåva tills den tas bort.
