# DommyDom — FINAL NAVIGATION RESTRUCTURE + CONSIDERATIONS REORGANIZATION

**Project:** DommyDom / Dominique Duncan-Nelson website
**VS Code repository/folder:** `sun-and-sage`
**Status:** Implement locally, visually verify, and STOP before publishing.

## Read this first

This specification records the navigation arrangement approved by the site owner. **Do not improvise a different menu, rename the approved top-level labels, or redesign the whole website.** The earlier oversized navigation, two-column disconnected tablet directory, accordion menus with lots of clicking, and overloaded hamburger are NOT the goal. Fix the menu structure and responsive behavior while protecting the existing luxury brand.

## 1. Exact top-level navigation — nine categories, in exactly this order

1. **Home**
2. **About**
3. **Buy**
4. **Sell**
5. **Property Management**
6. **Interior Design**
7. **Life Changes**
8. **Blog**
9. **Contact**

These nine labels are deliberate. In particular, **Buy** and **Sell** must remain separate because Dominique specifically requested it. Do **not** collapse them into "Real Estate" or "Services." **Life Changes** stays a top-level category. **Blog** stays top-level. **Home** must be explicitly visible in navigation even if clicking the logo also leads home.

**Remove `Considerations` and `Search` as top-level menu entries, without deleting their existing pages.**

## 2. Search is a separate header feature

- Keep the existing DommyDom brand/logo at the **left of the upper header row**.
- Place a discreet, refined **magnifying-glass icon plus the visible word "Search" at the upper-right** of the header, as one clickable/tappable Search control.
- The Search control must link to the **existing working Search page/experience**, preserving current destination and behavior; do not fabricate a new Search page.
- Search is **not** a tenth navigation label, and is **not hidden exclusively within Buy**. If a related property-search link already exists in the Buy dropdown, evaluate whether it is useful and avoid awkward duplicate navigation; the top-right Search control must remain available regardless.
- Match the site's established dark sage, ivory, white, spacing, typography and luxury editorial identity. Make the label easy to see and the touch target usable. Do not create a giant attention-grabbing search bar.
- Do not hide the Search control at laptop/tablet widths merely because the rest of the menu changes responsive mode; preserve convenient access when possible.

## 3. Desktop dropdown behavior and presentation

- Top-level navigation should appear as **a single clean horizontal row** where it can fit properly. Never wrap into an awkward double row, squeeze text to unreadable sizes, or let navigation overlap Search/logo.
- No visible dropdown indicators: **no arrows, chevrons, carets, triangles, plus signs, or accordion icons** next to category names.
- For categories already having dropdowns, opening the dropdown on **hover** on desktop should work naturally and smoothly, as requested. It must not require clicking on desktop just to reveal links.
- Preserve sensible click behavior for primary links, and support keyboard focus (`:focus-within`/appropriate accessibility), so links remain accessible beyond hover.
- Dropdown panels should feel cohesive, tasteful, clearly associated with the hovered category, and should not close the instant the pointer moves between the category and its submenu. Do not hide or orphan relevant pages.
- Keep categories that currently link directly to their own pages clickable; do not replace every navigation label with a dummy button or empty `#` anchor.
- Do not change the underlying brand, sitewide fonts, logo, content, hero, or other unrelated design elements.

## 4. Rehome ALL Considerations content under the appropriate subjects

The former `Considerations` main-navigation category should be removed **only from the header's top-level navigation**. Its underlying articles, landing pages, subcategories, assets, and links MUST remain live and accessible.

**First inspect the current project's actual Considerations links and all destination URLs.** Create an internal list of EVERY original linked destination and where it will be reached in the new navigation. Do not guess from titles alone if the page context clarifies intent.

Move/discoverability-map those links as follows:

- **Buy:** property purchase considerations, finances/financing, finding a home, offers, inspections, or decisions a purchaser faces.
- **Sell:** listing, timing a sale, preparing a home, pricing, negotiations, or seller decisions.
- **Life Changes:** divorce/separation, empty nest, growing family, retirement, bereavement, relocation, or other life-transition articles when those situations are the central topic. Life Changes is NOT to be collapsed into Buy or Sell.
- **Property Management:** rental ownership, leasing, landlord/tenant, ongoing asset-management subjects.
- **Interior Design:** design, renovation/visual presentation, or home styling where this is genuinely the subject.
- **Blog:** articles should remain accessible in the site's existing blog/category/article navigation as appropriate; do not dump every item under Blog as a substitute for relevant topic-based access.

**Use only actual existing links and pages.** If an item has more than one natural relationship, choose a clear primary navigation home and optionally link contextually elsewhere; avoid cluttering every dropdown with duplicates. If an existing Considerations landing page is still useful, retain it as a valid page and link it contextually where appropriate—not in the main nine labels. Preserve all live URLs, their article copy, publication dates, images, metadata, internal links, and SEO. **No redirects or URL renaming unless a real broken link is discovered and can be fixed without breaking indexed pages.** Never delete pages to make the menu smaller.

Also audit existing Buy, Sell, Life Changes, Property Management, Interior Design, Blog and Contact navigation destinations so reorganization doesn't accidentally remove any previously available links. Preserve all relevant existing subnavigation and avoid inventing filler content.

## 5. Tablet and mobile — fewer clicks, no awkward menu

- Test actual iPad/tablet widths and browser preview widths instead of assuming a CSS breakpoint means the layout is visually acceptable.
- Show the horizontal nine-item nav on wider views **only when it truly fits at readable size**. Do not force a hamburger on normal desktop/laptop widths; equally, don't force nine labels into a tablet width if that makes the menu cramped or wraps it onto two rows.
- For touch devices, a user must be able to open a submenu **with a tap** (hover isn't reliable). Preserve an accessible way to visit the top-level category page when the category also has a dropdown. Keep the interaction discoverable **without showing arrows/plus signs**.
- If a genuinely narrow tablet/phone requires a MENU control, opening it should display the approved nine primary labels promptly and coherently. Avoid the former disconnected left/right columns and avoid making users click through deep nested accordions. One straightforward submenu interaction when necessary is acceptable; endless nested tapping is not.
- Mobile menu should be clean, single-flow, readable, scroll naturally if needed, close correctly, and not overlay or obscure critical content without a clear way to dismiss it. Avoid both giant empty space and cramped text.
- Make top-right Search readily accessible and clickable/tappable on touch screens.

## 6. Engineering + full-site consistency

- Inspect how the shared header is actually implemented (shared partial, script-generated markup, or repeated copies). Update the true shared source or every necessary template/page consistently, rather than only the homepage.
- Find any conflicting CSS/media queries/old nav script behavior and fix the ROOT CAUSE rather than stacking yet another overriding CSS rule.
- Preserve existing working dropdowns, links, focus behavior, SEO markup, responsive structure, content and imagery.
- Respect relative URLs from nested folders (`life-changes/`, `buy/`, etc.); confirm links still work from pages at different directory depths.
- Do not introduce extra main-menu categories, a new Services umbrella, a Real Estate umbrella, or new navigation copy without approval.

## 7. Non-negotiable visual/function QA

Open and inspect the page visually at **1920, 1440, 1280, 1024, 820, 768, 600, 390, and 320 CSS pixels**, or the closest actual available screenshot/view sizes; explicitly include an iPad portrait width and a desktop/laptop preview. Test at least the homepage, one Buy page, one Sell page, one Life Changes page, one former Considerations destination, and one deeper nested blog/article page.

Verify:
- Logo left / Search icon + "Search" right in upper header; all nine menu labels exactly as approved.
- Desktop nav fits on one row without collision or tiny text.
- Desktop hover dropdowns open/close correctly, no arrows or + indicators, links are click-ready.
- Touch dropdowns are usable without a mouse, and Search works at phone/tablet widths.
- Each former Considerations destination remains live and can be found from an appropriate category or contextual navigation.
- All existing main pages still have working links from the header, regardless of nested directory depth.
- No text, images, pages, metadata, blog dates, URLs, or other design elements accidentally change.

## 8. Completion report and approval gate

When finished, report:
1. Which header/CSS/JS files were changed.
2. The exact final nine labels plus separate top-right Search feature.
3. A compact mapping of every former Considerations dropdown destination to its new discoverable menu location (include URLs so owner can verify nothing is missing).
4. Visual screenshots or precise previews at desktop, iPad portrait, and phone sizes.
5. Any URLs that were broken before you started and how they were handled, if applicable.

**Do not publish, push, or deploy until the owner approves the finished navigation.** Keep scope strictly to the header/navigation and link relocation/discoverability. The goal is a shorter, more beautiful menu without sacrificing any content or making visitors click excessively.
