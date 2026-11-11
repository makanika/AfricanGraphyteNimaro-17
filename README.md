# Nimaro at 17 — The Seventeen Issue

A 40-page, interactive, 3D page-flip birthday magazine built for Nimaro's
17th birthday (12 November 2026). This repo is set up to deploy straight
to **Cloudflare Pages** with no build step.

**Live entry point:** `index.html` at the repo root (Cloudflare Pages
serves this automatically — no configuration needed).

---

## What's in this repo

| File / folder | What it is |
|---|---|
| `index.html` | **The flip-book.** Standalone HTML/CSS/JS — the main piece. |
| `web/`, `photos/` | The 60 photos the flip-book references. |
| `css/colors.css` | The book's colour & type tokens, documented in plain CSS (see "Design system" below). |
| `favicon.svg`, `favicon.png`, `favicon.ico` | An original "17" mark used as the site icon. |
| `og-cover.jpg` | The 1200×630 preview image WhatsApp/Twitter/Instagram show when the link is shared, cropped from the real magazine cover. |
| `missing.svg` | Quiet placeholder tile shown if a photo fails to load (see "Missing photos" below). |
| `dashboard.html` | A separate "Life in Pictures" year-by-year timeline built from the family photo archive (27 photos, two per year where available). |
| `magazine.html` | A clean page-by-page viewer for your own finished 17-page PDF magazine design (`Nimaro17.pdf`), rasterized to images. |
| `assets/` | Images used by `dashboard.html` and `magazine.html`. |
| `scripts/port_flipbook.py` | The script that generated `index.html` from your original Claude-Design-canvas export — kept here so the port is reproducible if you send an updated `.dc.html` later. |

`index.html`, `dashboard.html` and `magazine.html` are three independent
pages — none of them link to each other yet. If you want a way to jump
between them, that's an easy follow-up; just say so.

---

## Deploying on Cloudflare Pages

1. Push this repo to GitHub (already done if you're reading this from
   `makanika/africangraphytenimaro-17`).
2. In the Cloudflare dashboard: **Workers & Pages → Create → Pages →
   Connect to Git**, pick this repo.
3. Build settings: leave **Build command** empty and **Build output
   directory** as `/` (this is a static site — nothing to build).
4. Deploy. Cloudflare serves `index.html` at the domain root automatically.

No environment variables, no framework, no `package.json` — it's plain
HTML/CSS/JS, so there's nothing else to configure.

---

## What changed from your original file

Your original export (`Nimaro_at_17_Web.dc.html`) was built with Claude's
own Design-canvas component runtime — it depends on a `support.js` script
and a `<x-dc>` wrapper that only exist inside Claude's artifact viewer, so
it would not have run on Cloudflare Pages as-is.

`index.html` here is a straight **behavioral port**: every page's content —
every word, every image, every inline style, every colour and font size —
is untouched, byte-for-byte, from your original. The only things rewritten
were the invisible scaffolding:

- The `<x-dc>`/`support.js`/templated-attribute wrapper → plain HTML.
- The page-flip state machine (which leaf is turned, keyboard/touch/swipe
  navigation, the chapter chips, the lightbox zoom, fullscreen, and the
  "resume where you left off" bookmark) → rewritten as plain vanilla
  JavaScript at the bottom of `index.html`, with exactly the same behavior:
  - **← / → arrow keys, swipe, or click left/right half of the page** to turn
  - **Double-click any photo** to zoom
  - **F** for fullscreen
  - **Home / End** to jump to the cover / back cover
  - Click any chapter chip along the bottom to jump straight there
  - Your page is remembered (via `localStorage`) if you close and reopen it

Everything is responsive — the same scaling math from your original design
(which already adapted between landscape "two pages side by side" and
portrait "one page at a time") is preserved, so it resizes correctly on
phones, tablets, and desktop windows.

### Added for sharing & polish
- Open Graph + Twitter Card meta tags, so pasting the link into WhatsApp,
  Twitter/X, or Instagram shows a title, description, and preview image
  (cropped from the real cover of your own PDF magazine).
- An original favicon (a simple navy/pink "17" mark — nothing borrowed).
- `alt` text on every photo, and `loading="lazy"` on everything past the
  cover spread, so the book opens quickly even on a slow connection.
- A soft placeholder tile for any photo that fails to load, instead of a
  broken-image icon (see below).

---

## Missing photos (17 files)

Your original design references 60 images. 43 were in the archive you
uploaded earlier this session and are already in `web/`/`photos/`. **17 are
not in anything uploaded to this session** and could not be included —
nothing has been faked or substituted in their place. They currently show
the quiet "photo to come" placeholder tile. Here's exactly where each one
belongs, so you can drop the real files straight into `web/` with these
exact names:

| Missing file | Appears on |
|---|---|
| `web/now01.jpg` | Cover |
| `web/now03.jpg` | Age 16 |
| `web/now02.jpg`, `web/now04.jpg`, `web/now05.jpg` | Age 16 Photos |
| `web/p07.jpg` | Contents, Age 13 Photos |
| `web/p09.jpg` | Age 3 Photos |
| `web/p06.jpg` | Age 4 Photos |
| `web/p10.jpg` | Age 5 Photos |
| `web/p03.jpg` | Age 7 Photos, Age 14 Photos |
| `web/p12.jpg` | Age 10 Photos |
| `web/p08.jpg` | Age 11 Photos |
| `web/p01.jpg` | Age 14 Photos, Back Cover |
| `web/p04.jpg`, `web/p11.jpg` | Age 14 Photos |
| `web/p02.jpg` | Age 15 |
| `web/p05.jpg` | Age 15 Photos |

Once you have those 17 files, just add them to `web/` with the exact
filenames above (lowercase, `.jpg`) and they'll appear automatically — no
other changes needed.

---

## One date to double-check

The **Age 3** spread (page 10) is illustrated with `web/img_1007.jpg`,
labelled "NOV 2012 — NOV 2013." That photo's own camera metadata (EXIF)
says it was taken **30 July 2014**, which would actually fall in the
**Age 4** window (Nov 2013 – Nov 2014). I haven't changed the label or
swapped the photo — just flagging it in case you want either the photo
or the label adjusted.

---

## Design system

The palette and type choices (navy `#1B1949`, magenta `#870C71`, light
pink `#efa3e5`, off-white `#F6F4F8`, display font Anton, editorial-italic
font Cormorant Garamond, body font Nunito) are documented as plain CSS
custom properties in `css/colors.css`. Your original file loaded its
colours from an internal Sprint design-system stylesheet path; that's
been replaced with this local, unbranded file so nothing here carries
Sprint naming.

---

## Local preview

No build step — just open `index.html` in a browser, or serve the folder
locally:

```bash
python3 -m http.server 8080
# then visit http://localhost:8080
```
