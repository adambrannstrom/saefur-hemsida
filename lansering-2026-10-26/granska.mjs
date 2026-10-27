// Granskar lanseringsversionen i headless Chromium. Playwright lånas ur Hantis-main.
// Kör: node granska.mjs   (servern måste vara igång: node server.mjs, port 5520)
// Formulärprovet byter ut mottagningens adress i sidans data och svarar med en stubbe i testet. Stubben finns inte i sidan.
import { chromium } from '/Users/adambrannstrom/Websites/Hantis-main/node_modules/playwright/index.mjs';
const BAS = 'http://127.0.0.1:5520/';
const SIDOR = ['index.html', 'funktioner.html', 'media.html', 'priser.html', 'om.html', 'early-bird.html', 'betatest.html'];
const fel = [];
const b = await chromium.launch();
const log = (...a) => console.log(...a);
async function ny(bredd, hojd, namn) {
  const ctx = await b.newContext({ viewport: { width: bredd, height: hojd } });
  const p = await ctx.newPage();
  p.on('console', m => { if (m.type() === 'error') fel.push(`${namn}: ${m.text()}`); });
  p.on('pageerror', e => fel.push(`${namn}: pageerror ${e.message}`));
  p.on('requestfailed', r => fel.push(`${namn}: request ${r.url()}`));
  p.on('response', r => { if (r.status() >= 400 && r.url().startsWith(BAS)) fel.push(`${namn}: ${r.status()} ${r.url()}`); });
  return p;
}

for (const [bredd, hojd] of [[1440, 900], [390, 844]]) {
  const p = await ny(bredd, hojd, 'sida' + bredd);
  for (const s of SIDOR) {
    await p.goto(BAS + s); await p.waitForTimeout(700);
    const m = await p.evaluate(() => ({
      scroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      band: document.querySelector('.lansering')?.textContent.replace(/\s+/g, ' ').trim(),
      inloggning: [...document.querySelectorAll('header a')].filter(a => a.textContent.trim() === 'Inloggning för betatest').map(a => a.href),
      eb: [...document.querySelectorAll('header .right a.btn')].map(a => a.textContent.trim() + '→' + a.getAttribute('href')),
      gamla: document.body.innerText.match(/Prova nu|gratis provperiod|Logga in|Konto skapas i webbläsaren|Interaktiv|[Pp]ilot|Funktioner|127\.0\.0\.1:55/g),
      regLank: [...document.querySelectorAll('a')].filter(a => /sv\/register/.test(a.href)).length,
      rubrik: document.querySelector('h1')?.innerText.replace(/\n/g, ' '),
    }));
    log(bredd, s, JSON.stringify(m));
    await p.screenshot({ path: `skarmbilder/${bredd}_${s.replace('.html', '')}.png` });
  }
  await p.context().close();
}

// Menyn: klick på varje huvudmenylänk på dator, och via Meny-knappen på mobil
{
  const p = await ny(1440, 900, 'meny-dator');
  await p.goto(BAS + 'index.html');
  for (const t of ['Vad ni kan göra', 'Media', 'Priser', 'Om SAEFUR']) {
    await p.click(`header .nav a:has-text("${t}")`); await p.waitForTimeout(300);
    log('meny dator', t, '→', p.url().replace(BAS, ''), '| aktiv:', await p.textContent('header .nav a[aria-current=page]'));
  }
  await p.click('header .right a.btn'); await p.waitForTimeout(300); log('Early Bird-knapp →', p.url().replace(BAS, ''));
  await p.click('.lansering a'); log('bandets länk →', p.url().replace(BAS, ''));
  await p.click('header .brand'); log('logotyp →', p.url().replace(BAS, ''));
  await p.click('.hero .btn.stor'); log('startsidans knapp →', p.url().replace(BAS, ''));
  await p.context().close();
}
{
  const p = await ny(390, 844, 'meny-mobil');
  await p.goto(BAS + 'index.html');
  for (const t of ['Vad ni kan göra', 'Media', 'Priser', 'Om SAEFUR', 'Early Bird']) {
    await p.goto(BAS + 'index.html');
    await p.click('header details.meny summary'); await p.waitForTimeout(150);
    await p.click(`header .panel a:has-text("${t}")`); await p.waitForTimeout(300);
    log('meny mobil', t, '→', p.url().replace(BAS, ''));
  }
  await p.goto(BAS + 'index.html'); await p.click('header details.meny summary');
  log('mobilpanel:', (await p.$$eval('header .panel a', as => as.map(a => a.textContent.trim() + '→' + a.getAttribute('href')))).join(' | '));
  await p.screenshot({ path: 'skarmbilder/390_meny_oppen.png' });
  await p.context().close();
}

// Alla interna länkar på alla sidor ska gå till en sida som finns (med ankare)
{
  const p = await ny(1440, 900, 'lankar');
  const sedda = new Set();
  for (const s of [...SIDOR, 'intern.html', 'kontroll-funktioner.html', 'kontroll-priser.html', 'kontroll-om.html']) {
    await p.goto(BAS + s); await p.waitForTimeout(250);
    const lankar = await p.$$eval('a[href]', as => as.map(a => a.getAttribute('href')));
    for (const h of lankar) {
      if (/^(mailto:|https?:\/\/(?!127))|^#|^\?/.test(h)) continue;
      const [fil, ank] = h.split('#');
      if (!fil || sedda.has(h)) continue;
      sedda.add(h);
      const r = await p.request.get(BAS + fil);
      if (r.status() !== 200) fel.push(`länk ${s} → ${h}: ${r.status()}`);
      else if (ank && !(await r.text()).includes(`id="${ank}"`)) fel.push(`länk ${s} → ${h}: ankaret saknas`);
    }
  }
  log('interna länkar kontrollerade:', sedda.size);
  await p.context().close();
}

// Early Bird-formuläret, utan anslutning (som det byggs nu)
{
  const p = await ny(1440, 900, 'eb-utan');
  let skickat = 0;
  p.on('request', r => { if (r.method() === 'POST') skickat++; });
  await p.route('**/early-bird.html', async r => { const resp = await r.fetch(); await r.fulfill({ response: resp, body: (await resp.text()).replace(/"mottagning": "[^"]*"/, '"mottagning": ""') }); });
  await p.goto(BAS + 'early-bird.html');
  log('EB utan anslutning, notis synlig:', await p.isVisible('#eb-ej-ansluten'));
  await p.click('#eb-skicka'); log('tomt →', await p.textContent('#eb-epost-fel'));
  await p.fill('#eb-epost', 'fel'); await p.click('#eb-skicka'); log('ogiltig →', await p.textContent('#eb-epost-fel'));
  await p.fill('#eb-epost', 'test@example.com'); await p.click('#eb-skicka'); await p.waitForTimeout(200);
  log('ifylld utan anslutning →', await p.textContent('#eb-status'), '| klass', await p.getAttribute('#eb-status', 'class'), '| POST skickade:', skickat);
  await p.screenshot({ path: 'skarmbilder/1440_early-bird_utan_anslutning.png' });
  await p.context().close();
}

// Early Bird-formuläret mot en stubbe i testet efter A:s gränssnitt: ok:true, svar utan ok, 429, 400, 403, 500, nätverksfel
{
  const URL_STUB = 'http://127.0.0.1:5599/api/early-bird';
  for (const fall of [
    { namn: 'ok med e-post', status: 200, json: { ok: true } },
    { namn: 'ok utan flagga', status: 200, json: {} },
    { namn: '429', status: 429, json: { ok: false, error: 'rate_limited' } },
    { namn: '400', status: 400, json: { ok: false, error: 'invalid_email' } },
    { namn: '403', status: 403, json: { ok: false, error: 'origin_not_allowed' } },
    { namn: '500', status: 500, json: { ok: false } },
    { namn: 'nätverksfel', abort: true },
  ]) {
    const p = await ny(390, 844, 'eb-stub');
    let kropp = null;
    await p.route('**/early-bird.html', async r => {
      const resp = await r.fetch(); const t = (await resp.text()).replace(/"mottagning": "[^"]*"/, `"mottagning": "${URL_STUB}"`);
      await r.fulfill({ response: resp, body: t });
    });
    await p.route(URL_STUB, async r => {
      if (r.request().method() === 'OPTIONS') return r.fulfill({ status: 204, headers: { 'access-control-allow-origin': '*', 'access-control-allow-headers': 'content-type, accept' } });
      kropp = r.request().postDataJSON();
      if (fall.abort) return r.abort('failed');
      await r.fulfill({ status: fall.status, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify(fall.json) });
    });
    await p.goto(BAS + 'early-bird.html');
    log(`stubbe ${fall.namn}: notis om saknad anslutning dold:`, !(await p.isVisible('#eb-ej-ansluten')));
    await p.fill('#eb-epost', '  Ada@Example.com '); await p.fill('#eb-foretag', 'Ada Bygg AB');
    await p.click('#eb-skicka'); await p.waitForTimeout(400);
    log(`  → ${await p.textContent('#eb-status')} | klass ${await p.getAttribute('#eb-status', 'class')} | knapp ${await p.textContent('#eb-skicka')} | epostfält efter: "${await p.inputValue('#eb-epost')}"`);
    log('  skickat:', JSON.stringify(kropp));
    if (fall.namn === 'ok med e-post') await p.screenshot({ path: 'skarmbilder/390_early-bird_ok.png' });
    await p.context().close();
  }
}

// Honungskruka: ifyllt dolt fält skickas med (mottagningen ska avvisa tyst); fältet syns inte
{
  const p = await ny(1440, 900, 'fang');
  await p.goto(BAS + 'early-bird.html');
  const r = await p.$eval('#eb-webb', e => { const b = e.getBoundingClientRect(); return { x: b.x, w: b.width, tab: e.tabIndex }; });
  log('honungskruka utanför bild:', JSON.stringify(r));
  await p.context().close();
}

log('FEL:', fel.length ? '\n' + fel.join('\n') : 'inga');
await b.close();
