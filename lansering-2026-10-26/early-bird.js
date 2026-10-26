// Early Bird-formuläret. Skickar bara till mottagningens adress i #data (MOTTAGNING i bygg/gemensamt.py).
// Fält enligt A:s /api/early-bird: email, companyName, locale, source, website. Svaret är {ok:true} även för dubblett.
// Bekräftelse visas bara när mottagningen själv svarar ok:true. Saknas adressen sägs det öppet och
// ingenting skickas. För många försök och avvisade uppgifter får egna besked. Vid serverfel och nätverksfel kan mottagningen
// ha sparat anmälan trots att svaret uteblev, så beskedet säger att bekräftelsen är osäker och hur man går vidare.
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var form = document.getElementById('eb-form');
  var epost = document.getElementById('eb-epost');
  var foretag = document.getElementById('eb-foretag');
  var fang = document.getElementById('eb-webb');
  var knapp = document.getElementById('eb-skicka');
  var status = document.getElementById('eb-status');
  var epostFel = document.getElementById('eb-epost-fel');
  var EPOST = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  if (!D.mottagning) document.getElementById('eb-ej-ansluten').hidden = false;

  function fel(el, text) { el.textContent = text; el.hidden = !text; }
  function visa(art, text) {
    status.className = 'eb-status ' + art;
    status.textContent = text;
    status.hidden = false;
    status.focus();
  }
  function kalla() {
    try {
      var r = document.referrer && new URL(document.referrer);
      if (r && r.origin === location.origin && r.pathname !== location.pathname) return r.pathname.replace(/^\//, '') || 'index.html';
    } catch (e) { /* ogiltig referrer */ }
    return 'early-bird.html';
  }

  epost.addEventListener('input', function () { fel(epostFel, ''); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.hidden = true;
    var adress = epost.value.trim();
    var ok = true;
    if (!EPOST.test(adress)) { fel(epostFel, adress ? 'Kontrollera e-postadressen.' : 'Ange en e-postadress.'); ok = false; }
    if (!ok) { epost.focus(); return; }

    if (!D.mottagning) {
      visa('info', 'Anmälan är inte ansluten ännu, så ingenting har skickats eller sparats. Skriv till info@saefur.com om du vill bli påmind när SAEFUR öppnar.');
      return;
    }

    knapp.disabled = true;
    knapp.textContent = 'Skickar…';
    var kropp = {
      email: adress,
      companyName: foretag.value.trim(),
      website: fang.value,
      source: kalla(),
      locale: 'sv'
    };
    fetch(D.mottagning, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(kropp),
      credentials: 'omit'
    }).then(function (svar) {
      return svar.json().catch(function () { return {}; }).then(function (json) { return { status: svar.status, ok: svar.ok, json: json }; });
    }).then(function (r) {
      if (r.ok && r.json && r.json.ok === true) {
        form.reset();
        visa('ok', 'Tack. Bekräfta anmälan med länken i mejlet som skickas till dig. Har du redan bekräftat en anmälan för den här adressen är allt klart.');
      } else if (r.status === 429) {
        visa('fel', 'Mottagningen tar emot många anmälningar just nu. Vänta en stund och försök igen. Den här anmälan har inte sparats.');
      } else if (r.status === 400 || r.status === 413 || r.status === 415) {
        visa('fel', 'Uppgifterna kunde inte tas emot. Kontrollera e-postadressen och försök igen. Den här anmälan har inte sparats.');
      } else {
        visa('fel', 'Vi kunde inte bekräfta att anmälan kom fram. Titta efter vårt mejl i inkorgen. Har inget mejl kommit om några minuter kan du skicka anmälan igen; samma adress registreras bara en gång. Du kan också skriva till info@saefur.com.');
      }
    }).catch(function () {
      visa('fel', 'Anslutningen bröts innan vi fick svar, så vi kan inte bekräfta att anmälan kom fram. Titta efter vårt mejl i inkorgen. Har inget mejl kommit om några minuter kan du skicka anmälan igen; samma adress registreras bara en gång. Du kan också skriva till info@saefur.com.');
    }).then(function () {
      knapp.disabled = false;
      knapp.textContent = 'Anmäl ditt företag';
    });
  });
})();
