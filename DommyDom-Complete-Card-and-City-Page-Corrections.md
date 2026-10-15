# DOMMYDOM — COMPLETE CARD AND CITY-PAGE DESIGN CORRECTIONS

**Project:** `sun-and-sage` (DommyDom / Dominique Duncan-Nelson)  
**For:** OpenAI Codex in the existing VS Code project  
**Status:** Local changes only. **Do not commit, push, deploy, or publish.**  

## First: Read and understand the current code

Inspect the current `blog.html`, relevant Life Changes category pages (including `life-changes/growing-family.html`, `life-changes/empty-nest.html`, and `life-changes/marriage.html` if they are present), their shared card CSS, and all relevant city information page templates (starting with `buy-winnetka.html`). Confirm actual file paths rather than assuming them.

Also locate and read these existing instruction files **if present**:

- `DommyDom-Luxury-Card-Framing-and-Spacing-v2.md`
- `DommyDom-Fix-Article-Card-Spacing.md`
- `DommyDom-City-Pages-Editorial-Layout-Codex.md`

Use this document as the **current final combined specification** where older instructions conflict. Check the existing design and site brand colors before editing. Focus on the root CSS/layout rules and avoid piling on competing overrides. Do not make unrelated changes.

---

## TASK 1 — MAKE ALL ARTICLE CARDS LOOK SUBSTANTIALLY, ELEGANTLY FRAMED

### What is wrong

In the supplied VS Code screenshots, the outer borders of many DommyDom article cards are now dark sage green, but the internal horizontal separator rules are pale or inconsistent, some stop short at the text padding, and the combined card design looks mismatched. The user wants the entire card's framing system to feel **stronger, substantial, refined, and deliberately designed**, **not simply the old thin lines painted green**.

### Exact visual requirement

1. Use the **existing dark sage-green brand color**, taken from the site's actual approved palette. Reuse its CSS variable/value rather than inventing an unrelated green.
2. Give each card a **visible, refined outer frame** around the full image, title/excerpt area, and Read More footer. Target a **visually substantial ~3px outer frame**, adjusting slightly if needed for elegance. It must be noticeably stronger than a hairline but **must not be chunky, cartoonish, or harsh**.
3. Every internal **structural** line or separator in this same card component must use that **same dark sage-green family**, not a mixture of sage, light gray, beige, or other line colors.
4. Differentiate hierarchy by weight where useful: outer frame is the strongest, interior structural dividers are refined but still clearly present (e.g. 1.5–2px where practical). These must read as one coordinated design system rather than random lines.
5. **Full-width horizontal dividers:** The line under the image (where present), the title/body separator (where present), and the separator immediately above **READ MORE** must extend across **the complete inner width of the card—from the inside left frame to the inside right frame**. Do **not** make these dividers stop at the text inset/padding or appear as short decorative underlines.
6. Accomplish full-bleed separators with appropriate structural wrappers or CSS (such as positioning/negative margins) while **keeping text comfortably padded**. Do not eliminate text padding merely to stretch a rule.
7. All parallel dividers must align identically from card to card, including first and last cards in a row. No missing, truncated, uneven, disconnected, or double-thick lines.
8. Retain a separate, tasteful **Read More link underline** only if already part of the editorial design. It is a link detail, **not** the structural full-width footer separator; do not confuse the two.
9. Ensure the green frame surrounds the full card from top image edge through footer, with no unframed gaps, broken corners, inconsistent edge thickness, or clipped borders.
10. Preserve an upscale white/ivory card surface and the brand's existing typography, photographs, aspect ratios, titles, and link style. Avoid thick shadows, flashy gradients, rounded bubble cards, or colored fills. A very subtle inset detail may be used only if it improves the final luxury appearance without clutter.
11. Apply the consistent frame treatment to the relevant article and blog card systems across the site, **not just one row or one page**. Reuse shared component styling whenever possible and check that a new override does not conflict with older styles.

**Visual acceptance:** A visitor should immediately see **a substantial dark sage frame** and deliberate, full-width dark sage separators throughout **each card**, instead of faint little outlines and short interior rules.

---

## TASK 2 — REMOVE EMPTY SPACE WITHOUT CREATING UNEVEN CARD LENGTHS

### What is wrong

Earlier Codex changes reduced some blank areas, but examples still show too much vertical whitespace between short previews and their Read More footers. Other cards have long previews, and older fixed heights / minimum heights / row stretching rules appear to cause unexpectedly tall cards.

### Required behavior

1. Trace and resolve the **winning** CSS rules for card body heights, `min-height`, fixed heights, flex/grid stretching, `grid-auto-rows`, padding, and alignment. Find and fix the underlying cause, rather than layering contradictory style rules.
2. Each desktop **row of cards must look evenly sized**, with photo tops, title areas, and Read More footer positions aligned across that row. Cards must remain uniform in height **within their row**; do not create a sloppy masonry layout of uneven bottoms.
3. The row height should follow the **real content needs of that row**, not a giant shared fixed height inherited from a different row or page. Avoid artificially tall cards whose lower half is blank.
4. Keep the **Read More** footer anchored consistently at the bottom of each card, while reducing excess blank space directly above it. Maintain elegant, moderate breathing room instead of pushing a footer hundreds of pixels below a short excerpt.
5. Preserve card photographs at the current approved sizes / crop treatments. Keep all titles legible, centered as presently designed, and visually balanced.
6. Preserve the approved card excerpts and complete article text. **Do not fabricate filler copy, repeat the introduction, change the article facts, truncate excerpts into ugly mid-sentence ellipses, or add invented information** merely to fill blank space.
7. Do not force all rows on the entire page to share the same height; balance each row individually. On mobile, where there is one card per row, allow the individual cards to use compact natural heights.
8. Review the visual result on representative short/medium/long excerpt rows. If some particular excerpt is so much longer that a perfectly compact equal-height row is impossible without editing copy, **name those cards in the final report** rather than silently padding the others with filler.
9. Keep consistent vertical rhythm between rows, aligned card edges, consistent image heights, and an intentional gap between the last card row and the next page section.
10. Do not modify source article content, publication dates, links, navigation, images, SEO, chat, footer, or unrelated sections to achieve this.

**Visual acceptance:** The cards look like a tightly composed luxury editorial grid, not tall empty white towers, **and** the Read More rows still align within every desktop row.

---

## TASK 3 — COMPLETE THE DOMMYDOM CITY INFORMATION REDESIGN

### Previous request was not completed

The user previously requested a **luxury editorial redesign of the actual city information sections**, not the site's top navigation. The original Winnetka screenshot (`buy-winnetka.html`) showed plain columns with tiny left-aligned category labels, centered headings, and left-aligned body paragraphs that did not visually connect. The same issue needs a consistent solution across **all relevant city pages**, not just Winnetka.

### Required design

1. Identify the shared city-page templates / selectors and all applicable city pages. Start with `buy-winnetka.html`; inspect other comparable city pages and cover all relevant templates.
2. Redesign the **city information blocks only** (e.g. shopping and dining, parks and recreation, healthcare, HOA costs, property taxes, and insurance/hazards, when they are present) into an elegant **luxury editorial two-column layout on desktop**.
3. Use the website's authentic **warm ivory / cream, muted sage, and dark sage-green palette**, existing fonts, and restrained editorial style. Do not invent an unrelated theme, gaudy graphics, oversized cards, or generic dashboard components.
4. Give each information panel a considered structure: **small readable category label, prominent but restrained heading, and explanatory paragraph all sharing a deliberate, consistent alignment**. Do not scatter left labels, centered headings, and paragraphs with unrelated alignment.
5. Use sophisticated spacing, balanced gutters, subtle ivory surface separation, and consistent rules / accent detailing. Make information easy to scan. Keep panel heights balanced where appropriate without forcing large empty blocks.
6. On mobile, switch to a beautiful **single-column** editorial layout with readable type, natural block heights, no horizontal overflow, no clipping, and comfortable spacing.
7. Preserve **every factual statement** on the city pages unless a verified correction is separately authorized. Do not rewrite or shorten the copy, invent market data, introduce new financial estimates, or remove existing links. Preserve each page's SEO metadata, canonical URL, header, footer, branding, and chat behavior.
8. Apply the redesign consistently to comparable city pages through shared style rules or templates where possible; avoid changing unrelated property or blog pages.
9. **Show the redesigned Winnetka section** as the initial visual benchmark, plus at least one other city page, before final approval or publication. Verify that the styling actually appears in the browser and is not merely written in CSS.

**Visual acceptance:** The city information blocks should look like thoughtfully designed luxury real estate editorial panels rather than raw text pasted into a two-column grid.

---

## NON-NEGOTIABLE PROTECTION RULES

- Work in the existing **`sun-and-sage` DommyDom** project only. **Do not edit StartWeb7 or Paradigm Janitorial.**
- Keep the existing top navigation, logos, business contact details, door-opening homepage video, other animations, approved photographs, and chat behavior unchanged.
- Preserve page copy, headings, URLs, dates, sources, links, SEO, structured data, and other existing site functionality.
- Make targeted changes, ideally in shared card and city-page styles, rather than repeating long overrides in hundreds of pages.
- Don't remove or overwrite unrelated updates in the worktree. Review the current changed-file list before and after editing.
- Never claim a design passes because a CSS rule was edited. **Visually inspect rendered browser previews.**
- Do not commit, push, deploy, or publish anything. Leave changes for the user to review.

## MANDATORY VISUAL QA

Test in a browser preview or local server where possible, at **1920, 1440, 1280, 1024, 768, 390, and 320px widths**, with particular attention to narrow browser preview conditions like those in the screenshots.

Check **all three areas**:

### Card frames
- Outer dark sage border is substantial and continuous on all four sides.
- Every structural divider uses the same sage color and consistent thickness.
- Horizontal rules span the **complete card width inside the outer frame**, not merely the inset text width.
- No double borders, misaligned rules, missing endcaps, clipping, or inconsistent corners.

### Card whitespace and alignment
- Each desktop row has aligned image tops, card bottoms, and Read More footers.
- No large, avoidable blank regions above Read More.
- No cut-off text, duplicated preview text, broken links, or changes to original excerpts.
- Mobile cards remain readable and naturally sized.

### City pages
- New editorial panels are actually visible on `buy-winnetka.html` and other relevant city pages.
- Headings/labels/body align consistently and feel intentionally designed.
- Responsive two-column desktop / single-column mobile layout works.
- No content, images, source links, or navigation broken.

Fix regressions introduced by your changes, then report:

1. Exact pages and files changed.
2. The reused dark sage brand color value and actual line thicknesses.
3. How full-width dividers were implemented.
4. Why excess empty space remained and how you corrected the winning CSS rules.
5. Which city pages received the editorial design.
6. Which viewport widths you **actually tested**, with preview screenshots or links when possible.
7. Any remaining limitations or unverified issues.

**STOP BEFORE PUBLISHING. The user must approve the visual result.**
