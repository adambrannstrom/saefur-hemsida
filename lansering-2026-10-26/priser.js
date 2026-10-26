// Priser: räknare och bakgrund. Ren JavaScript, ingen server. 2026-10-25.
// Räknaren använder samma staffling som tabellen (data i #data). Varje pris gäller bara sitt intervall.
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var falt = document.getElementById('antal'), glid = document.getElementById('glid');
  var summa = document.getElementById('summa'), iord = document.getElementById('iord'), delar = document.getElementById('delar'), snitt = document.getElementById('snitt');
  var rader = Array.prototype.slice.call(document.querySelectorAll('#staffel li'));
  var knappar = Array.prototype.slice.call(document.querySelectorAll('[data-n]'));
  var MAX = 2000, GLID_MAX = Number(glid.max);
  var ORD = ['', 'en', 'två', 'tre', 'fyra', 'fem', 'sex', 'sju', 'åtta', 'nio', 'tio', 'elva', 'tolv'];

  function kr(n) { return n.toLocaleString('sv-SE') + ' kr'; }
  function tal(n) { return n < ORD.length ? ORD[n] : String(n); }
  function heltal(v) { var n = parseInt(v, 10); return isNaN(n) ? 1 : Math.max(1, Math.min(MAX, n)); }

  function rakna(n) {
    var total = 0, poster = [];
    D.steg.forEach(function (s, k) {
      var lo = s[0], hi = s[1] || n, p = s[2];
      var antal = Math.max(0, Math.min(n, hi) - lo + 1);
      rader[k].classList.toggle('i', antal > 0);
      rader[k].querySelector('.antal-i').textContent = antal > 0 ? (antal + ' användare') : '';
      if (antal) { total += antal * p; poster.push({ antal: antal, pris: p, namn: k === 0 ? 'Första licensen' : ('Användare ' + lo + (hi === n && !s[1] ? ' och uppåt' : ' till ' + hi)) }); }
    });

    summa.firstChild.nodeValue = kr(total) + ' ';

    // I ord: "Första licensen 995 kr, nio användare à 229 kr och tjugo användare à 179 kr. Tillsammans 6 636 kr per månad."
    var led = poster.map(function (x, k) {
      return k === 0 ? 'första licensen ' + kr(x.pris) : tal(x.antal) + ' användare à ' + kr(x.pris);
    });
    var mening;
    if (n === 1) mening = 'En användare: första licensen, ' + kr(total) + ' per månad.';
    else {
      var sista = led.pop();
      mening = (n === 2 ? 'Två användare: ' : tal(n).charAt(0).toUpperCase() + tal(n).slice(1) + ' användare: ') + led.join(', ') + ' och ' + sista + '. Tillsammans ' + kr(total) + ' per månad.';
    }
    iord.textContent = mening;

    // Uppdelning med stapel per intervall, andel av totalen
    delar.innerHTML = poster.map(function (x) {
      var belopp = x.antal * x.pris, andel = Math.max(2, Math.round(100 * belopp / total));
      return '<li style="--andel:' + andel + '%"><span>' + x.namn + ' · ' + x.antal + ' × ' + kr(x.pris) + '</span><b>' + kr(belopp) + '</b><i aria-hidden="true"></i></li>';
    }).join('');

    snitt.innerHTML = n > 1 ? 'I snitt <b>' + kr(Math.round(total / n)) + '</b> per användare och månad.' : '';

    knappar.forEach(function (b) { b.setAttribute('aria-pressed', String(Number(b.dataset.n) === n)); });
    glid.value = Math.min(n, GLID_MAX);
    if (String(n) !== falt.value) falt.value = n;
  }

  falt.addEventListener('input', function () { if (falt.value !== '') rakna(heltal(falt.value)); });
  falt.addEventListener('blur', function () { rakna(heltal(falt.value)); });
  glid.addEventListener('input', function () { rakna(heltal(glid.value)); });
  knappar.forEach(function (b) {
    b.addEventListener('click', function () {
      rakna(Number(b.dataset.n));
      if (b.classList.contains('ex')) document.getElementById('raknare').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  });

  var start = heltal(new URLSearchParams(location.search).get('n') || D.standard);
  rakna(start);

  // Bakgrund: växlar var nionde sekund med övertoning, driver långsamt (CSS). Står stilla vid minskad rörelse och i dold flik.
  var bilder = Array.prototype.slice.call(document.querySelectorAll('.bakgrund img'));
  if (bilder.length > 1 && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var i = 0, timer = null;
    function rotera() {
      if (timer) clearInterval(timer);
      timer = document.hidden ? null : setInterval(function () {
        bilder[i].classList.remove('aktiv'); i = (i + 1) % bilder.length; bilder[i].classList.add('aktiv');
      }, D.vaxling * 1000);
    }
    document.addEventListener('visibilitychange', rotera);
    rotera();
  }
})();
