# DOMMYDOM — Refined dark sage card FRAMES and balanced spacing (v2)

## Task scope
Fix the current article and blog preview cards throughout the existing `sun-and-sage` / DommyDom website. The latest attempt did not fully resolve the problem. Use the user's screenshot examples of the blog grid and Life Changes article cards (Screenshots 4974, 4975, and 4976) to understand the remaining issues.

This is a **targeted correction to existing cards**, not a website redesign. **Do not commit, push, or publish.**

## Problem A: the cards look like thin, faint outlined rectangles — NOT luxurious frames

**This is the user's main visual correction.** The user does **not** want you to merely darken the existing skinny outlines. The cards need a noticeably **more substantial, refined, architectural framing treatment**, like an elevated editorial feature or a finely framed print — not a plain 1px CSS box. The distinction between an outline and a carefully designed frame matters.

**Design direction and required visible result:**

1. Inspect the DommyDom site's existing deep/dark sage-green brand color from its actual CSS and branding. Use that brand color (not bright green, olive, black, or an invented palette).
2. **Replace the flimsy 1px/hairline card outlines with a visibly substantial, continuous dark sage-green perimeter, starting at 3px solid** (or a comparably substantial frame treatment). Its presence should be obvious at a glance even on a full-sized desktop screenshot, **especially around the top and side edges**. Do NOT merely darken the previous 1px border.
3. Make it feel **refined rather than chunky**: consider a tasteful second inner ivory/sage inset rule, subtle layered matting, or a barely perceptible warm shadow *only if it adds a premium framed/editorial feel*. Keep the perimeter itself clearly defined. Avoid bulky cartoon borders, shadows that look like floating app cards, excessive rounding, neon colors, or gradients.
4. Style the image-to-copy transition and the **Read More** footer as part of the same framed composition. The frame must wrap the complete card continuously, including photo, article copy, and footer. Use the existing sage palette for its internal divider treatment.
5. The image should still be flush/aligned as currently designed; don't change the approved image crop/fit. Don't use an unexpectedly oversized green strip around the photo.
6. Retain the clean white/ivory inner surfaces, established typography, image dimensions, and page layout. Let **the frame** supply the bold, intentional presence.
7. Use the same treatment for the actual reusable article-preview card components across the blog and Life Changes sections, not for unrelated non-article panels or buttons.
8. Verify the completed result from **normal screenshot scale**, not only close up. The finished card should read as a beautiful, dark-sage **framed editorial card**, not 'a rectangle with a barely visible outline.' If it still looks like a skinny line, it has not met the requirement.
9. The user wants sophistication **and** visibility. If a plain 3px line still reads as merely a border, refine the framing construction (subtle internal mat/inset line or coordinated frame-and-footer treatment), not just thicker or darker lines indefinitely.
10. Keep all links and keyboard focus indications visible and functional. Preserve existing content, spacing hierarchy, and photography.

### Clear acceptance test for framing
- A viewer should immediately notice each card's **intentional dark sage-green frame** while still seeing an airy, elegant interior.
- Every side of the card, including the outside left of the first card and outside right of the last card, must be clearly framed.
- The design must feel more like a **luxury editorial portfolio frame** than a faint 1px grid outline.
- No card may be inconsistent with its neighbors.

## Problem B: excessive blank space STILL remains
In multiple rows, some short article previews have very large empty white areas before "Read More." The prior attempted fix reported success but visibly left the problem. **Do not report this fixed merely because the CSS changed. Verify the rendered appearance.**

1. Inspect the *winning computed styles* and all competing stylesheets/selectors, not only the newest CSS file. Identify any fixed height, oversized `min-height`, `grid-auto-rows: 1fr`, `height: 100%`, `flex-grow`, spacer, or other rule forcing rows/cards unnecessarily tall.
2. Make each card's height as content-driven and compact as possible. Remove artificial height requirements creating empty space.
3. **Cards in the same row must still be equal height, with their Read More links aligned along the bottom.** Different rows may have different heights based on their own content. Do not force every row on the page to match the tallest row elsewhere.
4. Standardize the *visual amount* of article-preview copy so a very long excerpt is not making two neighboring cards unnecessarily tall. Prefer a carefully chosen, consistent readable preview length (for example 4–5 displayed lines), using line clamping on the previews only where required; do not truncate headlines and do not change or delete full article content. Keep the original excerpt text in the HTML if clamped, and don't repeat it.
5. If visual clamping is inappropriate for a particular card group, use a cleaner content-led layout with modest row-level height differences rather than large blank spaces. Do not invent fluff or add fabricated information just to fill space.
6. Keep the card's "Read More" link clearly visible and clickable; make sure it isn't floating many inches beneath the text.
7. Keep approved photographs, consistent image dimensions, category labels, complete article titles, existing URLs, content, and Read More destinations unchanged.
8. Keep the grid elegantly balanced at standard desktop widths, narrower laptops, tablets and mobile. On mobile, show readable single-column cards with compact spacing, not artificially tall cards.

## Scope and preservation
- Apply the targeted changes through existing shared styles / the smallest necessary selectors.
- Preserve existing branding, header, footer, navigation, dropdowns, chat behavior, SEO metadata, canonicals, all blog articles and their original text, images, and links.
- Do not add new cards, change card counts, move sections, or redesign the website.
- Do not shorten or rewrite full article pages. Adjust only display treatment of card preview excerpts when truly necessary.
- Do not remove the temporary editorial handoff files or otherwise perform unrelated cleanup as part of this task.

## Mandatory visual verification
1. Preview the actual blog listing and representative Life Changes pages, including a row with mismatched excerpt lengths.
2. At 1440px, 1280px, 1024px, 768px, and 390px, check that each card has a visibly substantial, elegant dark sage-green FRAME (not just a darker thin outline) on all four sides, with an intentional coordinated footer.
3. Confirm cards are visually compact, without *large* unused gaps between excerpts and Read More links; compare after screenshots to the current blank-space examples.
4. Confirm equal card heights and aligned Read More links **within each row**, while rows can have different heights.
5. Confirm full headlines, images, link destinations, and all article pages are unchanged. No clipping or overflow.
6. Test Read More links and relevant mobile layouts. Fix any regressions introduced by the changes.
7. Provide a short report listing the specific CSS selectors/files changed, the cause of the previous blank-space issue, and which page sizes were actually tested. If anything remains visually problematic, say so rather than claiming success.

**Do not publish, commit, or push. Show the finished blog-card previews for approval, including a screenshot at normal scale demonstrating the distinctive dark sage framing.**
