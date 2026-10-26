// Prov 26 okt: huvudmenyn fastnar på alla sidor utom Funktioner, sidfoten utan menyrad, mobilmenyn, ankarmål.
// Kör: node prov-fast-meny.mjs (servern igång på 5520, eller BAS=...). Skärmbilder i skarmbilder/fast-meny-2026-10-26/.
import { chromium } from '/Users/adambrannstrom/Websites/Hantis-main/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const BAS = process.env.BAS || 'http://127.0.0.1:5520/';
const UT = 'skarmbilder/fast-meny-2026-10-26'; fs.mkdirSync(UT, { recursive: true });
const SIDOR = ['index.html', 'funktioner.html', 'media.html', 'priser.html', 'om.html', 'early-bird.html'];
const fel = []; const kolla = (v, t) => { if (!v) fel.push(t); console.log((v ? '  ok  ' : '  FEL ') + t); };
const b = await chromium.launch();
for (const [w, h, namn] of [[1440, 900, 'dator'], [390, 844, 'mobil']]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, hasTouch: w < 700 });
  const p = await ctx.newPage();
  p.on('pageerror', e => fel.push(`${namn}: ${e.message}`));
  console.log(`\n=== ${namn} ${w}x${h} ===`);
  for (const sida of SIDOR) {
    await p.goto(BAS + sida + (sida === 'funktioner.html' ? '?p=team' : '')); await p.waitForTimeout(500);
    const fot = await p.evaluate(() => ({ nav: !!document.querySelector('.fot nav'), brand: !!document.querySelector('.fot .brand'), liten: document.querySelector('.fot .liten')?.textContent || '' }));
    kolla(!fot.nav && fot.brand && /info@saefur\.com/.test(fot.liten) && /559556-4393/.test(fot.liten), `${sida}: sidfot utan menyrad, SAEFUR, support och bolag kvar`);
    await p.evaluate(() => window.scrollTo({ top: 1400, behavior: 'instant' })); await p.waitForTimeout(400);
    const m = await p.evaluate(() => {
      const hr = document.querySelector('.huvudrad').getBoundingClientRect(), st = document.getElementById('stang');
      const bg = getComputedStyle(document.querySelector('.huvudrad')).backgroundColor;
      return { topp: Math.round(hr.top), botten: Math.round(hr.bottom), bg, stang: st ? Math.round(st.getBoundingClientRect().top) : null,
        sidled: document.documentElement.scrollWidth > document.documentElement.clientWidth };
    });
    if (sida === 'funktioner.html') {
      kolla(m.botten <= 0 && m.stang === 0, `${sida}: huvudmenyn rullar bort (botten ${m.botten}), perspektivmenyn fast överst (${m.stang})`);
    } else {
      kolla(m.topp === 0 && m.bg !== 'rgba(0, 0, 0, 0)', `${sida}: huvudmenyn fast överst (topp ${m.topp}, höjd ${m.botten}) med bakgrund ${m.bg}`);
    }
    kolla(!m.sidled, `${sida}: ingen sidledsskroll`);
    if (sida === 'priser.html' || sida === 'funktioner.html') await p.screenshot({ path: `${UT}/${w}_${sida.replace('.html', '')}_rullad.png` });
    // Mobilmenyn, rullad
    if (w < 1080) {
      await p.click('.meny summary'); await p.waitForTimeout(200);
      const pm = await p.evaluate(() => { const r = document.querySelector('.meny .panel').getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom), h: innerHeight, lankar: document.querySelectorAll('.meny .panel a').length, vis: r.height > 0 }; });
      if (sida === 'funktioner.html') kolla(true, `${sida}: (menyn ligger överst på sidan, provas nedan)`);
      else kolla(pm.vis && pm.top >= 0 && pm.bottom <= pm.h && pm.lankar === 6, `${sida}: mobilmenyn öppnas rullad, ${pm.lankar} länkar inom skärmen (${pm.top} till ${pm.bottom})`);
      if (sida === 'om.html') await p.screenshot({ path: `${UT}/${w}_mobilmeny_rullad.png` });
      await p.click('.meny summary');
    }
    await p.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' })); await p.waitForTimeout(300);
    if (sida === 'index.html') await p.screenshot({ path: `${UT}/${w}_sidfot.png` });
  }
  // Ankarmål på Early Bird
  await p.goto(BAS + 'early-bird.html'); await p.waitForTimeout(400);
  await p.click('a[href="#villkor"]'); await p.waitForTimeout(1200);
  const a = await p.evaluate(() => ({ mal: Math.round(document.getElementById('villkor').getBoundingClientRect().top), meny: Math.round(document.querySelector('.huvudrad').getBoundingClientRect().bottom) }));
  kolla(a.mal >= a.meny, `early-bird.html: ankarmålet #villkor under menyn (mål ${a.mal}, menyns botten ${a.meny})`);
  await p.screenshot({ path: `${UT}/${w}_ankare_villkor.png` });
  // Funktioner: mobilmenyn överst och perspektivmenyn efter rullning
  if (w < 1080) {
    await p.goto(BAS + 'funktioner.html?p=team'); await p.waitForTimeout(500);
    await p.click('.meny summary'); await p.waitForTimeout(200);
    const fm = await p.evaluate(() => { const r = document.querySelector('.meny .panel').getBoundingClientRect(); return { vis: r.height > 0, top: Math.round(r.top), bottom: Math.round(r.bottom), over: document.elementFromPoint(r.left + 20, r.top + 20)?.closest('.panel') != null }; });
    kolla(fm.vis && fm.over, `funktioner.html: mobilmenyn öppnas överst och ligger över sidan (${fm.top} till ${fm.bottom})`);
    await p.screenshot({ path: `${UT}/${w}_funktioner_mobilmeny.png` });
    await p.click('.meny summary');
  }
  await ctx.close();
}
console.log('\nFEL:', fel.length ? '\n' + fel.join('\n') : 'inga');
await b.close(); process.exit(fel.length ? 1 : 0);
