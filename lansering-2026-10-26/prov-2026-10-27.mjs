// Skärmbilder 27 okt: berörda sidor på 1440, 1100 och 390, helsida. node prov-2026-10-27.mjs (5520 igång)
import { chromium } from '/Users/adambrannstrom/Websites/Hantis-main/node_modules/playwright/index.mjs';
const BAS = process.env.BAS || 'http://127.0.0.1:5520/';
const b = await chromium.launch();
for (const [w, h] of [[1440, 900], [1100, 800], [390, 844]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  for (const s of ['funktioner', 'priser', 'om', 'early-bird', 'betatest', 'index']) {
    await p.goto(BAS + s + '.html'); await p.waitForTimeout(500);
    const huvud = await p.evaluate(() => { const r = document.querySelector('header .right')?.getBoundingClientRect(); const n = document.querySelector('header .nav')?.getBoundingClientRect(); return { right: r && Math.round(r.right), navRight: n && Math.round(n.right), rightLeft: r && Math.round(r.left), hojd: Math.round(document.querySelector('header').getBoundingClientRect().height) }; });
    console.log(w, s, JSON.stringify(huvud));
    await p.screenshot({ path: `skarmbilder/2026-10-27/${w}_${s}.png`, fullPage: true });
  }
  await ctx.close();
}
await b.close();
