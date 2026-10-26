// Skärmbilder av skissen med produktutsnitt (5523) på dator och mobil, plus kontroll av förstoringen.
// Kör: node prov-skiss-utsnitt.mjs   (skissens server igång: PORT=5523 node server.mjs i ../skiss-produktutsnitt-2026-10-26)
import { chromium } from '/Users/adambrannstrom/Websites/Hantis-main/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const BAS = process.env.BAS || 'http://127.0.0.1:5523/';
const UT = 'skarmbilder/skiss-produktutsnitt-2026-10-26';
fs.mkdirSync(UT, { recursive: true });
const fel = [];
const b = await chromium.launch();
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h } }); const p = await ctx.newPage();
  p.on('pageerror', e => fel.push(w + ': ' + e.message)); p.on('console', m => { if (m.type() === 'error') fel.push(w + ': ' + m.text()); });
  for (const [fm, g, namn] of [['faktura-ur-arbete', 'kontoret', 'faktura'], ['plock-skanning', 'material', 'plock']]) {
    await p.goto(`${BAS}funktioner.html?p=team&g=${g}&q=leverans#${fm}`); await p.waitForTimeout(1400);
    const bild = await p.$eval(`#${fm} .utsnitt img`, i => ({ w: i.clientWidth, nat: i.naturalWidth, alt: i.alt.length }));
    console.log(w, fm, 'bild visad', bild.w, 'px av', bild.nat, '| alt', bild.alt, 'tecken');
    await p.screenshot({ path: `${UT}/${w}_${namn}.png` });
    if (namn === 'faktura') {
      await p.click(`#${fm} [data-forstora]`); await p.waitForTimeout(400);
      await p.screenshot({ path: `${UT}/${w}_${namn}_forstorad.png` });
      const oppen1 = await p.$eval('#forstoring', d => d.open);
      await p.keyboard.press('Escape'); await p.waitForTimeout(200);
      const oppen2 = await p.$eval('#forstoring', d => d.open);
      await p.click(`#${fm} [data-forstora]`); await p.waitForTimeout(300);
      await p.click('#forstoring .stang-bild'); await p.waitForTimeout(200);
      const oppen3 = await p.$eval('#forstoring', d => d.open);
      console.log(w, 'förstoring: öppnad', oppen1, '| stängd med Escape', !oppen2, '| stängd med knappen', !oppen3);
      if (!(oppen1 && !oppen2 && !oppen3)) fel.push(w + ': förstoringen');
    }
  }
  await ctx.close();
}
console.log('FEL:', fel.length ? fel.join('\n') : 'inga');
await b.close();
