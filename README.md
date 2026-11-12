# Nimaro's 17th Birthday Site

A single-page letter and tribute for Nimaro's 17th birthday (12 Nov 2026, born
05:53), built by David for his son. Live at:

**https://nimaro.africangraphyte.dev**

Hosted on Cloudflare Pages, connected to this repo — every push to `main`
deploys automatically within a few seconds.

## What this is

The page was built as a Claude Design canvas export (a `.dc.html`-style page)
and is served as-is: a single scrolling letter with five sections —
**Arrival, Name, Love, Growing, Blessing** — in a cream-and-gold palette,
closing with the letter from Mama and Daddy.

A small dynamic "chapters" block (Lego & puzzles, Swimming, A little sister,
Behind the wheel, School) renders client-side via `support.js`, which also
loads React from a CDN at runtime — this is normal for a Design-canvas export
and does not need a build step.

## Structure

```
index.html       The whole page — content, layout, styles, all inline.
support.js        Design-canvas runtime that boots the page and the
                  dynamic "chapters" component. Generated; don't hand-edit.
photos/           Photos used throughout the page (p01.jpg, p02.jpg, ...).
uploads/          The "now" photos — NOW-01 through NOW-05 — used for the
                  hero image and the closing photo with his mother.
favicon.ico/.png/.svg   Favicon in the page's gold/cream/purple palette.
og-cover.jpg      Social preview image (WhatsApp/Twitter/Instagram link
                  previews), same palette.
```

Every image `index.html` and `support.js` reference is present in `photos/`
or `uploads/` — there are no missing-photo placeholders in this version.

## Updating the letter

David is updating the letter content over time, including separate letters
to other family members and to himself. The letter text lives directly in
`index.html` inside the `<footer>` section near the end of the file — edit
the paragraph text in place; nothing else needs to change for a text-only
edit.

## Adding photos or video

To add a new photo: drop the file into `photos/` or `uploads/`, then
reference it by path (e.g. `photos/p21.jpg`) wherever it's needed in
`index.html` or in the `chapters`/`strip` arrays inside the
`<script type="text/x-dc" data-dc-script>` block at the bottom of the file.

Video (e.g. footage of Nimaro driving a Land Rover Defender at 10 years old)
isn't wired up yet — the page currently only renders images. When video
files are ready, we'll add a simple `<video>` block to the relevant section
rather than extending the dynamic chapters component.

## History

This replaces an earlier 40-page flip-book/scrolling "magazine" format
(ported from a different Design-canvas export) that is still available in
git history if ever needed again. It was retired in favor of this simpler,
complete design, which uses only photos already on hand.

---

Built with Claude Code.
