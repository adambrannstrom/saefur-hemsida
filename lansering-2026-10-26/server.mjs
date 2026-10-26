// Liten lokal server för designversionen. Inga beroenden. Stöder Range (krävs för video i Safari).
// Start: node server.mjs   (öppna sedan http://127.0.0.1:5520/)
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const rot = path.dirname(fileURLToPath(import.meta.url));
const port = Number(process.env.PORT || 5520);
const mime = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8", ".json": "application/json", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
  ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml", ".mp4": "video/mp4", ".webm": "video/webm",
  ".woff2": "font/woff2", ".woff": "font/woff", ".md": "text/markdown; charset=utf-8", ".txt": "text/plain; charset=utf-8",
};

http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (p.endsWith("/")) p += "index.html";
  const fil = path.normalize(path.join(rot, p));
  if (!fil.startsWith(rot)) { res.writeHead(403); return res.end(); }
  fs.stat(fil, (err, st) => {
    if (err || !st.isFile()) { res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" }); return res.end("Hittades inte: " + p); }
    const typ = mime[path.extname(fil).toLowerCase()] || "application/octet-stream";
    const huvud = { "Content-Type": typ, "Accept-Ranges": "bytes", "Cache-Control": "no-cache" };
    const range = req.headers.range;
    if (range) {
      const m = /bytes=(\d*)-(\d*)/.exec(range);
      let start = m && m[1] ? Number(m[1]) : 0;
      let slut = m && m[2] ? Number(m[2]) : st.size - 1;
      if (start >= st.size) { res.writeHead(416, { "Content-Range": `bytes */${st.size}` }); return res.end(); }
      slut = Math.min(slut, st.size - 1);
      res.writeHead(206, { ...huvud, "Content-Range": `bytes ${start}-${slut}/${st.size}`, "Content-Length": slut - start + 1 });
      return fs.createReadStream(fil, { start, end: slut }).pipe(res);
    }
    res.writeHead(200, { ...huvud, "Content-Length": st.size });
    fs.createReadStream(fil).pipe(res);
  });
}).listen(port, "127.0.0.1", () => {
  console.log(`SAEFUR lanseringsversion, granskning: http://localhost:${port}/  (avsluta med Ctrl+C)`);
});
