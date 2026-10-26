// Flödesprov för funktionssidan (sök, perspektivval, återvägar) i headless Chromium, på dator och mobil.
// Kör: node prov-funktioner.mjs   (servern igång: node server.mjs, port 5520). Skärmbilder i skarmbilder/funktioner-2026-10-26/.
// Provar Adams nio flöden från uppdraget 26 okt 2026 och skriver ut vad som händer; avvikelser samlas under FEL.
// Flöde 10 (samma kväll): förslagsytan vid fokus, centrerat perspektivval och förklaringen i utfällning.
import { chromium } from '/Users/adambrannstrom/Websites/Hantis-main/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const BAS = process.env.BAS || 'http://127.0.0.1:5520/';
const UT = 'skarmbilder/funktioner-2026-10-26';
fs.mkdirSync(UT, { recursive: true });
const fel = [];
const b = await chromium.launch();
const log = (...a) => console.log(...a);
const kolla = (villkor, text) => { if (!villkor) fel.push(text); log((villkor ? '  ok  ' : '  FEL ') + text); };

for (const [bredd, hojd, namn] of [[1440, 900, 'dator'], [390, 844, 'mobil']]) {
  const ctx = await b.newContext({ viewport: { width: bredd, height: hojd }, hasTouch: bredd < 700 });
  const p = await ctx.newPage();
  p.on('pageerror', e => fel.push(`${namn}: pageerror ${e.message}`));
  p.on('console', m => { if (m.type() === 'error') fel.push(`${namn}: ${m.text()}`); });
  const bild = n => p.screenshot({ path: `${UT}/${bredd}_${n}.png` });
  const lage = () => p.evaluate(() => ({
    url: location.search + location.hash, p: document.querySelector('.seg-knapp[aria-pressed=true]')?.dataset.p,
    panel: !document.getElementById('resultat').hidden, q: document.getElementById('q').value,
    omrade: document.getElementById('spar-har').textContent, kontextV: !document.querySelector('.kontext.vanster').hidden,
    traffar: document.querySelector('.kontext.hoger').hidden ? '' : document.getElementById('till-traffar').textContent.replace(/\s+/g, ' ').trim(),
    oppen: [...document.querySelectorAll('.fm[open]')].find(d => d.offsetParent)?.id || '', hjalp: document.getElementById('hjalp').hidden ? '' : document.getElementById('hjalp').textContent,
    forslag: !document.getElementById('sokforslag').hidden,
    fast: document.getElementById('stang').classList.contains('fast'), y: Math.round(window.scrollY),
    bredd: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  }));
  log(`\n=== ${namn} ${bredd}x${hojd} ===`);

  // 1. Öppna sidan och nå områdesöversikten via det kompakta perspektivvalet
  await p.goto(BAS + 'funktioner.html'); await p.waitForTimeout(600);
  let l = await lage();
  kolla(l.p === 'team' && !l.panel && !l.kontextV, `1 start: perspektiv ${l.p}, panel stängd, ingen områdeskontext`);
  kolla(!l.hjalp && !l.forslag, `1 start: ingen utfällning och ingen förslagsyta framme`);
  await bild('1_start');
  await p.click('.seg-knapp[data-p=sjalv]'); await p.waitForTimeout(500);
  l = await lage();
  kolla(l.p === 'sjalv' && l.url.startsWith('?p=sjalv'), `1 byte till Själv: ${l.url}, hjälp "${l.hjalp}"`);
  kolla(!l.bredd, '1 ingen sidledsskroll');
  await p.click('.seg-knapp[data-p=team]'); await p.waitForTimeout(400);

  // 2. Sök "leverans" via inskriven text och via sökordsknapp
  await p.click('#q'); await p.keyboard.type('leverans'); await p.waitForTimeout(500);
  l = await lage();
  const rubrik = await p.textContent('#res-rubrik');
  const grupper = await p.$$eval('#resultat .res-grupp h3', hs => hs.map(h => h.textContent.replace(/\s+/g, ' ').trim()));
  kolla(l.panel && /\d+ träffar i \d+ områden/.test(rubrik), `2 inskrivet: ${rubrik}; områden: ${grupper.join(' | ')}`);
  const antal = Number(rubrik.match(/^(\d+)/)[1]);
  const radAntal = await p.$$eval('#resultat a[data-fm]', as => as.length);
  kolla(radAntal === antal, `2 ${radAntal} rader i panelen = ${antal} i rubriken`);
  const synligTopp = await p.$eval('#resultat', e => { const r = e.getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom), h: Math.round(r.height) }; });
  kolla(synligTopp.bottom <= hojd + 1 && synligTopp.h >= 240, `2 panelen inom skärmen: topp ${synligTopp.top}, botten ${synligTopp.bottom} (skärm ${hojd})`);
  await p.waitForTimeout(900); await bild('2_sok_inskriven');
  await p.click('#rensa'); await p.waitForTimeout(200);
  l = await lage(); kolla(!l.panel && l.q === '' && !l.url.includes('q='), `2 rensa: fält tomt, panel stängd, adress ${l.url}`);
  await p.click('#q'); await p.click('#sokforslag .chip[data-q=leverans]'); await p.waitForTimeout(900);
  l = await lage(); kolla(l.panel && l.q === 'leverans' && l.url.includes('q=leverans'), `2 sökordsknapp: panel öppen, adress ${l.url}`);
  await bild('2_sok_knapp');

  // 3. Välj en träff, läs funktionen och återvänd till samma sökträffar
  await p.click('#resultat a[data-fm=mottagningsbekraftelse]'); await p.waitForTimeout(1200);
  l = await lage();
  kolla(!l.panel && l.oppen === 'mottagningsbekraftelse' && l.omrade === 'Kunden deltar', `3 träff öppnad: ${l.oppen} i "${l.omrade}", panel stängd, adress ${l.url}`);
  kolla(l.kontextV && /Sökträffarna \(\d+\)/.test(l.traffar), `3 bannern: Till områdesöversikten + "${l.traffar}"`);
  const fmPos = await p.$eval('#mottagningsbekraftelse', e => Math.round(e.getBoundingClientRect().top));
  const stangH = await p.$eval('#stang', e => e.getBoundingClientRect().height);
  kolla(fmPos >= stangH - 1 && fmPos < stangH + 60, `3 funktionen ligger under bannern: topp ${fmPos}, banner ${Math.round(stangH)}`);
  const fokus = await p.evaluate(() => document.activeElement?.closest('.fm')?.id || document.activeElement?.tagName);
  kolla(fokus === 'mottagningsbekraftelse', `3 fokus på funktionen: ${fokus}`);
  await bild('3_traff_oppnad');
  await p.click('#till-traffar'); await p.waitForTimeout(1200);
  l = await lage();
  kolla(l.panel && l.q === 'leverans' && l.kontextV, `3 tillbaka till sökträffarna: panel öppen, området kvar under ("${l.omrade}"), y=${l.y}`);
  const aktivt = await p.evaluate(() => document.activeElement?.id);
  kolla(aktivt === 'res-rubrik', `3 fokus på träffrubriken: ${aktivt}`);
  const sokPos = await p.$eval('#sokyta', e => Math.round(e.getBoundingClientRect().top));
  kolla(sokPos >= 0 && sokPos < 80, `3 sökområdet överst i läsläget: topp ${sokPos}`);
  await bild('3_tillbaka_till_traffar');

  // 4. Välj en träff och återvänd till områdesöversikten
  await p.click('#resultat a[data-fm=mottagningsbekraftelse]'); await p.waitForTimeout(1000);
  await p.click('#till-oversikt'); await p.waitForTimeout(1000);
  l = await lage();
  kolla(!l.kontextV && !l.oppen && !l.panel && l.q === 'leverans' && l.url.includes('q=leverans'), `4 till områdesöversikten: panel stängd, sökord kvar (${l.url})`);
  const kortPos = await p.$eval('#omr-team', e => Math.round(e.getBoundingClientRect().top));
  kolla(kortPos >= 0 && kortPos < 200, `4 områdeskorten i läsläget: topp ${kortPos}`);
  await bild('4_oversikt_efter_traff');
  await p.click('#q'); await p.waitForTimeout(900);
  l = await lage(); kolla(l.panel && l.q === 'leverans', `4 klick i fältet återöppnar panelen med sökordet`);

  // 5. Stäng panelen: klick utanför, Escape, scroll förbi sökområdet. Återöppna med sökordet bevarat.
  await p.mouse.click(6, 300); await p.waitForTimeout(200);   // i marginalen utanför sökområdet, även på mobil
  l = await lage(); kolla(!l.panel && l.q === 'leverans', `5 klick utanför stänger, sökord kvar`);
  await p.click('#q'); await p.waitForTimeout(600); await p.keyboard.press('Escape'); await p.waitForTimeout(200);
  l = await lage(); kolla(!l.panel && l.q === 'leverans', `5 Escape stänger, sökord kvar`);
  await p.click('#q'); await p.waitForTimeout(600); await p.mouse.move(bredd - 8, 150);
  await p.mouse.wheel(0, 1600); await p.waitForTimeout(700);
  l = await lage(); kolla(!l.panel && l.q === 'leverans', `5 scroll förbi sökområdet stänger (y=${l.y}), sökord kvar`);
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(400);
  await p.click('#q'); await p.waitForTimeout(600);
  l = await lage(); kolla(l.panel, `5 återöppnad med sökordet "${l.q}"`);
  // Rullning inne i listan ska behålla panelen
  await p.hover('#resultat .res-lista'); await p.mouse.wheel(0, 300); await p.waitForTimeout(400);
  l = await lage(); kolla(l.panel, `5 rullning inne i listan behåller panelen`);

  // 6. Rulla i en lång träfflista och välj den sista träffen
  await p.fill('#q', 'kund'); await p.waitForTimeout(600);
  const r6 = await p.textContent('#res-rubrik');
  const rullbar = await p.$eval('#resultat', e => e.classList.contains('rullbar'));
  log(`  6 "${r6}", intern rullning: ${rullbar}`);
  await bild('6_lang_lista');
  const sista = await p.$$eval('#resultat a[data-fm]', as => as[as.length - 1].dataset.fm);
  await p.evaluate(() => { const l = document.querySelector('#resultat .res-lista'); l.scrollTop = l.scrollHeight; }); await p.waitForTimeout(300);
  const vidSlutet = await p.$eval('#resultat', e => e.classList.contains('vid-slutet'));
  kolla(!rullbar || vidSlutet, `6 nedrullad lista markeras som vid slutet`);
  await bild('6_lang_lista_slut');
  await p.click(`#resultat a[data-fm="${sista}"]`); await p.waitForTimeout(1100);
  l = await lage(); kolla(l.oppen === sista && !l.panel, `6 sista träffen öppnad: ${sista} i "${l.omrade}"`);

  // 7. Byt perspektiv i fördjupning och översikt
  await p.click('.seg-knapp[data-p=avdelningar]'); await p.waitForTimeout(900);
  l = await lage(); kolla(l.p === 'avdelningar' && l.oppen === sista && l.omrade, `7 byte i fördjupning: samma funktion, område "${l.omrade}", hjälp "${l.hjalp}"`);
  const sokPers = await p.evaluate(() => document.querySelector('#resultat .res-pers')?.textContent);
  kolla(/flera avdelningar/.test(sokPers || ''), `7 sökträffarna följer perspektivet: "${sokPers}"`);
  await bild('7_byte_i_fordjupning');
  await p.click('#till-oversikt'); await p.waitForTimeout(800);
  await p.click('.seg-knapp[data-p=sjalv]'); await p.waitForTimeout(800);
  l = await lage(); kolla(l.p === 'sjalv' && !l.kontextV, `7 byte i översikt: ${l.url}`);
  if (bredd >= 1080) { await p.hover('.seg-knapp[data-p=avdelningar]'); await p.waitForTimeout(100); l = await lage(); kolla(/avdelning/.test(l.hjalp), `7 hovring visar hjälptext: "${l.hjalp}"`); await p.mouse.move(10, 10); }

  // 8. Tangentbord, direktlänk, omladdning, bakåt/framåt
  await p.goto(BAS + 'funktioner.html?p=team&q=leverans'); await p.waitForTimeout(800);
  l = await lage(); kolla(l.panel && l.q === 'leverans' && l.p === 'team', `8 omladdning med q: panelen öppen`);
  await p.focus('#q'); await p.keyboard.press('ArrowDown'); await p.waitForTimeout(100);
  let akt = await p.evaluate(() => document.activeElement?.dataset?.fm);
  kolla(!!akt, `8 pil ned från fältet fokuserar första träffen: ${akt}`);
  await p.keyboard.press('ArrowDown'); await p.keyboard.press('ArrowDown'); const tredje = await p.evaluate(() => document.activeElement?.dataset?.fm);
  await p.keyboard.press('Enter'); await p.waitForTimeout(1100);
  l = await lage(); kolla(l.oppen === tredje && !l.panel, `8 Enter öppnar fokuserad träff: ${tredje}`);
  await p.keyboard.press('Tab'); await p.keyboard.press('Shift+Tab');
  await p.goBack(); await p.waitForTimeout(1100);
  l = await lage(); kolla(l.panel && l.q === 'leverans' && !l.oppen, `8 bakåt: sökningen öppen igen (${l.url})`);
  await p.goForward(); await p.waitForTimeout(1100);
  l = await lage(); kolla(l.oppen === tredje && !l.panel, `8 framåt: funktionen igen (${l.url})`);
  await p.reload(); await p.waitForTimeout(1000);
  l = await lage(); kolla(l.oppen === tredje && !l.panel && /Sökträffarna/.test(l.traffar), `8 omladdning på en träff: funktion öppen, "${l.traffar}"`);
  await p.goto(BAS + 'funktioner.html?p=sjalv&g=fa-betalt'); await p.waitForTimeout(900);
  l = await lage(); kolla(l.p === 'sjalv' && l.kontextV && l.omrade === 'Få betalt' && !l.traffar, `8 direktlänk till område: "${l.omrade}", ingen sökåterväg`);
  await p.goto(BAS + 'funktioner.html#faktura-ur-arbete'); await p.waitForTimeout(1100);
  l = await lage(); kolla(l.oppen === 'faktura-ur-arbete' && l.kontextV, `8 direktlänk till funktion (perspektiv ur minnet ${l.p}): "${l.omrade}"`);
  await p.keyboard.press('Escape'); await p.waitForTimeout(800);
  l = await lage(); kolla(!l.kontextV, `8 Escape i område går till områdesöversikten`);

  // 9. Sticky banner: rubriker, fokus och klickmål synliga; layout i smal vy
  await p.goto(BAS + 'funktioner.html?p=team&g=kunden-deltar&q=leverans#mottagningsbekraftelse'); await p.waitForTimeout(1200);
  l = await lage();
  kolla(l.fast, `9 bannern fast efter rullning till funktionen`);
  const m9 = await p.evaluate(() => {
    const s = document.getElementById('stang').getBoundingClientRect();
    const f = document.getElementById('mottagningsbekraftelse').getBoundingClientRect();
    const h2 = document.querySelector('.grupp:not([hidden]) h2').getBoundingClientRect();
    return { banner: Math.round(s.height), fm: Math.round(f.top), h2: Math.round(h2.top), bredd: document.documentElement.scrollWidth > document.documentElement.clientWidth };
  });
  kolla(m9.fm >= m9.banner - 1 && !m9.bredd, `9 banner ${m9.banner}px, funktionens topp ${m9.fm}, områdesrubrik ${m9.h2}, sidledsskroll ${m9.bredd}`);
  await bild('9_sticky_i_omrade');
  await p.click('#till-oversikt'); await p.waitForTimeout(900);
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(500);
  l = await lage(); kolla(!l.fast, `9 bannern i flöde överst`);
  await bild('9_banner_i_flode');

  // 10. Förslagsytan, centrerat perspektivval och förklaringen i utfällning
  await p.goto(BAS + 'funktioner.html?p=team'); await p.waitForTimeout(700);
  l = await lage(); kolla(!l.forslag && !l.hjalp, `10 start: förslag och utfällning dolda`);
  const mitt = () => p.evaluate(() => { const r = document.querySelector('.seg').getBoundingClientRect(); return Math.round(r.left + r.width / 2 - document.documentElement.clientWidth / 2); });
  let avvik = await mitt(); kolla(Math.abs(avvik) <= 2, `10 perspektivvalet centrerat i översikten (avvikelse ${avvik}px)`);
  await p.click('#q'); await p.waitForTimeout(150);
  const fy = await p.evaluate(() => { const r = document.getElementById('sokforslag').getBoundingClientRect(); return { vis: !document.getElementById('sokforslag').hidden, v: Math.round(r.left), h: Math.round(r.right), n: document.querySelectorAll('#sokforslag .chip').length }; });
  kolla(fy.vis && fy.v >= 0 && fy.h <= bredd && fy.n === 8, `10 fokus i fältet visar förslagsytan med ${fy.n} sökningar inom skärmen (${fy.v} till ${fy.h})`);
  await bild('10_forslag');
  await p.keyboard.press('ArrowDown'); let fok = await p.evaluate(() => document.activeElement?.dataset?.q);
  kolla(fok === 'fakturera', `10 pil ned från fältet går till första förslaget: ${fok}`);
  await p.keyboard.press('Escape'); await p.waitForTimeout(100);
  l = await lage(); fok = await p.evaluate(() => document.activeElement?.id);
  kolla(!l.forslag && fok === 'q', `10 Escape stänger förslagsytan, fokus tillbaka i fältet`);
  await p.click('#q'); await p.keyboard.type('sie'); await p.waitForTimeout(300);
  l = await lage(); kolla(!l.forslag && l.panel, `10 skrivande byter förslagsytan mot träffpanelen`);
  await p.click('#rensa'); await p.waitForTimeout(150); l = await lage(); kolla(l.forslag && !l.panel, `10 rensa visar förslagen igen`);
  await p.click('h1'); await p.waitForTimeout(900); l = await lage(); kolla(!l.forslag, `10 klick utanför stänger förslagsytan`);
  const utfallKoll = (id) => p.evaluate((id) => {
    const u = document.getElementById('hjalp'), s = document.querySelector('.seg').getBoundingClientRect(), r = u.getBoundingClientRect();
    const b = document.querySelector(`.seg-knapp[data-p=${id}]`).getBoundingClientRect();
    return { vis: !u.hidden, text: u.textContent, underSeg: r.top >= s.bottom - 1, inom: r.left >= 0 && r.right <= document.documentElement.clientWidth,
      vidKnapp: r.left <= b.right && r.right >= b.left };
  }, id);
  for (const id of ['sjalv', 'team', 'avdelningar']) {
    if (bredd >= 1080) { await p.hover(`.seg-knapp[data-p=${id}]`); } else { await p.tap(`.seg-knapp[data-p=${id}]`); }
    await p.waitForTimeout(250);
    const u = await utfallKoll(id);
    kolla(u.vis && /Samma SAEFUR i alla tre/.test(u.text) && u.underSeg && u.inom && u.vidKnapp,
      `10 ${bredd >= 1080 ? "hovring" : "tryck"} ${id}: utfällning vid knappen, under valen, inom skärmen: "${u.text}" ${JSON.stringify({ ...u, text: undefined })}`);
    if (id === 'avdelningar') await bild('10_utfallning');
  }
  if (bredd >= 1080) {
    await p.mouse.move(10, 500); await p.waitForTimeout(100); l = await lage(); kolla(!l.hjalp, `10 musen bort stänger utfällningen`);
    await p.focus('#q'); await p.keyboard.press('Escape'); await p.keyboard.press('Tab');
    let tab = 0; while (tab++ < 20 && !(await p.evaluate(() => document.activeElement?.classList.contains('seg-knapp')))) await p.keyboard.press('Tab');
    const fid = await p.evaluate(() => document.activeElement?.dataset?.p);
    l = await lage(); kolla(fid && l.hjalp.length > 20, `10 tangentbordsfokus på ${fid} visar utfällningen`);
    await p.keyboard.press('Escape'); await p.waitForTimeout(50); l = await lage(); kolla(!l.hjalp, `10 Escape stänger utfällningen`);
    await p.goto(BAS + 'funktioner.html?p=sjalv&g=fa-betalt'); await p.waitForTimeout(900);
    avvik = await mitt(); kolla(Math.abs(avvik) <= 2, `10 perspektivvalet centrerat även i ett område (avvikelse ${avvik}px)`);
  } else {
    await p.tap('h1'); await p.waitForTimeout(100); l = await lage(); kolla(!l.hjalp, `10 tryck utanför stänger utfällningen`);
  }
  l = await lage(); kolla(!l.bredd, '10 ingen sidledsskroll');
  await ctx.close();
}
log('\nFEL:', fel.length ? '\n' + fel.join('\n') : 'inga');
await b.close();
process.exit(fel.length ? 1 : 0);
