# SAEFUR hemsida

Den publika webbplatsen för SAEFUR: Start, Funktioner, Media, Priser, Om SAEFUR och Early Bird.

## Mappar

- `publik-2026-10-26/` är den publicerbara webbplatsen: statiska filer (HTML, CSS, JavaScript, JSON och bilder) som läggs ut som de är. Den byggs ur lanseringsversionen och ska inte redigeras för hand.
- `lansering-2026-10-26/` är den aktuella webbversionen med byggkällorna i `bygg/`. Redigera här och bygg om.

## Bygga

Kör i `lansering-2026-10-26/`:

```
python3 -I bygg/bygg_alla.py   # bygger sidorna i lansering-2026-10-26/
python3 -I bygg/publik.py      # skriver den publicerbara utgåvan till ../publik-2026-10-26/
```

`publik.py` tar bort granskningsraden och de interna sidorna och stoppar om en intern länk eller lokal adress finns kvar.

## Visa och pröva lokalt

```
node server.mjs                # http://127.0.0.1:5520/
node granska.mjs               # alla sidor, länkar och formulärets felfall mot en stubbe
node prov-funktioner.mjs       # sök och perspektiv på Funktioner
node prov-fast-meny.mjs        # fast huvudmeny, mobilmeny och sidfot
```

Proverna lånar Playwright ur en lokal installation; se importraden överst i respektive fil.

## Publicering

Webbplatsen serveras på samma adress som produkten. Formuläret på Early Bird-sidan skickar till `/api/early-bird` på samma adress.
