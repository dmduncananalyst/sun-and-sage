# DommyDom — Fix Oversized Article Cards and Excessive Empty Space

## Goal
Make article-preview cards compact, elegant, consistently sized, and easy to scan. The current cards have enormous areas of unused white space between the excerpt and the “READ MORE” link. Fix the actual layout problem rather than padding every card with unnecessary writing.

## Where to begin
1. Start with the article-card grid on `life-changes/marriage.html` (the page in the attached user screenshots). Rows of three cards are currently much taller than their content warrants.
2. Inspect the CSS and any shared template/component used for these cards.
3. Identify other **article-preview grids of the same design** across DommyDom where the identical spacing problem appears, and apply a consistent fix there if they share the same component. Avoid touching unrelated property listings, city information sections, service tiles, navigation, or other card types.

## Problems to correct
- Excessive empty space below brief article excerpts and above “READ MORE.”
- Card height appears dictated by an unnecessarily large fixed `height`/`min-height`, oversized grid tracks, spacer blocks, or similar rules, rather than the actual content.
- Cards should not look visually mismatched or have differently positioned “READ MORE” links.
- Different rows should feel like one consistent, intentional editorial grid, not an assortment of oversized empty boxes.

## Exact visual requirements
1. **Keep the three-column layout at desktop widths**, and preserve existing responsive column behavior where appropriate. Make all cards in the same row equal in height and width, with their bottoms and “READ MORE” links aligned.
2. Aim for a **consistent, compact overall card height across the listing** when content allows; do not use excessively tall fixed dimensions simply to make cards match. A little breathing room is desirable. A huge blank area is not.
3. Keep the existing approved images, their placement and aspect ratios, typography, neutral/ivory colors, understated thin rules and borders, headings, category labels, and link style. Do not redesign the page.
4. Make card content flow naturally: image (if present), category label, headline, excerpt, then a modest gap and “READ MORE” at the bottom. Do not vertically center the body paragraph in a giant container or reserve hundreds of unused pixels beneath it.
5. Keep “READ MORE” in the same bottom position for cards within each row. Use a robust grid/flex layout (for example, a flex column with `margin-top: auto` for the footer/link) rather than large artificial spacers.
6. Review `height`, `min-height`, `grid-auto-rows`, `align-items`, absolute positioning, margin and padding rules, and any overly tall image or content placeholders. Remove or reduce the **specific rule causing the excess height**; do not add arbitrary negative margins or hide overflow to camouflage it.
7. Keep sensible and consistent vertical spacing between rows. The following row's images should begin soon after the previous row's links, separated by a tasteful gap.
8. Where a title naturally wraps to more lines, let the card accommodate it gracefully while keeping cards aligned. Avoid clipping text.

## Excerpt lengths: use substance, not filler
- First solve the CSS/layout issue.
- If one card still feels noticeably sparse compared with nearby cards, you may slightly expand its excerpt **only using relevant, accurate information from that specific existing article**. Aim for excerpts of roughly similar reading length, without rigid word-for-word matching.
- Do **not** invent facts, add generic promotional filler, repeat sentences, or change full article bodies just to fill visual space.
- Do not duplicate excerpts or alter SEO meta descriptions unless they actually serve as the visible card excerpts and must remain accurate.
- Preserve the intended meaning and tone of DommyDom's current editorial copy.

## Desktop and mobile checks
Test the affected article-card grids, especially the Marriage page, at 1920px, 1440px, 1366px, 1024px, 768px, and 390px widths. Also review the narrow VS Code integrated preview, but do not rely on it alone.

Verify that:
- cards are aligned and have reasonable, consistent heights;
- no prominent dead zones remain;
- images load at consistent sizes where used;
- card text is fully readable;
- “READ MORE” remains clickable and consistently positioned;
- there is no overlapping text, clipping, unusual stretching, horizontal scrolling, or layout jump;
- the mobile cards are readable in a single column (or the site's existing suitable mobile layout) without oversized forced blank space.

## Strict protections
- Do not redesign site navigation, homepage, article pages, city information sections, dropdown menus, chat, or other site sections.
- Do not remove articles, images, links, metadata, or approved content.
- Do not change the actual article text except for small, justified preview-excerpt adjustments as described above.
- Prefer minimal, targeted changes to the existing article-card styling; review any shared CSS impacts before changing common selectors.
- Do not commit, push, or publish to GitHub until I approve.

## Final report
Report: the root cause of the excess white space, the files and selectors modified, whether visible excerpts changed, which article-card grids you checked, screenshots or preview instructions, and any remaining limitation. Only claim tests you actually performed.
