#!/usr/bin/env python3
"""
Converts the flip-book (index.html, as committed) into a plain vertical
scrolling page. Every one of the 40 pages' content -- every image, every
word, every inline style -- is lifted out completely unchanged; only the
outer mechanism changes: instead of a 3D page-flip with touch/keyboard/
click gesture handling, each page is just a stacked, scaled-to-fit block
in a normal scrolling document. No flip animation, no swipe detection,
no viewport-fit math beyond "scale this fixed 1080x1350 design to the
screen's width."

Source of truth is whatever index.html currently contains (so re-running
this after further edits to individual pages -- like the letter -- just
re-pulls the latest content).
"""
import re
from bs4 import BeautifulSoup

SRC = "/home/claude/africangraphytenimaro-17/index.html"
OUT = "/home/claude/africangraphytenimaro-17/index.html"

with open(SRC, encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

pages = soup.find_all(attrs={"data-label": True})
assert len(pages) == 40, f"expected 40 pages, found {len(pages)}"

# Jump-nav entries: (visible label, target page's data-label to anchor to)
NAV = [
    ("Cover", "Cover"), ("Letter", "Letter"),
] + [(f"Age {a}", f"Age {a}") for a in range(0, 17)] + [
    ("17 Wishes", "Wishes 1"), ("The End", "Back Cover"),
]

def slugify(label):
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")

page_sections = []
for p in pages:
    label = p.get("data-label")
    anchor_id = "page-" + slugify(label)
    # Drop the data-label/data-screen-label attributes' role as flip-book
    # hooks (harmless to keep, but the id is what navigation now uses).
    p["id"] = anchor_id
    page_html = str(p)
    page_sections.append(
        f'<div class="spread"><div class="page-canvas">{page_html}</div></div>'
    )

nav_links = "".join(
    f'<a href="#page-{slugify(target)}">{label}</a>'
    for label, target in NAV
)

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Nimaro at 17 &mdash; The Seventeen Issue</title>
<meta name="description" content="A birthday magazine celebrating Nimaro's 17th birthday &mdash; from Age 0 to Age 17, plus 17 Wishes for 17.">

<meta property="og:type" content="website">
<meta property="og:title" content="Nimaro at 17 &mdash; The Seventeen Issue">
<meta property="og:description" content="A birthday magazine celebrating Nimaro's 17th birthday &mdash; from Age 0 to Age 17, plus 17 Wishes for 17.">
<meta property="og:image" content="og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Nimaro at 17 &mdash; The Seventeen Issue">
<meta name="twitter:description" content="A birthday magazine celebrating Nimaro's 17th birthday.">
<meta name="twitter:image" content="og-cover.jpg">

<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="favicon.png">
<link rel="apple-touch-icon" href="favicon.png">

<script>
  // Registered before any <img> tag is parsed, in the capture phase, on
  // `document` -- not inside DOMContentLoaded -- because 'error' does not
  // bubble and some photos load eagerly, so a late listener can miss the
  // event entirely. A handful of source photos referenced by the design
  // were never supplied (see README "Missing photos"); this swaps in a
  // quiet placeholder tile instead of a broken-image icon.
  document.addEventListener("error", function (e) {
    var img = e.target;
    if (!img || img.tagName !== "IMG") return;
    if (img.dataset.fallenBack) return;
    img.dataset.fallenBack = "1";
    img.src = "/missing.svg";
    img.style.objectFit = "contain";
    img.style.background = "#1B1949";
    img.style.padding = "12%";
  }, true);
</script>

<link rel="stylesheet" href="css/colors.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&family=Nunito:wght@400;600;700;800;900&display=swap">
<style>
  html { scroll-behavior: smooth; }
  body { margin:0; background:#0d0d20; font-family:'Nunito',sans-serif; }
  img { -webkit-user-drag:none; user-drag:none; }

  .topbar {
    position: sticky; top: 0; z-index: 50;
    background: rgba(13,13,32,0.92); backdrop-filter: blur(6px);
    display: flex; align-items: center; gap: 18px;
    padding: 14px 20px; color: #fff;
  }
  .topbar .brand { display:flex; align-items:baseline; gap:10px; flex: none; }
  .topbar .brand b { font-family:'Anton',sans-serif; font-size:20px; letter-spacing:0.03em; }
  .topbar .brand span { font-weight:800; font-size:11px; letter-spacing:0.22em; color:#efa3e5; white-space:nowrap; }
  .topbar nav { flex:1; min-width:0; display:flex; gap:6px; overflow-x:auto; padding:2px 0; }
  .topbar nav::-webkit-scrollbar { height:0; }
  .topbar nav a {
    flex:none; color:rgba(255,255,255,0.75); text-decoration:none;
    font-weight:800; font-size:12px; letter-spacing:0.1em;
    padding:7px 11px; border:1.5px solid rgba(255,255,255,0.2); white-space:nowrap;
  }
  .topbar nav a:hover { color:#fff; border-color:#870C71; background:#870C71; }

  .spread {
    width: 100%;
    display: flex;
    justify-content: center;
    overflow: hidden;
  }
  .page-canvas {
    width: 1080px;
    height: 1350px;
    flex: none;
    transform-origin: top center;
    box-shadow: 0 24px 64px rgba(0,0,0,0.45);
    margin-bottom: 26px;
  }
  .page-canvas > div { width:100%; height:100%; }
</style>
</head>
<body>
<div class="topbar">
  <div class="brand"><b>NIMARO</b><span>THE SEVENTEEN ISSUE</span></div>
  <nav>__NAV__</nav>
</div>
__PAGES__
<script>
(function () {
  function scalePages() {
    document.querySelectorAll(".spread").forEach(function (wrap) {
      var canvas = wrap.querySelector(".page-canvas");
      if (!canvas) return;
      var scale = Math.min(1, wrap.clientWidth / 1080);
      canvas.style.transform = "scale(" + scale + ")";
      wrap.style.height = (1350 * scale + 26) + "px";
    });
  }
  window.addEventListener("resize", scalePages);
  window.addEventListener("load", scalePages);
  document.addEventListener("DOMContentLoaded", scalePages);
  scalePages();
})();
</script>
</body>
</html>
"""

final = HEAD.replace("__NAV__", nav_links).replace("__PAGES__", "\n".join(page_sections))

with open(OUT, "w", encoding="utf-8") as f:
    f.write(final)

print("wrote", OUT, "length", len(final))
print("pages embedded:", len(page_sections))
