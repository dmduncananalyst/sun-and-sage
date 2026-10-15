# DOMMYDOM — EXACT HEADER + OPEN MENU RESPONSIVE REPAIR

**Repo/folder:** `sun-and-sage` (DommyDom / Dominique Duncan-Nelson).  
**Scope:** Sitewide header, navigation and OPEN mobile/tablet menu only.  
**Instruction priority:** This document supersedes earlier conflicting navigation/header prompts. Do NOT redesign any content sections, hero layouts, typography elsewhere, article cards, city pages or site structure. Do not commit, push, or publish until approved.

## WHY THIS REPAIR IS NEEDED — ACTUAL SCREENSHOTS

Current screenshots show TWO equally unacceptable outcomes:

1. **Narrow desktop / tablet-width preview (~650–750 CSS px):** Signature logo left, RISE logo far right, two phone numbers and email crowded together on a left-aligned middle row, Neighborhoods and Search crammed on the left of yet another row, isolated MENU button far right. The right side of the contact row is vacant. The header feels like elements wrapped at random; it has dead space *and* crammed areas.
2. **Wider laptop/desktop preview (~1300–1400 CSS px):** Logo, both phones, email, RISE, Neighborhoods and Search are stretched into one crowded utility line; full 9-item nav on a separate line. This feels pinched, busy and poorly proportioned rather than luxurious. Do NOT solve the problem by increasing header height, adding yet more lines, or shrinking all text until it fits.
3. The open hamburger MENU itself has not been designed carefully enough. It must feel as polished as the closed header. The client strongly dislikes needless clicking and endless menus.

**Outcome:** One coherent premium editorial header family, with **intentional** layouts for full desktop, medium/laptop, tablet and phone. No awkward intermediate width where the design breaks, no giant blank regions, no navigation that splits into two lines of menu items. Visually prove that it works.

## NON-NEGOTIABLE CONTENT / FUNCTION

- Keep Dominique's **actual existing signature logo**, RISE × REAL marks, BOTH existing phone numbers, existing email address, and existing real links/actions. Never use placeholder brand text or new phone/email details.
- Main navigation (preserve exact labels and original destination links): **Home | About | Buy | Sell | Property Management | Interior Design | Life Changes | Blog | Contact**. Exactly nine. Do not restore Considerations as a main item, and do not add vague 'Services'. Buy and Sell must remain distinct.
- Header actions: **house icon + “Neighborhoods”** and **magnifying glass icon + “Search”**, visibly distinct from main nav. These are not part of Buy.
- **Desktop hover only to OPEN** the Neighborhoods menu, Search menu and main-nav dropdowns. Do not require a preliminary click and do not include arrows/chevrons/pluses beside desktop nav categories. Clicking a final link navigates directly to that page.
- Neighborhoods: ALL currently existing real city/neighborhood destinations, immediately available in a thoughtfully composed dropdown or panel on hover; do not send visitors to an intermediate “Explore All Cities” directory. Preserve correct destination URLs and display names.
- Search: hovering opens the EXISTING functional Search menu/options (audit current implementation and preserve true destinations). Do NOT replace with an inert mock menu, dummy input or fabricated functionality.
- Small-screen/touch devices: hovering is not reliable; accessible TAP interaction to reveal a menu or submenu is APPROVED and necessary. It must not require multiple needless intermediate pages. No random extra accordions or 'Explore All' links. Avoid duplicate tap-to-open plus tap-again-to-open another nested control.
- Preserve all currently reachable Considerations content under appropriate existing sections, unchanged URLs, all city pages and articles. All 351-ish pages must retain correct headers, original links, SEO and content.
- Preserve current luxury palette (muted sage/olive, ivory/white, fine restrained borders), existing fonts and logos. No loud colored buttons, giant card outlines, generic giant white panels, or unrelated styling changes.

## EXACT LAYOUT DESIGN RULES

### A. FULL DESKTOP — when both main nav and utility information can fit genuinely comfortably (often >= 1380–1440 CSS px, but measure instead of treating these numbers as magic)

- Build one coherent **compact two-tier header**, not a random two-row wrap:
  - **Identity/utility tier**: Signature logo anchored LEFT with a deliberate margin; a gracefully spaced area for the TWO phone links and email (not all jammed together, not drifting into logo); RISE marks visually grouped with identity, and the Neighborhoods/Search action pair together toward the RIGHT. Use flex or CSS grid with explicit areas, safe min widths and gaps.
  - **Navigation tier**: ALL nine navigation items on **one single unbroken centered horizontal line**, with consistent optical spacing, restrained top/bottom padding, and no wrapping.
- The *entire header* must be proportionate, compact and editorial, NOT an extra-tall white slab. It is acceptable to have one slim utility tier plus one slim nav tier when each has a clear purpose; it is NOT acceptable to have a tall, crowded first line and a second line just because items overflowed.
- Prioritize comfortable reading sizes. Reduce oversized horizontal margins, redistribute groups and use graceful spacing *before* changing typography. Do not shrink links to illegibility or collide logos.
- The full-width white/header background should look finished: content occupies the width in balanced zones with controlled side gutters, not everything shoved to one side and empty acres elsewhere.
- The RISE marks are an important part of the branding: keep their readable relative size and spacing.

### B. INTERMEDIATE LAPTOP WIDTHS (~1024–1439 CSS px)

- **This is the problem area.** Do NOT stretch the full utility line beyond capacity; do NOT let the main nav wrap; do NOT auto-wrap contact details onto an accidental extra line.
- Use explicit content-aware breakpoints. As soon as 9 navigation items or contact areas cannot fit with *real* breathing room, switch to the **intentionally designed compact header** below. It is better to switch a bit earlier than to retain a painfully cramped faux-desktop layout.
- If a single-line full nav fits comfortably at a given width, show it; if not, switch to MENU. Never display a partial/cropped nav or two rows of nav buttons.

### C. TABLET / COMPACT WIDTH — including the approx. 650–750px preview in Screenshot 5005 and tablet portrait

- **MAXIMUM TWO compact, intentional header bands** (never the screenshot's disconnected three-row effect):
  1. **Brand band:** Signature logo on the LEFT; RISE × REAL grouped on the RIGHT, vertically centered. Their sizes must work together. No isolated phone/email cluster on its own row.
  2. **Actions band:** Neighborhoods + Search grouped neatly (icons + text) and a consistent MENU button aligned toward the right/opposite side. Distribute them across available width with meaningful edge alignment and breathing room. Do not strand MENU far away or force all controls into a tiny left cluster.
- Put both existing phone numbers and email as easily visible, tappable contact details **inside the OPEN tablet/mobile MENU** (at an attractive top or bottom utility strip), rather than cramming them into a third header row. Their presence and clickability must be preserved.
- Use compact, reasonable vertical margins. The page content should begin shortly below the header rather than being pushed down by a huge white slab.
- Do not render a fake desktop header at narrow window widths merely because the user happens to be viewing it inside VS Code.

### D. PHONE — 320px, 375px, 390px, 430px

- Compact brand/signature at left; thoughtfully scale or reposition RISE without crushing the logo. Menu, Neighborhoods and Search remain discoverable and tappable without overflowing.
- Allow a small controlled second actions row if needed, not arbitrary third/fourth rows. Use real responsive sizing, NOT CSS zoom or uniformly scaled whole header.
- No horizontal scrolling, clipped links or overlap with the top of the page.

## OPEN MENU — DESIGN THIS, DON'T JUST MAKE IT WORK

- MENU tap opens **one elegant, coherent surface** under the compact header, aligned with the page gutters; accessible close control clearly visible and not off-screen.
- Show nine primary navigation categories in a clear, compact, readable **one-column visual hierarchy**; this is **not** a giant two-column collection of disconnected categories, and **not** an unbounded dump of all 351 articles.
- On touch: tapping a category with children reveals the directly relevant links **inline in the same panel**; no routing to pointless intermediate directories and no nesting more than necessary. Categories with direct destination can still be reached (ensure parent destination is available if applicable). Expanded content should be readable, appropriately indented, and visually related to the parent. Use touch-friendly target heights.
- Do **not** pre-expand every city, article and question. Only show the nine main nav categories until a relevant section is selected; otherwise the menu becomes hundreds of links long. Remember that mobile tap-to-expand is acceptable; desktop must be hover-to-expand.
- Neighborhoods and Search have their own clear controls in the closed header. On tablet/mobile, tap these controls to open their respective **direct options**; tapping the selected city/search destination should navigate directly. Full city list may be scrollable *within a bounded viewport-aware panel*; do not shrink text or overflow offscreen.
- The phone numbers/email appear in a beautifully spaced utility area within open mobile/tablet MENU; phone links use correct `tel:` format and email uses `mailto:`.
- Ensure screen readers, keyboard focus/Enter/Escape, pointer hover, tap-outside, and close button all work. Avoid bugs where pointer crossing a tiny gap dismisses the submenu, or where the panel is hidden behind the hero.
- No arrows, chevrons or plus signs cluttering the desktop main nav. Where touch needs affordance, use careful hierarchy and clear interactive text; do not introduce oversized accordion icon columns.
- OPEN menu should be **visually inspected** on phone and tablet, not just the closed header.

## DROPDOWNS AND SPACING — ALL NINE MAIN CATEGORIES + BOTH HEADER ACTIONS

- Position dropdown flush/visually connected directly beneath its trigger, avoiding awkward top gaps, and guarantee no flicker when pointer moves into it.
- Compact small dropdowns (Interior Design and Life Changes especially): no giant white rectangles around five links, no excessive link-to-link spacing, no gratuitous dead space. Preserve all links.
- Desktop Buy should NOT contain the giant city directory now that Neighborhoods is separate. Organize remaining buyer resources thoughtfully, with priority to **Buy With Dominique, First-Time Homebuyers, Buying Process, Financing, Buyer Resources**. Use hover submenus only where actually helpful; retain access to every buyer article, with no new unnecessary click-through directory pages. Correct any duplicate redundant labels only after confirming destination uniqueness.
- Neighborhoods header dropdown should be a compact, intentionally arranged multi-column city list (e.g. a 3–4-column editorial flyout, depending on available room), anchored to the trigger and kept within the viewport. Its city labels must be comfortably readable and directly clickable. Do not use a huge blank megamenu or a narrow panel hundreds of pixels tall.
- Search header dropdown should likewise be proportional to its real links/options, not huge empty space.
- For any flyout near viewport right edge, smart-align inside the screen. Do not let it clip or force page sideways. No synthetic placeholder links.

## IMPLEMENTATION REQUIREMENTS (PREVENT ANOTHER FALSE “FIXED” REPORT)

1. Inspect all existing header markup, shared stylesheet(s), JS controllers, and responsive CSS source order before editing. Find duplicated and conflicting rules from prior Codex instructions/iterations. Locate the real cascade that controls the layout at narrow, intermediate and desktop widths. Do not simply append another high-specificity emergency patch while conflicting older rules remain active.
2. Use the fewest necessary maintainable shared changes across sitewide templates, preserving per-page content, CSS and assets. When handling many static HTML pages, automate carefully with validation; don't rewrite 351 unrelated page bodies.
3. Keep search/Neighborhoods hover behavior and links FUNCTIONAL, not simulated for screenshots. Confirm desktop pointer, keyboard, mobile touch, dropdown transition, and opening/closing.
4. Compare the BEFORE screenshots (5005 narrow and 5006 wider) against AFTER at matching browser content widths; test preview viewport, NOT simply physical monitor size. Avoid testing browser zoom as a substitute for real CSS viewport widths.
5. **Actual visual screenshot evidence** required at CSS widths **320, 390, 650, 768, 900, 1024, 1280, 1366, 1440, 1920**. For each, confirm layout doesn't wrap unexpectedly, branding isn't cramped, navigation doesn't split, and hero remains untouched.
6. At minimum supply screenshots **with OPEN MENU** at 390 and 768, **OPEN Neighborhoods** at 768 and 1440, **OPEN Search** at 768 and 1440, and **OPEN Buy, Interior Design, Life Changes** at 1440. Carefully inspect all for proportion and overflow.
7. Test actual representative pages including home, a Buy page, a Sell page, a Life Changes page, a city page, and Blog. Check shared header consistency and run a link/URL audit so no previous destinations disappeared.
8. Provide concise report: root cause(s), exact files changed, which breakpoints used and why, screenshots or precise preview paths, any remaining limitations. **Do not claim all breakpoints look great without visual evidence.**
9. Do **not** commit, push, deploy or publish. Let user approve visuals first.

## ACCEPTANCE CRITERIA (FAIL IF ANY VIOLATED)

- At ~680px, logo & RISE balance on one brand band; Neighborhoods/Search/MENU balance on one compact controls band. There is **NO THIRD CONTACT ROW**, no cramped left cluster, and no acres of unused right-side space.
- At ~1366px, header feels compact and harmonious, not a squashed single line plus a swollen nav. All 9 main nav links fit a SINGLE nav line when shown; switch to compact if that can't be achieved comfortably.
- At desktop, Neighborhoods, Search, and dropdowns OPEN ON HOVER with NO preliminary click and NO arrows/plus signs. City links are available directly in Neighborhoods, not hidden in Buy or an Explore All page.
- Touch menu and its open state are beautifully organized and don't expose hundreds of links at once; phones, email, RISE, signature, links all preserved.
- No design, SEO, copy, images, videos, hero content, city content, or article pages changed outside the shared header/nav.
- Screenshots inspected, working behaviors verified, original destination links preserved, and nothing published.

**Directive:** Stop editing when the result is visually verified and matches the criteria. If a specific requested behavior is technically constrained at a width, solve it with the responsive compact layout rather than silently inventing a compromised third-row layout. Report constraints clearly instead of claiming success.
