# DOMMYDOM — MASTER IMPLEMENTATION DIRECTIONS
## Tablet/phone navigation + simplified menus + Considerations card page + provided photos + EXACT header group swap

**Project/repository:** `sun-and-sage` (DommyDom / Dominique Duncan-Nelson website)

**This is the CURRENT, COMBINED, AUTHORITATIVE brief for the directions agreed since the instruction that the hamburger menu belongs on phones, NOT iPads.** Implement as one coordinated, careful change. It supersedes contradictory instructions in older files, particularly directions to *remove Considerations from the main navigation* or *show MENU on tablets*. Read current source to obtain exact existing names, links, assets and structure, rather than treating old instruction documents as the source of truth for content.

**IMPLEMENT LOCALLY ONLY. No commit, push, deploy, or publish before approval. Preserve existing uncommitted work.**

---

## 0. FIRST: RECONCILE THE CURRENT ACTUAL WEBSITE AND RECORD WHAT EXISTS

The site already has hundreds of completed static pages and existing approved designs. The owner does **not** want a new website or another broad redesign.

Before editing:

1. Open the `sun-and-sage` project and inspect current shared navigation sources (HTML templates/JS/CSS, including any auto-generated/repeated headers); inspect the current `Considerations` category/dropdown definitions and their real destination pages. Inspect `git status` to protect unrelated edits; do not discard/overwrite other ongoing work.
2. Identify the **exact, already-written, natural-sounding category labels** previously displayed in the Considerations dropdown, their destination page URLs, the layout of those category/article pages, and the already-approved photograph cards used elsewhere on the site. **Do not guess the labels from filenames, from an old MD, or from this brief.**
3. If the latest header no longer includes `Considerations`, recover the last authentic Considerations link map from the existing repo, relevant page/source files or local Git history. **Retain each original heading/label and URL.** Do not invent replacement names like “Buyer Questions,” “Seller Questions,” or newly brainstormed categories.
4. Identify newly uploaded image files in the repository root. These are the **owner-provided, already downloaded card photos**. Match them to actual existing Considerations categories by subject, without inventing categories or requiring more photography. If a filename is ambiguous, inspect the image and provide a proposed mapping; do not silently place a mismatched photo.
5. Identify the real link destination, dropdown behavior and current styling for `Neighborhoods`, `Search`, `Buy`, `Sell`, `Property Management`, `Interior Design`, `Life Changes`, and the existing header contact details.

**Deliverable of this initial audit:** List each actual Considerations category title -> actual existing category-page destination -> matching uploaded photo. If any original link cannot be recovered, report that specific gap rather than creating an imaginary replacement.

---

## 1. EXACT PRIMARY NAVIGATION — CONSIDERATIONS IS BACK AS A DIRECT PAGE

Keep the main navigation clear and editorial. The final approved main menu, now with `Considerations` returned, is:

**Home | About | Buy | Sell | Property Management | Interior Design | Life Changes | Considerations | Blog | Contact**

- **`Considerations` is ONE direct navigation link. IT HAS NO DROPDOWN.** Hovering over Considerations on desktop should not produce a mega-menu; click opens the Considerations landing page described in section 5.
- **Keep both Buy and Sell as separate top-level items.** Dominique specifically requested separate Buy and Sell. Do NOT replace them with `Real Estate` or generic `Services`.
- Keep `Home`, `Property Management`, `Interior Design`, `Life Changes`, `Blog`, `Contact` as real visible top-level items. Do not remove or rename them to make room.
- `Neighborhoods` and `Search` are **special HEADER features**, NOT additional labels within the horizontal primary nav.
- Preserve the primary link destinations and the existing established typography and brand. No desktop arrow, chevron, caret, triangle, or plus-sign indicators.
- Do not introduce a second crowded desktop nav row. Do not use unreadably tiny text to fit everything.

---

## 2. RESPONSIVE NAVIGATION — HAMBURGER FOR PHONES ONLY, NOT iPADS

**NON-NEGOTIABLE NEW APPROVAL:** iPads and tablets must **not** display a hamburger MENU in place of the primary navigation merely because the browser becomes tablet width. The earlier instructions permitting a tablet hamburger are SUPERSEDED.

- **Desktop/laptop:** Show visible horizontal main navigation, one elegant line, readable labels and adequate gaps. No split/two-row desktop nav.
- **iPad/tablet portrait AND landscape:** Keep the primary navigation **visible**, including the new `Considerations` item. No hamburger at common iPad widths (test 744, 768, 820, 834, 1024 and 1180 CSS pixels).
- Use content-aware responsive widths, refined typography and spacing, not CSS zoom or shrinking the entire header. If all TEN labels cannot truly fit comfortably at a narrow tablet width, use a thoughtfully styled **single-line horizontally swipeable navigation strip** as the last resort, with clear affordance that more items are available. This is preferable to an iPad hamburger, tiny unreadable text, clipping, or a broken second row. Ensure the items are reachable by touch and keyboard. Report if this fallback is needed. Try a full visible single row first.
- **Phones only:** Use the existing `MENU` / hamburger control at genuinely phone-sized layouts (approximately <=599 CSS px is a reasonable starting implementation threshold; refine for real devices). Test 320, 375, 390 and 430 CSS px. No desktop-style nav squeezed onto a phone.
- **Desktop pointer:** Dropdowns that actually have children automatically open on **HOVER**, with NO preliminary click. Keep menus attached beneath their triggers, no dead gaps or flicker.
- **Tablet touch:** A tap opens the relevant dropdown because touch lacks reliable hover. Tapping an actual destination then visits that page. Ensure parent landing pages remain accessible.
- **Phone open menu:** A user taps MENU once to reveal a polished, cohesive, single-column list of the TEN main categories. Categories that have genuine children can be tapped to show them inline; do not show hundreds of articles all at once or force visitors through multiple nested accordions. `Considerations` should link **directly** to its landing page, without expanding a submenu. Keep CLOSE easy to reach; preserve proper scroll and focus, avoid clipped/overlapping content.
- Do **not** revert to the old disconnected two-column accordion layout or an endless, fully expanded directory inside MENU. Touch tapping is expected on phones; Dominique's “too many clicks” concern means avoiding *extra* nested layers.

**Acknowledge technical constraints transparently:** If the full ten-item nav simply cannot fit at 744px, do NOT claim it fits; implement the visible one-line swipeable tablet rail if necessary and provide an actual screenshot and note.

---

## 3. HEADER ORDER — SIMPLE SWAP ONLY, NOT ANOTHER HEADER REDESIGN

**The owner APPROVED the current header structure/positioning and requested exactly ONE change:**

**SWAP the placement of these existing TWO GROUPS:**
- Group A = `Neighborhoods` + `Search` together (same icons and text, same internal order).
- Group B = both existing phone numbers + existing email together.

**The result is Neighborhoods and Search appearing before the contact numbers/email,** in the places formerly occupied by the contact group. Move the contacts to the position formerly occupied by Neighborhoods/Search.

Do NOT independently rearrange every header item, change the header's number of rows, alter the spacing globally, move/rework RISE × real, resize the signature logo, change phone numbers, change the email, modify the header height, or produce a fresh design. **Just swap those two groups within the existing responsive header architecture.** Maintain their current spacing and look, and make the responsive order sensible when it adapts to narrow screens.

- Keep signature/logo, genuine contact information, and RISE × real branding exactly as approved.
- Keep existing `tel:` and `mailto:` functionality.
- Preserve the house icon + `Neighborhoods` label and magnifying-glass icon + `Search` label; do not make these icons-only on desktop/tablet.
- On narrow phone screens, prevent overlaps/clipping while remaining faithful to the existing header.

---

## 4. HOVER NEIGHBORHOODS + HOVER SEARCH — THESE ALREADY EXIST, PRESERVE THEM

**Both HEADER features open on HOVER on desktop, NOT click.** Keep this behavior from prior work and verify it still functions after changes.

### Neighborhoods

- Hover anywhere over the house icon/`Neighborhoods` hit area to open an attached, compact dropdown immediately.
- Display **EVERY existing city/neighborhood link** with its actual existing destination (not just an example subset). A few names shown previously: Reseda, Canoga Park, Encino, Porter Ranch, Northridge, Winnetka, Sherman Oaks and Chatsworth; inspect the real full set in code.
- Show the cities directly in a compact, comfortably spaced multi-column presentation where width permits. NO `Explore All Cities` intermediary, NO new directory required to get to them, NO plus signs, NO nested city flyouts.
- Hover -> menu opens -> ONE click on a city goes to that city page. Prevent clipping near screen edges and hover closing gaps.

### Search

- Hover over magnifying-glass/`Search` to open its actual working search options immediately. No click to reveal.
- Use ONLY search options/links already supported by the real site. Preserve the working existing Search page and any real destinations. Do not invent search features.
- Keep Search's panel compact, proportional and connected to its header trigger.

### Touch and accessibility

On tablets/phones, use touch tap to open these specific feature menus (hover is unavailable), then tap direct actual destinations. Enable keyboard `focus-within` / Escape behavior; make focus and close functional. Do not change the type of interaction on desktop.

---

## 5. CONSIDERATIONS — MAIN LANDING PAGE BUILT FROM EXISTING EXACT CATEGORIES

**This is the major CONTENT PRESENTATION change.** The owner has already written all article content, already chosen natural wording, and already approved luxury photo-card layouts. Do not rewrite or reinvent any of those things.

**Required visitor flow:**

`Considerations` main menu link (NO dropdown)
→ **Considerations landing page** displaying the **existing former dropdown category names as photographic cards**
→ clicking one category card opens that category's **EXISTING article-listing/category page** with its established individual photo/article cards
→ clicking an article opens the existing article page.

Detailed requirements:

1. Use the existing Considerations landing page if present; otherwise create a single suitable landing page using the site's established internal naming conventions, without changing any existing URLs. Link the top-level `Considerations` menu directly to it. If there is a previously indexed Considerations page, **reuse its URL** rather than create a duplicate.
2. **ONE top-level photo card for EVERY existing Considerations dropdown category**. The card's public visible title is the **EXACT already-written category label from the actual website**. Do **NOT** invent labels, titles ending in `Questions`, or alternatives such as `Financing Questions`, `Buyer Questions`, etc. The existing names are natural sounding. Do not derive a label from a technical file name.
3. Cards MUST visually MATCH the site's other already-approved luxury image/article/category cards: same authentic typography, sage/ivory palette, coordinated substantial dark-sage card borders/frames and separators where those are part of the current approved design, photo crop/aspect, card height behavior, spacing, short excerpt style, hover/focus, responsive columns. **Reuse real existing components/classes/layout patterns.** Do NOT introduce a generic card redesign, bright buttons, UI mockups, floating tiles, or a different visual language.
4. Each card includes: the matching **photo**, exact category **title**, a brief **natural, original 1–2 sentence description** only if the current card convention uses one, and the current approved link/read-more affordance. Descriptions summarize existing category content; do not write them as questions or add unsupported claims. The photo itself must have **NO words overlaid/generated into the image**; site UI text should be HTML/CSS layered in the existing card style as appropriate, not baked into pixels.
5. Card should link DIRECTLY to the associated already-existing category page. Prefer fully clickable card with accessible anchor semantics and keyboard focus. Absolutely no extra “choose another directory” step or extra flyout.
6. All existing category-page article cards, photos, previews, article titles, metadata, article URLs, publication dates, internal links, canonical SEO, and article bodies are PRESERVED. Do not re-author or rename them. Do not delete articles or category pages.
7. Retain access to each original Considerations destination, including older category-level and article-level links that may have been redistributed under Buy/Sell/etc. If simplifying old Buy/Sell dropdowns, verify these destinations are still reachable via the new Considerations landing → original categories and by relevant existing contextual links. Don't break SEO discoverability.
8. Responsive photo grid: elegant desktop card layout with balanced rows; appropriate tablet layout; single column on smaller phones. Do not introduce overly tall blank card bottoms or orphaned short rows. Validate all genuine photos and alt text.
9. Card image files get normal descriptive names/alt text, appropriate loading and size handling. Never replace images throughout unrelated pages. Preserve all existing site graphics and any genuinely approved Dominique photos already elsewhere; **do not fabricate or generate any additional images**.

### PHOTO RULES — already settled

The owner supplies the category-card photos. **Do not generate more photos, create image collages or pictures with text.** Do not depict a made-up real estate agent or attempt to generate a fake Dominique likeness. Use lifestyle/home/family/design/financing imagery relevant to the existing category. For provided images containing people, follow the owner's stated preference for Black, Asian, Mexican/Latino, or Middle Eastern subjects, not white subjects. If an image violates a known approval constraint or seems to portray another agent, flag it rather than silently using it.

### IMPORTANT — DO NOT INVENT CATEGORY NAMES

Earlier ChatGPT image-generation attempts incorrectly introduced public labels such as `Buyer Questions`, `Seller Questions`, `Design Questions`, `Financing Questions`, `Short-Term Rental Questions`, or unrelated proposed headings. **These are NOT approved renames and must NOT be inserted into the landing page.** Use the REAL labels already present in the user's code/previous Considerations menu. File names are not public-facing titles.

---

## 6. IMAGE UPLOAD / PLACEMENT — CODEX HANDLES THE FOLDERS

The owner will drag **the downloaded `.md` file AND all newly approved card photos into the TOP LEVEL of the existing `sun-and-sage` folder in VS Code Explorer**, next to `index.html` and the other main HTML files. This is a temporary incoming location; do not require the owner to discover or manually create assets directories.

**Codex, after the photos appear in the project root:**

1. Inspect all newly dropped image filenames and visuals.
2. Create or reuse `assets/images/considerations/` (or the existing site's established image directory if a different pattern is already used; prefer consistency over duplication).
3. **Move/copy** the approved newly supplied images into that folder; give them short descriptive, SEO-friendly filenames where sensible, avoiding collisions. Ensure relative asset paths work from the Considerations landing page and any nested page paths.
4. Map exactly one appropriate photo to each required category card, using owner-provided photos first. Existing approved images can be reused if suitable. If photos outnumber cards, do not invent extra sections. If a category has no suitable available photo, report precisely which category rather than adding an unrelated stock photo.
5. Optimize for web carefully if appropriate, preserve source originals or source backup, add `loading="lazy"` for offscreen cards, meaningful `alt`, stable aspect ratios and no visual shifts. Don't embed title text into image pixels.
6. Provide a final clear mapping: `exact card title -> file used -> existing category URL`.

**The owner should not have to drag photos one-by-one into a hidden folder.** Codex can move them after they are dropped into root.

---

## 7. SIMPLIFY THE REST OF THE MENU WITHOUT HIDING CONTENT

The owner and Dominique disliked gigantic mega-menus, dropdown-inside-dropdown-inside-dropdown, too much clicking, huge blank rectangles and long unrelated lists. Keep the navigation inviting, concise and easy to scan.

- `Buy` and `Sell`: Keep a modest set of important, already-existing direct destinations, with names taken from the current actual pages. `Buy With Dominique` is a key buying destination. **Remove the giant city grid from Buy** (cities now live under the special Neighborhoods header feature). Avoid deeply nested flyouts of every article. Detailed educational content is easily discoverable through the Considerations photo-card landing and related existing category/article pages; don't bury it behind repeated extra hover/click levels.
- `Property Management` and `Interior Design`: Show their real subpages in compact dropdowns; fit to content and preserve existing links.
- `Life Changes`: Keep major real-life topic links such as the site's actual Marriage, Growing Family, Relocation, Empty Nest, Retirement, Divorce, and Death of a Loved One destinations as currently named/linked; no oversized menu panel or dead space.
- `Blog`: Keep visible as a direct main nav destination. Article discovery via the existing blog/category card layouts.
- `Considerations`: **NO DROPDOWN — directly opens its image-card page.**
- No site-wide removal of articles, no SEO-harmful orphaned pages. Audit actual crawlable HTML links and XML sitemap; add/adjust entries only where truly necessary for the new Considerations landing page, without losing previously indexed pages.
- NO arrows/plus signs on desktop dropdown labels. Compact ivory and sage dropdowns should appear immediately under the category, not detached lower on the page. Preserve actual hover-to-open behavior.

---

## 8. QA — SITE-WIDE CONSISTENCY AND VISUAL PROOF

This website comprises hundreds of static HTML pages. Update the true shared header/JS/CSS source, or safely apply any necessary page-wide changes without overwriting other ongoing edits.

**Test actual CSS viewport sizes:** 320, 375, 390, 430, 600, 650, 744, 768, 820, 834, 1024, 1180, 1280, 1366, 1440, 1920. Test the view itself rather than relying solely on CSS/media-query statements or browser zoom.

**Required screenshots/visual inspection:**

- Desktop (1440) homepage/header showing TEN nav labels + Neighborhoods and Search before contact info, unchanged logo/RISE branding.
- iPad portrait (768 and 820/834) with the **nav visible and NO hamburger**; show exactly how all TEN items remain accessible.
- iPad landscape (1024) with visible nav, no hamburger.
- Phone (390) with MENU closed and **MENU OPEN**, including `Considerations` as a direct link and the expanded state of a genuine category.
- Desktop OPEN Neighborhoods and OPEN Search separately. Check hover stability, dropdown size, link targets and viewport overflow.
- Desktop OPEN Buy, Sell, Interior Design, Life Changes to verify they are compact and not enormous/empty. Hover `Considerations` and prove it does **not** open a submenu.
- Considerations landing at desktop/tablet/mobile, showing the owner-provided category photos, exact existing labels, matching approved card design, and no embedded text.
- One clicked category card leading to an **existing** article-card listing; one clicked article card leading to the existing full article. Check navigation links on nested pages, e.g. `life-changes/...`.

**Functional checks:** pointer hover, keyboard navigation and focus, Escape, iPad touch tapping, phone tap, navigation click targets, `tel:`/`mailto:`, real Search/Neighborhoods destinations, all Considerations category destination URLs; no JS console errors, broken image src, missing link targets, duplicate broken sitemap entries, or horizontal overflow.

**No unrelated changes:** Preserve Dominique's video/door-opening homepage hero, RISE branding, blog content and dates, existing page-specific designs, sitemap/indexed URLs, SEO/AEO content, city/region pages, portfolio visuals, approved cards, global fonts/colors, and other business work.

---

## 9. FINAL REPORT + STOP

When finished, report:

1. The exact 10 main navigation labels and confirmation that Considerations goes directly to its landing (NO dropdown).
2. Confirm **phones have MENU; iPads/tablets do not**. State breakpoints used and any tablet single-line scroll fallback and show evidence.
3. Confirm `Neighborhoods+Search` and `phone numbers+email` were simply SWAPPED in the header, without changing the rest of its architecture.
4. Exact category name -> photo filename -> linked existing category page, including any link/image that could not be mapped confidently.
5. Files changed, screenshots/preview paths, and a concise list of any unresolved technical or content issues. Do not claim all widths are good without actual inspection.
6. Confirm **NOT committed, pushed, deployed, or published**.

**STOP for owner approval. Do not decide to redesign any other website areas.**
