# DommyDom — UPDATED HEADER & HOVER NAVIGATION (APPROVED DIRECTIONS)

**Project:** Dominique Duncan-Nelson / DommyDom luxury real estate website  
**Existing VS Code repo:** `sun-and-sage`  
**Scope:** Header navigation, dropdown layout/behavior, and discoverability of existing destinations ONLY  
**Approval:** Implement locally and provide visual proof. **DO NOT commit/push/publish/deploy until approved.**

## IMPORTANT — THIS DOCUMENT SUPERSEDES CONFLICTING NAVIGATION INSTRUCTIONS

The previous file `DommyDom-Final-Navigation-and-Considerations-Codex.md` remains useful for the nine navigation labels, preservation of Considerations pages, QA, and website-wide consistency. However, **its instruction to make Search merely a clickable link is superseded**: **BOTH Search and Neighborhoods are separate upper-right HEADER CONTROLS whose complete dropdowns open automatically on HOVER on desktop.** Neighborhoods is **NOT** inside Buy. Do not revert to the giant Buy mega-menu, do not bury Neighborhoods under Buy, and do not invent another header arrangement.

Read the current code and inspect the current rendered menu first. Fix the actual shared header source and related CSS/JavaScript rather than adding layers of contradictory overrides.

## 1 — EXACT TOP HEADER LAYOUT

- Preserve the authentic Dominique Duncan-Nelson logo on the **left**; preserve existing telephone numbers, email, RISE × real branding, fonts, and luxury sage/ivory/white aesthetic.
- On the **right side of the TOP header row**, place **two distinct, attractive controls side by side**:
  - A subtle **house/neighborhood icon + the visible word `Neighborhoods`**.
  - A subtle **magnifying-glass icon + the visible word `Search`**.
- Preferred order from left to right: **Neighborhoods | Search**. Do not turn them into top-level labels in the horizontal navigation row below, and do not show icons-only on desktop.
- Use existing project icons if suitable or lightweight accessible SVGs; tasteful, subtle, aligned icon/text sizes. Do not use a giant search input/bar in the header.
- Keep the header composed and balanced across real laptop and desktop widths; gracefully adjust inner gaps, not by hiding the business identity, shrinking text to tiny sizes, or creating a crowded/double-row navigation.

### Main horizontal navigation (EXACT labels and order)

**Home | About | Buy | Sell | Property Management | Interior Design | Life Changes | Blog | Contact**

- **Nine categories only** in the primary horizontal row.
- Dominique specifically wanted **Buy** and **Sell** separate. Do not combine as `Real Estate` or `Services`.
- **Do not** add `Search`, `Neighborhoods`, or `Considerations` to this horizontal row.
- No visible arrowheads, triangles, chevrons, carets, plus signs, or indicators on ANY nav items or header controls.
- Keep existing parent destinations accessible as appropriate (e.g. Buy can remain a real link to its approved page), while HOVER—not click—is what exposes desktop submenus.

## 2 — MANDATORY DESKTOP HOVER BEHAVIOR FOR THE TWO NEW HEADER FEATURES

### NEIGHBORHOODS — hover to display ALL cities directly

1. Hover over **house icon, `Neighborhoods` text, or its unified hit area**. The **full actual Neighborhoods dropdown must immediately appear**. **No click to open.**
2. The dropdown must display **every existing city/neighborhood destination that was previously in the enormous Buy city grid**, all visible within a compact, readable, orderly multi-column listing (scrolling the menu itself only when necessary for viewport height). Include existing regional destination pages if currently part of that list. Examples seen in the current menu include Reseda, Encino, Porter Ranch, Canoga Park, Northridge, Winnetka, Sherman Oaks, Chatsworth, etc. **Audit the actual complete code; do not rely on examples or silently omit any cities.**
3. From the open menu, **one click on an individual city goes directly to that city's EXISTING URL**. No intervening `Explore All Cities` page, second submenu, accordion, expandable plus, click-to-reveal step, or new directory page.
4. The dropdown appears visually associated with **Neighborhoods** in the top header: no giant empty gap, detached rectangle, or panel floating far below its trigger. Since the control is near the top-right edge, position the panel inward within the viewport so the full city list stays visible, not clipped offscreen.
5. Arrange neighborhoods in 3–4 compact columns if available width permits; fewer at smaller desktop widths, with readable line lengths and even gutters. **Avoid the old oversized Buy menu** and excessive padding around every line. Fit the content naturally.
6. Do not repeat the entire city list under Buy. This dedicated feature is what makes the Buy dropdown substantially more manageable.

### SEARCH — hover to display actual search options

1. Hover over the **magnifying-glass icon, `Search` text, or its unified hit area**. Its **Search dropdown immediately appears**, **without clicking** on the Search control.
2. Display **all genuine search-related links/options already supported by this site** and expose the actual existing property/home-search destination prominently (e.g. `Search Homes` if that accurately describes the existing search page). **Inspect the real current Search page/navigation and use its real links, routes, and any existing functionality; do NOT fabricate search features or nonfunctional filter widgets.**
3. Where the current site has only one genuine search destination, show a compact, polished menu containing that actionable existing search destination rather than inventing empty categories. If the existing site supports multiple meaningful search modes, include them without unnecessary additional nesting. Report exactly what was found and implemented.
4. A visitor should **hover to see their real options**, then **click the specific option to go there**. Don't require the visitor to click Search merely to reveal the dropdown; don't require any intermediate page just to see options.
5. Make this Search panel a compact luxury dropdown aligned with and visually connected to the upper-right Search control, not a massive empty overlay.

### Hover interaction and accessibility

- Both panels must stay open while the mouse travels from trigger to dropdown and while moving among menu items; remove pointer gaps/closing flicker. Opening one closes the other cleanly. Hovering out of the trigger+panel closes it reasonably.
- Provide visible-but-discreet focus states and keyboard access (`focusin`/`:focus-within`, Escape to close; focus returns correctly when appropriate). Avoid using mouse-only JS without keyboard access.
- On touch/iPads/phones, **hover does not exist**. Use a natural tap fallback: first tap reveals relevant menu when necessary; then tap the direct link. No additional nesting or awkward accordions. Preserve the ability to reach the landing page where needed, without dead clickable labels.
- Search and Neighborhoods must remain discoverable on responsive/tablet header views even when the primary site navigation switches to the MENU presentation. Integrate them logically in the touch layout without duplicating or hiding the destination links.

## 3 — SHRINK BUY INTO AN INTENTIONAL, EASY-TO-SCAN DROPDOWN

**Remove the entire city/neighborhood grid from Buy** now that all actual city pages are instantly available in the top-right Neighborhoods dropdown. The current Buy mega-menu spanning almost the whole screen is explicitly NOT APPROVED.

The visible first-level Buy dropdown should be **compact and roughly this order** (map each title to existing real pages/links; don't create empty pages):

1. **Buy With Dominique** — direct to the existing buying landing page.
2. **First-Time Homebuyers** — direct to existing landing content (if a suitable landing page exists).
3. **Buying Process** — hover/focus reveals the existing process topics such as touring, making offers, negotiations, closing, preapproval, etc., linked directly to their real pages.
4. **Financing** — hover/focus reveals legitimate existing financing articles/resources where available.
5. **Buyer Resources** — hover/focus reveals other existing buyer questions and related articles, including relevant former Considerations items.

- **Neighborhoods does not appear within Buy**. It has its own top-right control.
- A flyout submenu may be used for these CONTENT GROUPINGS on desktop if it makes the dropdown smaller, but it **must open on hover**; no click-to-expand and no plus/arrow indicators. Links must be one final click from whichever menu is revealed. No artificial directory landing pages.
- Before creating the grouping, audit EVERY currently linked buyer destination and map it to a visible, intuitive group. Avoid duplicate menus and invented labels where real page structure suggests a more appropriate existing title. If a grouping contains only one true destination, simplify it rather than making visitors hover to reveal one item.
- Preserve the existing Buy landing page and its content, images, diagrams, and SEO.

## 4 — COMPACT ALL OTHER HOVER DROPDOWNS

**Current visually observed problems:** `Interior Design` currently produces an oversized pale rectangle for about five links; `Life Changes` shows a tall box with excessive line spacing; `Buy` expands into a near full-page directory; dropdowns feel detached from the header.

- Keep other normal dropdowns (especially Sell, Property Management, Interior Design, Life Changes, About if applicable) compact, proportionate to their actual contents, and aligned directly under their respective navigation labels (with a seamless hover-safe connection).
- Reduce excessive outer padding, line heights and redundant top/bottom blank space; use readable but economical spacing. **Do not compress so much that labels become hard to read or select.**
- If a submenu's first link merely repeats the parent's category and goes to the exact same page, it may be safely simplified; do **not** remove distinct linked destinations.
- Do not add more vertical separators, oversized full-screen overlays, fake headings, extra click layers, or a giant dropdown merely because one section has many links.
- All desktop dropdowns reveal on HOVER. No visible arrows or plus symbols.
- Match the existing upscale ivory and dark sage branding. Avoid broad unrelated design changes.

## 5 — CONSIDERATIONS MUST STAY AVAILABLE, NOT RETURN AS A TOP-LEVEL ITEM

- Continue implementing the previous agreed reorganization: **Considerations** is NOT a tenth main nav category.
- Preserve **every existing Considerations page, destination URL, article, image, date, metadata and internal link**. Relocate its discoverable links under meaningful relevant groups such as Buy/Buyer Resources, Sell, Life Changes, Property Management, Interior Design, and Blog as appropriate to subject matter.
- Map all original Considerations destinations, then verify each new discoverable route. Do not indiscriminately dump everything under Blog, duplicate the entire article list in every dropdown, delete pages, or rewrite content.
- Preserve the rest of the working 351-page site's URLs and relative link paths. A former city/buyer/Considerations link moved to a new dropdown must still be reachable from sitewide headers including nested pages.

## 6 — RESPONSIVE FIT AND MENU QUALITY

- Desktop and laptop: authentic logo, telephone/email and RISE logos remain attractive; top-right Neighborhoods/Search controls visible when there is room; nine-item nav stays one readable row when it actually fits. No wrapping nav across multiple rows.
- If a narrow tablet/phone needs a MENU button, keep it intuitive and reduce needless clicking. **Do not force a desktop-only hover pattern on touch devices.** Neighborhoods and Search must still be accessible there, with direct city links and existing search options.
- Handle narrow browser preview, iPad portrait AND landscape, phone portrait; avoid panel overflow, hidden destinations, clipped scroll regions, accidental horizontal page scroll, and dropdowns blocked by browser/header stacking contexts.
- Large cities panel: use compact columns and safe `max-height`/`overflow-y` when needed; don't make the whole page jump or scroll just to reveal neighborhoods.
- Dropdown placement should remain correct when scrolling / sticky headers / changing zoom. Use anchor-based positioning; avoid fixed absolute offsets that visibly detach menus at different widths.
- Ensure live hero video/door effect, article cards, body sections, metadata, SEO and other layouts remain exactly unchanged.

## 7 — ACCEPTANCE TESTS (MANDATORY, WITH SCREENSHOTS)

Visually inspect at least **1440px, 1280px, 1024px, 820px, 768px, 390px and 320px** CSS viewport widths; include an actual laptop-ish and iPad-sized preview rather than only claiming script assertions passed. Test the homepage and at least one nested Buy page, one Life Changes page, and one other article page that uses the shared header.

**Must visibly prove:**

1. Upper header shows **Neighborhoods (house icon)** followed by **Search (magnifying-glass icon)**, aligned right; existing business branding remains visible.
2. Primary nav shows exactly **Home | About | Buy | Sell | Property Management | Interior Design | Life Changes | Blog | Contact** on fitting desktop widths.
3. **HOVER Neighborhoods:** entire genuine existing city list immediately displays in a well-aligned, compact dropdown; click a city -> direct working city page; no extra steps.
4. **HOVER Search:** genuine search destinations/actions immediately display in a compact anchored dropdown; click a destination -> existing correct Search experience; no click required merely to show it.
5. **HOVER Buy:** small grouped menu with NO CITY GRID. Test Buying Process, Financing, and Buyer Resources flyouts directly on hover if applicable.
6. **HOVER Interior Design + Life Changes:** compact menus with sensible padding, no big rectangles of dead air, and no gap between trigger and dropdown.
7. All dropdowns remain open while moving the cursor; keyboard access works; touch fallback works and nothing is offscreen.
8. Verify every previously shown neighborhood and Considerations destination remains reachable from actual page navigation and works from nested directory paths.

If browser automation is unavailable, be truthful; supply the exact tests actually performed and what still requires owner inspection. **Do not claim screenshots, interactive QA, or all-page link auditing happened if they did not.**

## 8 — REQUIRED COMPLETION REPORT / STOP BEFORE PUBLISHING

Report: (a) which HTML/CSS/JS files were changed, (b) exact options exposed by Search, (c) total neighborhood links found and verified plus any missing/broken routes, (d) how the large Buy menu was reorganized, (e) examples/mapping of former Considerations links to new navigation groups, and (f) annotated or labeled desktop/iPad/mobile preview screenshots showing **OPEN Neighborhoods AND Search menus** plus open Buy/Interior Design/Life Changes dropdowns.

**No publishing, pushing, committing, or deployment before the owner's explicit approval.** Keep scope narrow and preserve every working page and all unrelated design work.
