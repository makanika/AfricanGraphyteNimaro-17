#!/usr/bin/env python3
"""
One-off port script: takes David's original Claude-Design-canvas flip-book
(.dc.html, uses <x-dc>, support.js, {{ }} template bindings, sc-for/sc-if)
and rewrites it into a standalone vanilla HTML/CSS/JS file that runs in any
browser with no runtime dependency, suitable for Cloudflare Pages.

All page CONTENT (every leaf's markup, every inline style, every image path,
every word of copy) is left byte-for-byte untouched. Only the outer shell
(head, the two templated attributes on the stage/book divs, and the bottom
nav chrome + state-machine script) is replaced.
"""
import sys

SRC = "/mnt/user-data/uploads/9265f0e5-Nimaro_at_17_Web.dc.html"
OUT = "/home/claude/africangraphytenimaro-17/index.html"

with open(SRC, "r", encoding="utf-8") as f:
    text = f.read()

# ---------- anchors (verified unique) ----------
anchor1 = '<div id="stage" onClick="{{ stageClick }}" onDoubleClick="{{ stageDbl }}" style="position:fixed;inset:0;background:radial-gradient(1200px 800px at 50% 40%,#2a1550 0%,#14123a 45%,#0d0d20 100%);overflow:hidden;font-family:\'Nunito\',sans-serif;color:#fff;cursor:pointer;user-select:none;">'
anchor2 = '<div style="position:absolute;left:0;top:0;width:2160px;height:1350px;perspective:5200px;transform-origin:0 0;transform:{{ bookTransform }};transition:transform 1.1s cubic-bezier(.6,.05,.25,1);">'
anchor3 = '<div style="position:absolute;left:0;right:0;top:0;padding:22px 32px;display:flex;justify-content:space-between;align-items:center;pointer-events:none;">'

for name, a in [("anchor1", anchor1), ("anchor2", anchor2), ("anchor3", anchor3)]:
    c = text.count(a)
    if c != 1:
        sys.exit(f"ABORT: {name} occurs {c} times, expected 1")

# ---------- split off the tail (everything from the top toolbar onward) ----------
idx3 = text.index(anchor3)
head_and_body = text[:idx3]

# ---------- new <head> ----------
NEW_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Nimaro at 17 &mdash; The Seventeen Issue</title>
<meta name="description" content="A 40-page interactive flip-through magazine celebrating Nimaro's 17th birthday &mdash; from Age 0 to Age 17, plus 17 Wishes for 17.">

<!-- Open Graph / WhatsApp / Facebook -->
<meta property="og:type" content="website">
<meta property="og:title" content="Nimaro at 17 &mdash; The Seventeen Issue">
<meta property="og:description" content="A 40-page interactive flip-through magazine celebrating Nimaro's 17th birthday &mdash; from Age 0 to Age 17, plus 17 Wishes for 17.">
<meta property="og:image" content="og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Nimaro at 17 &mdash; The Seventeen Issue">
<meta name="twitter:description" content="A 40-page interactive flip-through magazine celebrating Nimaro's 17th birthday.">
<meta name="twitter:image" content="og-cover.jpg">

<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="favicon.png">
<link rel="apple-touch-icon" href="favicon.png">

<link rel="stylesheet" href="css/colors.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&family=Nunito:wght@400;600;700;800;900&display=swap">
<style>
  html,body{margin:0;height:100%;background:#0d0d20;overflow:hidden;}
  a{color:#efa3e5;} a:hover{color:#fff;}
  ::-webkit-scrollbar{display:none;}
  img{-webkit-user-drag:none;user-drag:none;}
  #chipsRow::-webkit-scrollbar{height:0;}
</style>
</head>
<body>
"""

NEW_STAGE_OPEN = '<div id="stage" onclick="NB.stageClick(event)" ondblclick="NB.stageDbl(event)" style="position:fixed;inset:0;background:radial-gradient(1200px 800px at 50% 40%,#2a1550 0%,#14123a 45%,#0d0d20 100%);overflow:hidden;font-family:\'Nunito\',sans-serif;color:#fff;cursor:pointer;user-select:none;opacity:0;transition:opacity .35s ease;">'
NEW_BOOKSTAGE_OPEN = '<div id="bookStage" style="position:absolute;left:0;top:0;width:2160px;height:1350px;perspective:5200px;transform-origin:0 0;transition:transform 1.1s cubic-bezier(.6,.05,.25,1);">'

# strip the old head block (everything up to and including the stage-opening anchor),
# then rebuild: NEW_HEAD + stage-open + rest-of-body-up-to-anchor2 + bookstage-open
idx_anchor1_end = head_and_body.index(anchor1) + len(anchor1)
between_1_and_2 = head_and_body[idx_anchor1_end:head_and_body.index(anchor2)]
after_anchor2 = head_and_body[head_and_body.index(anchor2) + len(anchor2):]

new_head_and_body = NEW_HEAD + NEW_STAGE_OPEN + between_1_and_2 + NEW_BOOKSTAGE_OPEN + after_anchor2

# ---------- new tail (nav chrome + vanilla JS state machine) ----------
NEW_TAIL = """<div style="position:absolute;left:0;right:0;top:0;padding:22px 32px;display:flex;justify-content:space-between;align-items:center;pointer-events:none;">
    <div style="display:flex;align-items:baseline;gap:14px;"><div style="font-family:'Anton',sans-serif;font-size:26px;letter-spacing:0.04em;">NIMARO</div><div style="font-weight:800;font-size:12px;letter-spacing:0.26em;color:#efa3e5;">THE SEVENTEEN ISSUE</div></div>
    <div id="hint" style="font-weight:700;font-size:12px;letter-spacing:0.14em;color:rgba(240,230,248,0.7);">&larr; &rarr; TO TURN &nbsp;&middot;&nbsp; DOUBLE-CLICK A PHOTO TO ZOOM &nbsp;&middot;&nbsp; F FOR FULL SCREEN</div>
  </div>
  <div onclick="event.stopPropagation()" style="position:absolute;left:0;right:0;bottom:0;height:84px;display:flex;align-items:center;gap:14px;padding:0 24px;background:linear-gradient(180deg,rgba(13,13,32,0),rgba(13,13,32,0.92) 40%);cursor:default;">
    <div id="prevBtn" onclick="event.stopPropagation();NB.prev();" style="flex:none;width:48px;height:48px;border-radius:9999px;border:2px solid rgba(255,255,255,0.5);display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;">&lsaquo;</div>
    <div id="chipsRow" style="flex:1;min-width:0;display:flex;gap:8px;overflow-x:auto;align-items:center;padding:4px 0;"></div>
    <div id="counter" style="flex:none;min-width:120px;text-align:right;font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:700;font-size:24px;color:#efa3e5;"></div>
    <div id="nextBtn" onclick="event.stopPropagation();NB.next();" style="flex:none;width:48px;height:48px;border-radius:9999px;border:2px solid rgba(255,255,255,0.5);display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;">&rsaquo;</div>
  </div>
  <div id="lightbox" onclick="NB.closeLb(event)" style="position:absolute;inset:0;background:rgba(13,13,32,0.94);display:none;align-items:center;justify-content:center;padding:40px;cursor:zoom-out;z-index:999;">
    <img id="lightboxImg" src="" alt="" style="max-width:100%;max-height:100%;object-fit:contain;box-shadow:0 30px 90px rgba(0,0,0,0.6);">
  </div>
</div>
<script>
(function () {
  "use strict";
  var state = { f: 0, side: 0, vw: window.innerWidth, vh: window.innerHeight, lb: "" };
  var tap = 0, tx = null, ct = null;

  function portrait() { return state.vw / state.vh < 1.15; }

  function curPage() {
    if (!portrait()) return state.f === 0 ? 1 : state.f === 20 ? 40 : 2 * state.f;
    return state.side === 0 ? 2 * state.f + 1 : 2 * state.f;
  }

  function save() { try { localStorage.setItem("nimaro17-page", String(curPage())); } catch (e) {} }

  var LABELS = [["COVER", 1], ["LETTER", 3]];
  for (var a = 0; a <= 16; a++) LABELS.push(["AGE " + a, 4 + 2 * a]);
  LABELS.push(["17 WISHES", 38], ["THE END", 40]);

  function render() {
    var W = 1080, H = 1350;
    var por = portrait();
    var s = por ? Math.min((state.vw - 24) / W, (state.vh - 150) / H)
                : Math.min((state.vw - 120) / (2 * W), (state.vh - 150) / H);
    var cx = W;
    if (por) cx = state.side === 0 ? 1.5 * W : 0.5 * W;
    else if (state.f === 0) cx = 1.5 * W;
    else if (state.f === 20) cx = 0.5 * W;
    var left = state.vw / 2 - s * cx, top = (state.vh - 84) / 2 - s * H / 2 + 14;

    var bookStage = document.getElementById("bookStage");
    if (bookStage) bookStage.style.transform = "translate(" + left + "px," + top + "px) scale(" + s + ")";

    var page = curPage();
    var act = LABELS.reduce(function (m, l, i) { return l[1] <= (por ? page : Math.max(1, page)) ? i : m; }, 0);

    var chipsRow = document.getElementById("chipsRow");
    chipsRow.innerHTML = "";
    LABELS.forEach(function (l, i) {
      var chip = document.createElement("div");
      chip.textContent = l[0];
      chip.style.cssText = "flex:none;padding:9px 14px;font-weight:800;font-size:13px;letter-spacing:0.14em;" +
        "border:2px solid " + (i === act ? "#870C71" : "rgba(255,255,255,0.28)") + ";" +
        "background:" + (i === act ? "#870C71" : "rgba(255,255,255,0.06)") + ";color:#fff;cursor:pointer;white-space:nowrap;";
      chip.onclick = function (e) { e.stopPropagation(); goPage(l[1]); };
      chipsRow.appendChild(chip);
    });

    document.getElementById("counter").textContent = por
      ? ("p. " + page + " / 40")
      : (state.f === 0 ? "Cover" : state.f === 20 ? "p. 40" : "pp. " + (2 * state.f) + "\\u2013" + (2 * state.f + 1));

    document.getElementById("prevBtn").style.opacity = (por ? (state.f === 0 && state.side === 0) : state.f === 0) ? 0.25 : 1;
    document.getElementById("nextBtn").style.opacity = (por ? (state.f === 20) : state.f === 20) ? 0.25 : 1;

    document.getElementById("stage").style.opacity = "1";
  }

  function apply() {
    var f = state.f;
    document.querySelectorAll("[data-leaf]").forEach(function (el) {
      var i = +el.getAttribute("data-leaf"), fl = i <= f;
      el.style.transform = fl ? "rotateY(-180deg)" : "rotateY(0deg)";
      el.style.zIndex = fl ? i : 40 - i;
    });
    render();
  }

  function goPage(n) {
    n = Math.max(1, Math.min(40, n));
    var odd = n % 2 === 1;
    state.f = odd ? (n - 1) / 2 : n / 2;
    state.side = odd ? 0 : 1;
    save();
    apply();
  }

  function next() {
    if (portrait()) {
      if (state.side === 0 && state.f < 20) { state.f += 1; state.side = 1; save(); apply(); }
      else if (state.side === 1 && state.f < 20) { state.side = 0; save(); apply(); }
    } else if (state.f < 20) { state.f += 1; state.side = 0; save(); apply(); }
  }

  function prev() {
    if (portrait()) {
      if (state.side === 0 && state.f > 0) { state.side = 1; save(); apply(); }
      else if (state.side === 1) { state.f -= 1; state.side = 0; save(); apply(); }
    } else if (state.f > 0) { state.f -= 1; state.side = 0; save(); apply(); }
  }

  function measure() { state.vw = window.innerWidth; state.vh = window.innerHeight; apply(); }

  window.NB = {
    prev: prev,
    next: next,
    goPage: goPage,
    stageClick: function (e) {
      if (state.lb) return;
      if (tap) { tap = 0; return; }
      var x = e.clientX;
      clearTimeout(ct);
      ct = setTimeout(function () { x < state.vw / 2 ? prev() : next(); }, 240);
    },
    stageDbl: function (e) {
      clearTimeout(ct);
      var t = e.target;
      if (t && t.tagName === "IMG" && t.src) {
        state.lb = t.src;
        document.getElementById("lightboxImg").src = t.src;
        document.getElementById("lightbox").style.display = "flex";
      }
    },
    closeLb: function (e) {
      e.stopPropagation();
      state.lb = "";
      document.getElementById("lightbox").style.display = "none";
    }
  };

  window.addEventListener("resize", measure);
  window.addEventListener("keydown", function (e) {
    var k = e.key;
    if (k === "ArrowRight" || k === "ArrowDown" || k === " " || k === "PageDown") { e.preventDefault(); next(); }
    else if (k === "ArrowLeft" || k === "ArrowUp" || k === "PageUp") { e.preventDefault(); prev(); }
    else if (k === "Home") goPage(1);
    else if (k === "End") goPage(40);
    else if (k === "Escape") { state.lb = ""; document.getElementById("lightbox").style.display = "none"; }
    else if (k === "f" || k === "F") {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
    }
  });
  window.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
  window.addEventListener("touchend", function (e) {
    if (tx == null) return;
    var dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) { tap = 1; dx < 0 ? next() : prev(); }
    tx = null;
  }, { passive: true });

  document.addEventListener("DOMContentLoaded", function () {
    try {
      var p = parseInt(localStorage.getItem("nimaro17-page") || "1", 10);
      measure();
      goPage(p);
    } catch (e) { measure(); apply(); }

    // A handful of source photos referenced by the original design were never
    // supplied to this session (see README "Missing photos"). Rather than show
    // a broken-image icon on those spreads, swap in a quiet placeholder tile
    // that matches the book's own palette.
    document.querySelectorAll("img").forEach(function (img) {
      img.addEventListener("error", function () {
        if (img.dataset.fallenBack) return;
        img.dataset.fallenBack = "1";
        img.src = "missing.svg";
        img.style.objectFit = "contain";
        img.style.background = "#1B1949";
        img.style.padding = "12%";
      });
    });
  });
})();
</script>
</body>
</html>
"""

final = new_head_and_body + NEW_TAIL

with open(OUT, "w", encoding="utf-8") as f:
    f.write(final)

print("wrote", OUT, "length", len(final))
print("contains {{ :", "{{" in final)
print("contains <x-dc>:", "<x-dc>" in final)
print("contains sc-for:", "sc-for" in final)
print("contains support.js:", "support.js" in final)
print("contains DCLogic:", "DCLogic" in final)
print("data-leaf count:", final.count("data-leaf="))
