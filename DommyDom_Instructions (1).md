# DommyDom — Master Codex Instructions: Luxury Tablet Navigation + Google Translation

**Project:** `sun-and-sage` (DommyDom / Dominique Duncan-Nelson)  
**Status:** Local implementation and visual review only. **Do not commit, push, deploy, publish, or activate paid Google Cloud services without approval.**  
**Purpose:** Bring the existing tablet navigation up to a genuinely polished luxury standard and implement multilingual access through Google's official translation technology **without redesigning or rewriting the existing website.**

## READ THIS FIRST — NON-NEGOTIABLE PRESERVATION

1. Work only inside the existing `sun-and-sage` repository. Inspect its actual HTML, shared header/navigation CSS and JS, hosting/deployment configuration, and existing card systems before editing.
2. **Keep the existing website and approved work the same.** Preserve every existing page, URL, photo, video, logo, footer, original English copy, card title, article, SEO/AEO work, schema, menu destination, and working interaction. Do not creatively rewrite, shorten, rename, or replace content. Do not create mock/example pages or placeholder translation UI and report it as completed work.
3. Scope the changes to (A) **meaningful visual refinement of the existing tablet sidebar** and (B) **the multilingual feature**. Do not redesign desktop navigation, the About biography, the homepage video, Buy With Dominique's wheel/maps/graphs, Life Changes, Considerations, Contact, Interior Design, or other page compositions.
4. Use the current implementation as the baseline. Preserve the agreed navigation: main categories Home, About, Buy, Sell, Property Management, Interior Design, Life Changes, Considerations, Blog, Contact; separate Neighborhoods and Search controls. Keep the existing intended behavior of direct links, hover menus, and touch interactions. Do not resurrect earlier abandoned menus, question-based section titles, or deleted categories.
5. The design must remain DommyDom's refined **ivory / muted dark sage / sophisticated editorial typography**. Do not add generic web-app/dashboard widgets, bright colors, unapproved icons, solid rectangular selected-item buttons, or generic card templates.

## A. TABLET / IPAD NAVIGATION — REAL VISUAL IMPROVEMENT

### What is wrong now

The current screenshot shows a solid sage-green sidebar to the left of the About page. It is usable but too much like a software dashboard. Selected-item rectangles, mechanical separators, heavier than necessary background blocks, and compressed sublinks compete with Dominique's portrait and the page content. Codex previously reported styling changes that were barely noticeable. **This new pass must produce an obvious, visible refinement, not only tiny CSS adjustments.**

### Requirements

1. **Retain the approved tablet navigation concept:** main categories always visible in an integrated left-side navigation; no tablet hamburger, no horizontal sliding navigation, no "More" menu, and no two stacked horizontal rows. On phones, keep the current functional mobile menu. On true desktop, keep the approved horizontal desktop menu.
2. **Codex owns the aesthetic design solution.** Make the tablet sidebar genuinely premium, coherent with the page, and editorial rather than a dashboard. Refine its width, visual weight, typography, active-page indication, contrast, section rhythm, padding, dividers, and background treatment. Do not cover or compress the content excessively. Keep text readable and touch targets comfortably sized (aim for about 44 × 44 CSS pixels where appropriate).
3. The navigation should feel like a *part of the page*, not an unrelated overlay or permanent large solid block. Use considered visual hierarchy and breathing room **without making the overall header/sidebar giant**.
4. Submenus expand **directly below their parent category** and align with it. They should be compact but readable, use polished transitions if any, and remain easy to use without bouncing the content, clipping, unexpected horizontal overflow, or awkward dead space. The current active page and current expanded submenu should be legible but not decorated like a generic app button.
5. Every main link stays visible and every existing nested destination remains reachable. Do not eliminate labels, quietly remove links, shrink text to microscopic sizes, or hide navigation beyond the visible width.
6. On touch devices: tapping a category with a submenu exposes it, and tapping a destination follows the link; ensure the category's own landing page remains reachable if it is also a legitimate destination. Other main categories stay visible when one submenu is open. No extra Back button is required for the sidebar. Use keyboard focus, Escape/dismissal where relevant, semantic navigation, and appropriate expanded state attributes.
7. On desktop: existing menu dropdowns open on **hover** and are centered immediately under their respective labels (not drifting left or right). No decorative arrows, plus signs, or chevrons. Neighborhoods and Search keep their approved dropdown behavior.
8. Keep current header/logo/contact group placements unless a minimal responsive adjustment is essential; Neighborhoods and Search stay before the phone/email group as approved. Do not change their names or destinations. Keep the portrait and About text intact.
9. Use the existing shared navigation architecture so the change is consistent across all 351+ pages, rather than independently rewriting unrelated page structures or duplicating conflicting stylesheet rules.

### Tablet acceptance criteria

- Visual **before/after** screenshots at 768, 820, 834, 1024, and 1180 px, showing a closed and an expanded sidebar (particularly Buy and Interior Design).
- Visual checks at representative desktop widths 1280 and 1440, and phone widths 390 and 430 px to prove that their current navigation still works.
- No horizontal page scrolling, no clipped Contact link, no detached dropdowns, no unreadable text, no excessive blank space, no collision with About content, and no noticeable layout regressions.
- If the resulting sidebar looks effectively identical to the initial screenshot, it is **not** done; refine again before claiming completion.

## B. MULTILINGUAL ACCESS USING GOOGLE'S OFFICIAL CLOUD TRANSLATION

### Intended visitor experience

1. **Keep visitors on DommyDom's website.** Do not send them to translate.google.com, change them to a Google Translate proxy page, require browser installations, or rely on the discontinued public Google website widget.
2. Add a tasteful, discoverable language control to the **existing** header, alongside Neighborhoods and Search, integrated with the approved responsive layout (no extra header row, crowded labels, or awkward wrapping).
3. The small visible control should include a **globe** plus these three native-language labels: **Español · فارسی · 中文**. Make sure it remains legible and does not crowd the header. **No arrows, chevrons, or plus signs.** If tablet space is constrained, solve it thoughtfully without undoing the tablet navigation requirements.
4. On pointer devices, **hovering over the language control opens** a tasteful language dropdown. The dropdown stays open while the mouse moves into it; no initial click is required. On iPads and phones, it opens by **tap**.
5. List languages in **their own writing systems**, including: English; Español (Spanish); فارسی (Persian/Farsi); 简体中文 (Simplified Chinese/Mandarin); 繁體中文 (Traditional Chinese); Հայերեն (Armenian); 한국어 (Korean); Tagalog (Filipino); తెలుగు (Telugu); Русский (Russian); العربية (Arabic). Additional languages are fine when correctly supported, but do not include broken/unimplemented selections.
6. Hovering/focusing an individual language may reveal a short invitation **only in that language** (not duplicated in English), consistent with the user's request. **Selecting the language must apply it immediately** without a second confirmation screen. On touch devices, the selection must remain simple and obvious.
7. If the visitor's preferred browser language is one of the supported languages and different from English, show an optional, nonintrusive invitation **in that language only**. It must be dismissible and must never automatically force a translation. Remember the visitor's dismissal/choice where possible.
8. When a visitor switches to a language from any page, remain on **that same page**, with navigation, headings, article content, captions, card titles/descriptions, buttons, menus, forms' static labels, and accessible text translated. Retain their choice while browsing other pages, with an obvious way to switch back to English.
9. Preserve names and protected strings that should not be translated: **Dominique Duncan-Nelson, DommyDom, RISE × REAL, branded logos, website/domain URLs, phone numbers, email addresses, proper project titles where appropriate, and visitor-entered input.** Do not send private form submissions or personal client information through translation just to localize the interface.
10. **English remains authoritative.** Translation is a display/accessibility layer; do not replace the English HTML content, articles, titles, canonical URLs, or SEO text. Do not falsely claim translated pages are independently SEO-indexed if the solution translates at runtime only.

### CRITICAL: Translating text must NOT damage card or page layouts

This is an explicit owner requirement:

- **Keep every existing card the same design and preserve its complete content.** In a translation that needs more words or longer words, **fit as much translated language as the card needs to display the FULL original meaning**. Let the text wrap naturally, and let the card grow in height as needed.
- **Never truncate translations**, hide words, use an ellipsis, force a character limit, replace content with shorter marketing copy, or lower fonts until unreadable merely to squeeze translated text into an English-sized card.
- Maintain the already approved image proportion, borders, visual hierarchy, typography, button appearance, spacing, and responsive breakpoints. Use flexible CSS heights/grid alignment thoughtfully to keep card rows attractive without turning them into huge blocks of blank space.
- The same principle applies to dropdowns, navigation labels, headings, captions, article cards, forms and buttons. Allow appropriate line wrapping and sufficient breathing room.
- For **Arabic and Farsi**, apply correct right-to-left reading behavior where required. Preserve left-to-right direction for phone numbers, email addresses, web addresses and other LTR technical strings. Avoid mirrored photographs, logos, charts or other visual assets.
- Ensure translations are readable and responsive at all requested sizes. Test at least one long-text language (e.g. Armenian/Russian) and RTL Farsi/Arabic, plus Spanish and Chinese.

### Secure implementation and hosting reality

1. Inspect whether the live site is served via GitHub Pages / another **static** host. The current VS Code previews use `file://` paths, which cannot by themselves prove a hosted translation integration works.
2. Use **Google Cloud Translation** as the translation provider. A static HTML site cannot securely call a paid Google Cloud API with embedded browser-visible secrets. Implement a suitable **serverless endpoint/backend** or other secure architecture and explain any needed external hosting/configuration.
3. **Never commit credentials or API keys to GitHub, HTML, JavaScript, CSS, or a public directory.** Use cloud secret management/environment configuration. Add appropriate rate limiting, caching, request validation, errors/fallback, cost controls, and API usage/billing safeguards. Never misrepresent an unauthenticated stub as a working translator.
4. Cache translations appropriately, keyed by original content/version and target language. Refresh when English text changes. Avoid resubmitting all pages on every visitor interaction when unnecessary.
5. Keep English pages fully usable if translation API, network, or backend is unavailable. Report errors gracefully without showing raw machine output or breaking the page.
6. **Google Cloud setup and billing require the owner's action/approval.** Build the parts that can be completed locally, then provide exact one-step-at-a-time setup guidance for any cloud account, billing, credentials, and deployment required. **Do not activate billing, publish a live endpoint, or initiate paid service usage on behalf of the owner without approval.**
7. The site must support selected-language navigation between pages; test links and page state, including from category pages to articles and from Contact to consultations. Do not change existing URL destinations.
8. Do not modify SEO canonicals, sitemap entries, robots instructions, or `hreflang` tags to claim unbuilt translated URLs. If translated indexable pages are added later, that is a separate approved project.
9. Follow Google's applicable API and branding/attribution requirements. Do not imply that Dominique speaks every language or promises multilingual consultations.

## C. PRESERVE OTHER APPROVED SITE WORK

- Preserve the homepage's door-opening video and its existing smooth playback; do not freeze frames or alter the design.
- Preserve all existing card layouts and approved photo assets on Life Changes, Considerations, Blog, Contact, Interior Design, cities, and individual articles.
- Preserve any existing Contact dropdown (Contact + Reviews), Interior Design dropdown (Interior Design + Portfolio), direct landing page links for Life Changes and Considerations, and the established Buy/Sell navigation content. Do not expand enormous city lists back into Buy; Neighborhoods remains a separate header feature.
- Preserve the latest portfolio and contact card work; do not invent new portfolios or replace existing photos.
- Do not alter wording or render categories as question-based titles. Everything previously approved should stay as is.
- If a prior instruction conflicts with this file, use this file for **tablet visual refinement and Google translation only**, while keeping all previously approved page designs and user content.

## D. DELIVERY AND VERIFICATION — SHOW ACTUAL RESULTS

1. List the exact files you changed, and for what reason. Distinguish changed, newly created, and untouched files.
2. Provide **real before/after screenshots** (or paths to generated local screenshots) of iPad portrait and landscape sidebar closed/open, representative desktop header, and phone navigation.
3. Provide screenshots of **translated pages** in Spanish, Chinese, Farsi/Arabic, and one longer-text language showing complete text inside cards without cropping; show header, card grids, at least one long article, and a consultation page.
4. Confirm that hover/touch, navigation links, English return, RTL, keyboard accessibility, card heights and overflow have been checked. State clearly what was actually tested and what is blocked by missing Google Cloud access.
5. Do not claim "translation works" just because a local simulated response displays. Distinguish code completed from actual live API connection.
6. If any requested behavior is not achievable with the current hosting or design constraints, explain the specific obstacle and propose the smallest viable alternative **before** replacing the approved layout.
7. **Nothing should be committed, pushed, published, or billed without approval.**

## Final success definition

A visibly more luxurious and user-friendly **left-side tablet navigation**, unchanged approved English design and content throughout DommyDom, plus a secure Google-powered language feature that keeps visitors on the current page and shows **all translated text in full**, automatically adapting card heights/line wrapping rather than truncating content. No unrelated redesigns.
