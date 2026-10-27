// Funktioner med tre perspektiv: vyer i sidan, sök, adresser. Ren JavaScript, ingen server. 2026-10-25.
// Sök och navigering omgjorda 2026-10-26: sökpanel under fältet, ett perspektivval i en sticky banner med återvägar.
// Samma kväll: vanliga sökningar i en förslagsyta när fältet har fokus, perspektivets förklaring i en utfällning vid knappen.
//
// Prioritet vid sidöppning och omladdning: adressen (p, g, q, #funktion) går först, sedan sparat perspektiv i
// webbläsaren, sedan standardperspektivet. Sökordet lever bara i adressen (q) och i fältet; panelen öppnas vid start
// när adressen har q men ingen öppnad funktion eller område.
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var q = document.getElementById('q'), rensa = document.getElementById('rensa'), resultat = document.getElementById('resultat');
  var sokyta = document.getElementById('sokyta'), forslag = document.getElementById('sokforslag');
  var stang = document.getElementById('stang'), vakt = document.querySelector('.stang-vakt');
  var utfall = document.getElementById('hjalp'), hjalp = utfall.querySelector('.hjalp'), seg = stang.querySelector('.seg');
  var kontextV = stang.querySelector('.kontext.vanster'), kontextH = stang.querySelector('.kontext.hoger');
  var sparHar = document.getElementById('spar-har'), traffAntal = document.getElementById('traff-antal'), tillOversikt = document.getElementById('till-oversikt');
  var STANDARD = 'team';
  var P = {}; D.perspektiv.forEach(function (p) { P[p.id] = p; });
  var fmNamn = {}; D.funktioner.forEach(function (x) { fmNamn[x.id] = x.namn; });
  // gruppAv[p][fmId] = grupp-id, gruppNamn[p][gruppId] = namn, gruppOrdning[p] = grupp-id i visad ordning
  var gruppAv = {}, gruppNamn = {}, gruppOrdning = {};
  D.perspektiv.forEach(function (p) {
    gruppAv[p.id] = {}; gruppNamn[p.id] = {}; gruppOrdning[p.id] = [];
    p.grupper.forEach(function (g) { gruppNamn[p.id][g.id] = g.namn; gruppOrdning[p.id].push(g.id); g.ids.forEach(function (i) { gruppAv[p.id][i] = g.id; }); });
  });
  function html(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  // ---------- Bakgrund: långsam växling i översikten, områdets bild när en grupp är öppen ----------
  var bakgrund = (function () {
    var bilder = Array.prototype.slice.call(document.querySelectorAll('.bakgrund img'));
    var av = {}; bilder.forEach(function (b) { av[b.dataset.bild] = b; });
    var stilla = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var timer = null, i = 0, aktuell = D.bilder[0];
    function visa(nyckel) {
      if (!av[nyckel] || nyckel === aktuell) return;
      bilder.forEach(function (b) { b.classList.toggle('aktiv', b.dataset.bild === nyckel); });
      aktuell = nyckel;
    }
    function stopp() { if (timer) { clearInterval(timer); timer = null; } }
    function rotera() {
      stopp();
      if (stilla || document.hidden) return;
      timer = setInterval(function () { i = (D.bilder.indexOf(aktuell) + 1) % D.bilder.length; visa(D.bilder[i]); }, D.vaxling * 1000);
    }
    document.addEventListener('visibilitychange', function () { if (document.hidden) stopp(); else if (!lage.g) rotera(); });
    return {
      oversikt: function () { rotera(); },
      grupp: function (p, g) { stopp(); var n = D.gruppbild[p] && D.gruppbild[p][g]; if (n) visa(n); }
    };
  })();

  var lage = { p: null, g: null, fm: null, q: '' };   // var besökaren är: perspektiv, område, öppnad funktion, sökord
  var senasteFm = null;                               // senast öppnade funktion, följer med vid perspektivbyte
  var sok = { antal: null, omraden: 0 };              // senaste sökningens träffar, för "Till sökträffarna (n)"
  var panelOppen = false;
  var rullarTillSok = false, rullTimer = null;        // sidan rullas just nu upp till sökområdet av skriptet

  function minne(nyckel, varde) {
    try { if (varde === undefined) return localStorage.getItem(nyckel); localStorage.setItem(nyckel, varde); } catch (e) { return null; }
  }
  function sektion(p) { return document.getElementById('p-' + p); }
  function gruppEl(p, g) { return document.getElementById('g-' + p + '-' + g); }

  // ---------- Bannern: läge när den fastnat, förklaring i utfällning, återvägar ----------
  var fast = false;
  function matt() {
    document.documentElement.style.setProperty('--stang-h', (stang.offsetHeight + 12) + 'px');
    if (!utfall.hidden && utfallVid) placeraUtfall(utfallVid);
  }
  function sattFast(ny) {
    if (ny === fast) return;
    fast = ny;
    stang.classList.toggle('fast', fast);
    matt();
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (poster) {
      var e = poster[0];
      sattFast(!e.isIntersecting && e.boundingClientRect.top < 0);
    }, { threshold: 0 }).observe(vakt);
  }
  // Utfällningen: under den knapp den gäller, inom skärmen, och aldrig över de andra valen.
  // Mus: vid hovring. Tangentbord: vid fokus. Pekskärm: när perspektivet väljs, en stund eller tills man trycker utanför.
  var utfallVid = null, utfallTimer = null, senastePekare = 'mouse';
  function placeraUtfall(b) {
    var sr = stang.getBoundingClientRect(), br = b.getBoundingClientRect(), gr = seg.getBoundingClientRect();
    var bredd = utfall.offsetWidth, vw = document.documentElement.clientWidth;
    var mitt = br.left + br.width / 2, vanster = Math.min(Math.max(mitt - bredd / 2, 16), vw - bredd - 16);
    utfall.style.left = (vanster - sr.left) + 'px';
    utfall.style.top = (gr.bottom - sr.top + 10) + 'px';
    utfall.style.setProperty('--pil', Math.min(Math.max(mitt - vanster, 18), bredd - 18) + 'px');
  }
  function visaUtfall(b, sekunder) {
    clearTimeout(utfallTimer);
    hjalp.textContent = P[b.dataset.p].beskrivning;
    utfall.hidden = false; utfallVid = b;
    placeraUtfall(b);
    if (sekunder) utfallTimer = setTimeout(doljUtfall, sekunder * 1000);
  }
  function doljUtfall() { clearTimeout(utfallTimer); utfall.hidden = true; utfallVid = null; }
  function uppdateraBanner() {
    var iOmrade = !!lage.g;
    kontextV.hidden = !iOmrade;
    sparHar.textContent = iOmrade ? gruppNamn[lage.p][lage.g] : '';
    tillOversikt.setAttribute('href', '?p=' + lage.p);
    var harSok = !!(lage.q && sok.antal);
    kontextH.hidden = !(iOmrade && harSok);
    traffAntal.textContent = harSok ? '(' + sok.antal + ')' : '';
    stang.classList.toggle('i-omrade', iOmrade);
    matt();
  }
  stang.querySelectorAll('.seg-knapp').forEach(function (b) {
    b.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') visaUtfall(b); });
    b.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse' && utfallVid === b) doljUtfall(); });
    b.addEventListener('focus', function () { var tangent = false; try { tangent = b.matches(':focus-visible'); } catch (e) { } if (tangent) visaUtfall(b); });
    b.addEventListener('blur', function () { if (utfallVid === b && senastePekare !== 'touch') doljUtfall(); });
    b.addEventListener('click', function () {
      bytPerspektiv(b.dataset.p);
      if (senastePekare !== 'mouse') visaUtfall(b, 6);
      senastePekare = 'mouse';
    });
  });
  document.addEventListener('pointerdown', function (e) {
    senastePekare = e.pointerType === 'mouse' ? 'mouse' : 'touch';
    if (utfallVid && !seg.contains(e.target)) doljUtfall();
  }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && utfallVid) doljUtfall(); }, true);


  // ---------- Perspektiv ----------
  function flyttaRader(p) {
    var s = sektion(p);
    s.querySelectorAll('.lista-fm[data-ids]').forEach(function (lista) {
      lista.dataset.ids.split(' ').forEach(function (id) { var el = document.getElementById(id); if (el) lista.appendChild(el); });
    });
    // "Ligger också under" i varje rad: samma funktion i de andra perspektiven
    D.funktioner.forEach(function (x) {
      var el = document.getElementById(x.id); if (!el) return;
      var andra = D.perspektiv.filter(function (pp) { return pp.id !== p; }).map(function (pp) {
        return '<a href="?p=' + pp.id + '&g=' + gruppAv[pp.id][x.id] + '#' + x.id + '" data-byt="' + pp.id + '">' + html(pp.namn) + ' › ' + html(gruppNamn[pp.id][gruppAv[pp.id][x.id]]) + '</a>';
      });
      el.querySelector('[data-plats]').innerHTML = 'I de andra perspektiven: ' + andra.join(' · ');
    });
  }
  function visaPerspektiv(p) {
    if (!P[p]) p = STANDARD;
    if (lage.p === p) return;
    lage.p = p;
    document.querySelectorAll('.p').forEach(function (s) { s.hidden = s.dataset.p !== p; });
    document.querySelectorAll('.seg-knapp').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.p === p ? 'true' : 'false'); });
    flyttaRader(p);
    minne('saefur-perspektiv', p);
    if (lage.q) uppdatera();
  }

  // ---------- Vyer ----------
  function visaOversikt(rulla) {
    // rulla: false (ingen rullning), 'topp' (perspektivets rubrik) eller 'kort' (områdeskorten)
    var s = sektion(lage.p);
    s.querySelector('.oversikt').hidden = false;
    s.querySelectorAll('.grupp').forEach(function (g) { g.hidden = true; });
    document.querySelectorAll('.fm.mal').forEach(function (m) { m.classList.remove('mal'); });
    lage.g = null; lage.fm = null;
    bakgrund.oversikt();
    uppdateraBanner();
    if (rulla === 'kort') rullaTill(document.getElementById('omr-' + lage.p), 24);
    else if (rulla) rullaTill(s);
  }
  function visaGrupp(g, fm, rulla) {
    var el = gruppEl(lage.p, g);
    if (!el) { visaOversikt(rulla); return; }
    var s = sektion(lage.p);
    s.querySelector('.oversikt').hidden = true;
    s.querySelectorAll('.grupp').forEach(function (x) { x.hidden = x !== el; });
    lage.g = g;
    bakgrund.grupp(lage.p, g);
    document.querySelectorAll('.fm.mal').forEach(function (m) { m.classList.remove('mal'); });
    if (fm) {
      var f = document.getElementById(fm);
      if (f) {
        f.open = true; f.classList.add('mal'); lage.fm = fm; senasteFm = fm;
        uppdateraBanner();
        if (rulla) {
          // Fokus och rullning ihop: fokus utan egen rullning, sedan mjuk rullning som tar hänsyn till bannern.
          var sum = f.querySelector('summary');
          try { sum.focus({ preventScroll: true }); } catch (e) { }
          setTimeout(function () { f.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 20);
        }
        return;
      }
    }
    lage.fm = null;
    uppdateraBanner();
    if (rulla) rullaTill(el);
  }
  function stangHojd() { return parseInt(getComputedStyle(document.documentElement).getPropertyValue('--stang-h'), 10) || 80; }
  function rullaTill(el, extra) {
    var y = el.getBoundingClientRect().top + window.scrollY - stangHojd() - (extra || 0);
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
  }

  // ---------- Adresser: ?p=team&g=kontoret&q=leverans#faktura-ur-arbete ----------
  function adress(p, g, fm) {
    return location.pathname + '?p=' + p + (g ? '&g=' + g : '') + (lage.q ? '&q=' + encodeURIComponent(lage.q) : '') + (fm ? '#' + fm : '');
  }
  function ga(p, g, fm, satt, rulla) {
    // satt: 'push' (ny post i historiken), 'replace', 'start' eller 'ingen' (vid popstate).
    // rulla: hur översikten rullas (false, 'topp', 'kort'); ett område eller en funktion rullas alltid fram utom vid start.
    visaPerspektiv(p);
    if (g) visaGrupp(g, fm, true); else visaOversikt(rulla === undefined ? (satt !== 'start' ? 'topp' : false) : rulla);
    if (satt === 'push') history.pushState({}, '', adress(lage.p, lage.g, lage.fm));
    else if (satt === 'replace' || satt === 'start') history.replaceState(history.state || {}, '', adress(lage.p, lage.g, lage.fm));
  }
  function oppnaFm(id, satt) {
    var g = gruppAv[lage.p][id];
    if (!g) return;
    ga(lage.p, g, id, satt || 'push');
  }
  function bytPerspektiv(p) {
    if (p === lage.p) return;
    var fm = lage.fm || (lage.g ? senasteFm : null);
    if (lage.g && fm && gruppAv[p][fm]) ga(p, gruppAv[p][fm], fm, 'push');
    else if (lage.g) ga(p, null, null, 'push', 'kort');
    else ga(p, null, null, 'push', false);
  }
  function lasAdress() {
    var params = new URLSearchParams(location.search);
    var hash = decodeURIComponent(location.hash.slice(1));
    var p = params.get('p') || minne('saefur-perspektiv') || STANDARD;
    if (!P[p]) p = STANDARD;
    var g = params.get('g');
    var fm = hash && document.getElementById(hash) && document.getElementById(hash).classList.contains('fm') ? hash : null;
    if (fm) g = gruppAv[p][fm];
    if (g && !gruppNamn[p][g]) g = null;
    return { p: p, g: g, fm: fm, q: params.get('q') || '' };
  }

  // ---------- Sök: index ----------
  var STOPP = ['vad', 'är', 'kan', 'hur', 'finns', 'det', 'en', 'ett', 'i', 'på', 'med', 'och', 'att', 'för', 'som', 'ni', 'vi',
    'man', 'jag', 'till', 'av', 'om', 'utan', 'går', 'har', 'ska', 'den', 'de', 'er', 'vår', 'våra', 'min', 'mina', 'sin', 'sina', 'där', 'när', 'från', 'göra', 'gör'];
  function norm(s) { return (s || '').toLowerCase().replace(/[^a-z0-9åäöéü ]+/g, ' ').replace(/\s+/g, ' ').trim(); }
  function vik(s) { return s.replace(/[åä]/g, 'a').replace(/ö/g, 'o').replace(/é/g, 'e').replace(/ü/g, 'u'); }
  var index = {};
  D.funktioner.forEach(function (x) {
    var el = document.getElementById(x.id);
    var namn = norm(x.namn), sokord = norm(x.sok.join(' '));
    var text = vik(norm(x.namn + ' ' + x.sok.join(' ') + ' ' + el.querySelector('.vad').textContent + ' ' + el.querySelector('.nytta').textContent));
    index[x.id] = { text: ' ' + text + ' ', namn: ' ' + vik(namn) + ' ', sok: ' ' + vik(sokord) + ' ', ord: vik(sokord).split(' ').filter(function (w) { return w.length >= 6; }) };
  });
  var gIndex = D.granser.map(function (g) { return { g: g, text: ' ' + vik(norm(g.namn + ' ' + g.text)) + ' ', ord: vik(norm(g.namn)).split(' ').filter(function (w) { return w.length >= 6; }) }; });
  function tokenMatch(ix, t) {
    if (t.length <= 3) return ix.text.indexOf(' ' + t + ' ') !== -1;
    if (ix.text.indexOf(t) !== -1) return true;
    return ix.ord.some(function (w) { return t.length > w.length && t.indexOf(w) !== -1; });
  }
  function matchar(ix, tk) { return tk.every(function (t) { return tokenMatch(ix, t); }); }
  function rang(ix, tk) { var r = 0; tk.forEach(function (t) { r += ix.namn.indexOf(t) !== -1 ? 3 : ix.sok.indexOf(t) !== -1 ? 2 : 1; }); return r; }
  function tokens() { return vik(norm(q.value)).split(' ').filter(function (t) { return t.length >= 2 && STOPP.indexOf(t) === -1; }); }
  var chips = Array.prototype.slice.call(forslag.querySelectorAll('.chip'));
  var exempelOrd = chips.map(function (c) { return c.dataset.q; });

  // ---------- Sök: panelens innehåll ----------
  var MAX = 40;
  function uppdatera() {
    var tk = tokens(), soker = q.value.trim().length > 0;
    rensa.hidden = !soker;
    lage.q = soker ? q.value.trim() : '';
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.q.toLowerCase() === lage.q.toLowerCase() ? 'true' : 'false'); });
    if (!soker) { sok = { antal: null, omraden: 0 }; resultat.innerHTML = ''; uppdateraBanner(); return;
    }
    var traffar = [];
    D.funktioner.forEach(function (x) { if (tk.length && matchar(index[x.id], tk)) traffar.push({ x: x, r: rang(index[x.id], tk) }); });
    traffar.sort(function (a, b) { return b.r - a.r || a.x.namn.localeCompare(b.x.namn, 'sv'); });
    traffar = traffar.slice(0, MAX);
    var utanfor = tk.length ? gIndex.filter(function (ix) { return matchar(ix, tk); }) : [];
    var ut = utanfor.length ? '<p class="utanfor"><b>Sköts utanför SAEFUR:</b> ' + utanfor.map(function (ix) { return '<b>' + html(ix.g.namn) + '.</b> ' + html(ix.g.text); }).join(' ') + '</p>' : '';
    // Gruppera per område i perspektivets ordning; inom området efter rang
    var per = {}; traffar.forEach(function (t) { var g = gruppAv[lage.p][t.x.id]; (per[g] = per[g] || []).push(t); });
    var grupper = gruppOrdning[lage.p].filter(function (g) { return per[g]; });
    sok = { antal: traffar.length, omraden: grupper.length };
    if (traffar.length) {
      var rubrik = traffar.length + (traffar.length === 1 ? ' träff' : ' träffar') + ' i ' + grupper.length + (grupper.length === 1 ? ' område' : ' områden');
      resultat.innerHTML = '<div class="res-huvud"><h2 id="res-rubrik" tabindex="-1">' + rubrik + '</h2><p class="res-pers">Ordnade som i perspektivet <b>' + html(P[lage.p].namn) + '</b></p></div>' +
        '<div class="res-lista">' + grupper.map(function (g) {
          return '<section class="res-grupp"><h3>' + html(gruppNamn[lage.p][g]) + ' <span>' + per[g].length + '</span></h3><ul>' + per[g].map(function (t) {
            return '<li><a href="' + adress(lage.p, g, t.x.id) + '" data-fm="' + t.x.id + '"><span class="namn">' + html(t.x.namn) + '</span><span class="stod">' + html(t.x.nytta) + '</span></a></li>';
          }).join('') + '</ul></section>';
        }).join('') + ut + '</div>' +
        '<p class="res-fot"><span class="mer">Rulla för fler träffar</span><span class="tangenter">Enter öppnar den första träffen · pil ned och upp flyttar · Esc stänger</span></p>';
    } else {
      resultat.innerHTML = '<div class="res-huvud"><h2 id="res-rubrik" tabindex="-1">Inga träffar på ”' + html(lage.q) + '”</h2></div>' +
        '<div class="res-lista"><p class="inget">Prova ett kortare ord eller ett annat ord för samma sak, välj ett av orden nedan, eller bläddra bland områdena under sökningen.</p>' +
        '<p class="inget-chips">' + exempelOrd.map(function (e) { return '<button type="button" class="chip" data-q="' + html(e) + '">' + html(e) + '</button>'; }).join('') + '</p>' +
        '<p class="inget mikro">Hittar du ändå inget? <a href="mailto:info@saefur.com?subject=Fr%C3%A5ga%20om%20SAEFUR">Fråga oss</a>, så svarar vi hur SAEFUR stöder ert arbete.</p>' + ut + '</div>';
    }
    uppdateraBanner();
    if (panelOppen) matta();
  }

  // ---------- Sök: panelens synlighet ----------
  function matta(forskjutning) {
    // Panelen får plats under fältet inom skärmen; listan rullar inuti när träffarna är fler.
    // forskjutning: så många pixlar sidan är på väg att rullas (panelen hamnar högre upp än den står just nu).
    var vv = window.visualViewport, hojd = vv ? vv.height : window.innerHeight;
    var topp = resultat.getBoundingClientRect().top - (vv ? vv.offsetTop : 0) - (forskjutning || 0);
    resultat.style.maxHeight = Math.max(240, Math.floor(hojd - topp - 16)) + 'px';
    var lista = resultat.querySelector('.res-lista');
    if (lista) {
      var rullbar = lista.scrollHeight > lista.clientHeight + 2;
      resultat.classList.toggle('rullbar', rullbar);
      slutKoll(lista);
    }
  }
  function slutKoll(lista) { resultat.classList.toggle('vid-slutet', lista.scrollTop + lista.clientHeight >= lista.scrollHeight - 8); }
  function oppnaPanel() {
    // Sökområdet lyfts till skärmens överkant när panelen annars får för lite plats eller ligger ovanför skärmen.
    if (!lage.q) return;
    if (!resultat.innerHTML) uppdatera();
    resultat.hidden = false; panelOppen = true;
    q.setAttribute('aria-expanded', 'true');
    var vv = window.visualViewport, hojd = vv ? vv.height : window.innerHeight;
    var sokTopp = sokyta.getBoundingClientRect().top, rum = hojd - resultat.getBoundingClientRect().top;
    var flytt = 0;
    if (sokTopp < 0 || (rum < 420 && sokTopp > 24)) {
      flytt = sokTopp - 24;
      rullaTillSok(Math.max(0, window.scrollY + flytt));
    }
    matta(flytt);
  }
  function rullaTillSok(mal) {
    // Egen rullning: panelen hålls öppen tills sidan är framme (scrollend, stillastående eller som längst två sekunder).
    rullarTillSok = true;
    clearTimeout(rullTimer);
    var framme = function () { if (!rullarTillSok) return; rullarTillSok = false; clearTimeout(rullTimer); window.removeEventListener('scrollend', framme); if (panelOppen) matta(); };
    window.addEventListener('scrollend', framme);
    rullTimer = setTimeout(framme, 2000);
    var senast = -1, koll = function () {
      if (!rullarTillSok) return;
      var y = Math.round(window.scrollY);
      if (y === senast || Math.abs(y - mal) < 2) framme(); else { senast = y; setTimeout(koll, 120); }
    };
    window.scrollTo({ top: mal, behavior: 'smooth' });
    setTimeout(koll, 120);
  }
  function stangPanel() {
    if (!panelOppen) return;
    resultat.hidden = true; panelOppen = false;
    q.setAttribute('aria-expanded', 'false');
  }
  function visaTraffar() {
    // Återväg från en läst träff: samma sökning, panelen öppen, sökområdet överst i läsläget, fokus på rubriken.
    uppdatera();
    oppnaPanel();
    var r = document.getElementById('res-rubrik');
    if (r) { try { r.focus({ preventScroll: true }); } catch (e) { } }
  }
  function valjTraff(a) {
    // Ett träffklick: historikposten före träffen blir "sökningen öppen", så att Bakåt återöppnar panelen.
    history.replaceState({ sok: true }, '', adress(lage.p, lage.g, lage.fm));
    stangPanel();
    oppnaFm(a.dataset.fm, 'push');
  }
  function sparaSokord() { history.replaceState(history.state || {}, '', adress(lage.p, lage.g, lage.fm)); }
  var skrivTimer = null;

  // ---------- Sök: förslagsytan med vanliga sökningar, när fältet har fokus och är tomt ----------
  function visaForslag() { if (lage.q) return; forslag.hidden = false; }
  function doljForslag() { forslag.hidden = true; }
  forslag.addEventListener('keydown', function (e) {
    var knappar = chips, i = knappar.indexOf(document.activeElement);
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); (knappar[i + 1] || knappar[0]).focus(); }
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); if (i <= 0) q.focus(); else knappar[i - 1].focus(); }
    else if (e.key === 'Escape') { e.preventDefault(); q.focus(); doljForslag(); }   // efter fokus, som annars öppnar ytan igen
  });

  q.addEventListener('input', function () { uppdatera(); if (lage.q) { doljForslag(); oppnaPanel(); } else { stangPanel(); visaForslag(); } clearTimeout(skrivTimer); skrivTimer = setTimeout(sparaSokord, 300); });
  q.addEventListener('focus', function () { if (lage.q) oppnaPanel(); else visaForslag(); });
  q.addEventListener('click', function () { if (lage.q) oppnaPanel(); else visaForslag(); });
  q.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { var f = resultat.querySelector('a[data-fm]'); if (f) { e.preventDefault(); valjTraff(f); } }
    else if (e.key === 'ArrowDown' && panelOppen) { var f1 = resultat.querySelector('a[data-fm]'); if (f1) { e.preventDefault(); f1.focus(); } }
    else if (e.key === 'ArrowDown' && !forslag.hidden) { e.preventDefault(); chips[0].focus(); }
    else if (e.key === 'Escape') { e.preventDefault(); stangPanel(); doljForslag(); }
  });
  resultat.addEventListener('keydown', function (e) {
    var lankar = Array.prototype.slice.call(resultat.querySelectorAll('a[data-fm]'));
    var i = lankar.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); (lankar[i + 1] || lankar[0] || q).focus(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (i <= 0) q.focus(); else lankar[i - 1].focus(); }
    else if (e.key === 'Escape') { e.preventDefault(); stangPanel(); q.focus(); }
  });
  resultat.addEventListener('scroll', function (e) { if (e.target.classList && e.target.classList.contains('res-lista')) slutKoll(e.target); }, true);
  rensa.addEventListener('click', function () { q.value = ''; uppdatera(); stangPanel(); sparaSokord(); q.focus(); visaForslag(); });
  document.addEventListener('click', function (e) {
    var c = e.target.closest('.chip'); if (!c) return;
    q.value = c.dataset.q; uppdatera(); sparaSokord(); doljForslag(); oppnaPanel();
    var r = document.getElementById('res-rubrik'); if (r) { try { r.focus({ preventScroll: true }); } catch (x) { } }
  });
  // Stängs vid klick eller tryck utanför sökområdet, när fokus lämnar det, och när hela sökområdet rullat förbi.
  document.addEventListener('pointerdown', function (e) { if (!sokyta.contains(e.target)) { if (panelOppen) stangPanel(); doljForslag(); } });
  sokyta.addEventListener('focusout', function (e) { if (e.relatedTarget && !sokyta.contains(e.relatedTarget)) { if (panelOppen) stangPanel(); doljForslag(); } });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (poster) {
      var e = poster[0];
      if (!e.isIntersecting && e.boundingClientRect.bottom < 0) { doljForslag(); if (panelOppen && !rullarTillSok) stangPanel(); }
    }, { threshold: 0 }).observe(sokyta);
  }
  if (window.visualViewport) window.visualViewport.addEventListener('resize', function () { if (panelOppen) matta(); matt(); });
  window.addEventListener('resize', function () { if (panelOppen) matta(); matt(); });

  // ---------- Händelser i sidan ----------
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a, button');
    if (!a) return;
    if (a.dataset.kopiera) {
      e.preventDefault();
      var url = location.origin + adress(lage.p, lage.g || gruppAv[lage.p][a.dataset.kopiera], a.dataset.kopiera).replace(/&q=[^&#]*/, '');
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { a.classList.add('kopierad'); setTimeout(function () { a.classList.remove('kopierad'); }, 2000); });
      return;
    }
    if (a.hasAttribute('data-visa-traffar')) { e.preventDefault(); visaTraffar(); return; }
    if (a.dataset.byt) { e.preventDefault(); var id = a.getAttribute('href').split('#')[1]; ga(a.dataset.byt, gruppAv[a.dataset.byt][id], id, 'push'); return; }
    if (a.dataset.fm) { e.preventDefault(); if (a.closest('#resultat')) valjTraff(a); else oppnaFm(a.dataset.fm, 'push'); return; }
    if (a.dataset.g) { e.preventDefault(); ga(lage.p, a.dataset.g, null, 'push'); return; }
    if (a.dataset.till === 'oversikt') { e.preventDefault(); ga(lage.p, null, null, 'push', 'kort'); return; }
    if (a.hasAttribute('data-forstora')) { forstora(a); return; }
    if (a.hasAttribute('data-stang-bild')) { document.getElementById('forstoring').close(); return; }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' || panelOppen || sokyta.contains(document.activeElement)) return;
    var dlg = document.getElementById('forstoring'); if (dlg && dlg.open) return;
    if (lage.g) ga(lage.p, null, null, 'push', 'kort');
  });
  // Öppnad rad blir "senaste", så att ett perspektivbyte landar på samma funktion
  document.addEventListener('toggle', function (e) {
    var d = e.target; if (d.classList && d.classList.contains('fm') && d.open) { senasteFm = d.id; lage.fm = d.id; }
  }, true);
  window.addEventListener('popstate', function () {
    var a = lasAdress(), st = history.state || {};
    if (a.q !== lage.q) { q.value = a.q; uppdatera(); }
    if (st.sok && a.q && !a.g) { ga(a.p, null, null, 'ingen', false); visaTraffar(); }
    else { stangPanel(); ga(a.p, a.g, a.fm, 'ingen'); }
  });

  // ---------- Förstorad bild (skissen med produktutsnitt) ----------
  function forstora(knapp) {
    var dlg = document.getElementById('forstoring'); if (!dlg || !dlg.showModal) return;
    var img = knapp.querySelector('img'), fig = knapp.closest('figure');
    dlg.querySelector('img').src = img.currentSrc || img.src;
    dlg.querySelector('img').alt = img.alt;
    dlg.querySelector('.bildtext').textContent = fig ? fig.querySelector('figcaption').textContent : '';
    dlg.showModal();
    dlg.querySelector('.stang-bild').focus();
  }
  (function () {
    var dlg = document.getElementById('forstoring'); if (!dlg) return;
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  })();

  // ---------- Start ----------
  var start = lasAdress();
  if (start.q) q.value = start.q;
  ga(start.p, start.g, start.fm, 'start');
  if (start.q) uppdatera();                // efter perspektivet, eftersom träffarna grupperas per område i det
  matt();
  if (start.q && !start.g) { history.replaceState({ sok: true }, '', adress(lage.p, lage.g, lage.fm)); oppnaPanel(); }
})();
