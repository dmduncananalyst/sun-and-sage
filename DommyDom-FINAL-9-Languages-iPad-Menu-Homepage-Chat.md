# DOMMYDOM — COMPLETE, CORRECTED CODEX IMPLEMENTATION BRIEF
## TWO jobs: a genuinely refined iPad/tablet menu + Google-powered homepage translations in EXACTLY NINE languages with a matching multilingual consultation chat

**Repository:** `sun-and-sage` (DommyDom) ONLY.  
**This file replaces conflicting earlier Codex briefs concerning iPad navigation or multilingual translation. Read it all before editing.**  
**No publishing, pushing, committing, deploying, paid activations, or real billable API calls without explicit approval.** The owner and ChatGPT will handle Google Cloud account setup separately; Codex should handle the website code and technical integration only.

---

# JOB 1 — ACTUALLY REDESIGN THE iPAD/TABLET NAVIGATION

## What is wrong now

The existing left-side iPad/tablet navigation has repeatedly received superficial updates without achieving a professional luxury look. Some main entries, especially items such as Buy, Sell, and Interior Design, have inconsistent text sizes, weights, padded blocks, and backgrounds compared with Home, About, Life Changes, or other categories. It looks like mismatched components, takes attention away from Dominique's photographs and video, and is not the approved quality level.

**Do a visibly meaningful redesign, not another color swap or tiny CSS tweak.** Codex has creative responsibility for the final visual design while respecting the following precise functional rules.

## Required behavior and visual design

1. **One cohesive menu system:** Every TOP-LEVEL navigation item uses consistent font size, font weight, line height, left alignment, vertical padding, spacing, clickable/tappable area, and selected/hover styling. No oversized categories beside tiny ones. Use a single reusable component/style pattern across all pages.
2. Submenu links may have a different, slightly smaller style, but **all submenus must follow that same subordinate style**. Keep submenu indentation, typography, dividers, and spacing consistent.
3. Preserve **every approved existing menu label, destination, and link**. Inspect the actual current project rather than guessing labels or inventing routes. Preserve the existing approved structure for Home, About, Buy, Sell, Property Management, Interior Design, Life Changes, Considerations, Blog, Contact, Neighborhoods, Search, and any genuine existing destinations. Do not restore obsolete dropdowns that the project has already removed.
4. On iPads/tablets, keep the **visible, touch-friendly navigation** and use the existing left-side presentation as the starting point, but transform its visual quality. Do NOT use a hamburger, horizontal sliding menu, hidden horizontal overflow, tiny fonts, a generic "More" option, or two stacked rows of horizontal navigation links.
5. Allow long labels such as **Property Management** and **Interior Design** to fit intentionally and legibly; do not make an entire word or category microscopic. Do not let the sidebar consume an excessive portion of the main content or homepage media.
6. On touch devices, tapping a top-level category with children reveals its submenu **directly beneath that category**, not as an overlapping detached panel. Main category labels remain visible. Tapping again may close its submenu. Direct links navigate as expected. No separate Back button is required just to return to the top-level menu.
7. On conventional desktop, **keep the approved full horizontal navigation**, with its existing dropdowns appearing automatically **on hover, not click**. Align every desktop dropdown **centered directly below its own parent label**, without an unusable gap between the pointer and the panel. Do not display arrows, chevrons, or plus signs in the visible desktop nav.
8. On phones, **preserve the working hamburger menu** and its tap-operated submenus. Do not expose every single article link at once or force hundreds of links into a flat mobile menu.
9. Keep **Neighborhoods and Search** visible and functional in their existing approved header positions, including their desktop-hover and touch-tap behavior. Do not rearrange logos, contact numbers, email, or the overall header as part of this sidebar redesign.
10. Use DommyDom's established high-end ivory, white, dark-sage palette and existing typography; present appropriate breathing room, refined hierarchy and elegant active states. Avoid a generic dashboard or file-directory appearance, thick clashing boxes, repetitive heavy rules, and oversized dead space.
11. Verify keyboard access, logical tab order, visible focus states, touchscreen targets, `aria-expanded` controls, and no inaccessible or clipped links.
12. **Look for conflicting stylesheets/media queries, duplicate menu markup, specificity collisions and cache issues.** Ensure the correct files are loaded across the whole website, not only one preview page.

## Required visual proof

Capture and inspect actual **BEFORE and AFTER screenshots at 768, 820, 834, 1024 and 1180 pixels**, with the menu both collapsed and at least one submenu expanded. Also verify **1440 desktop** and **390/430 phone**. The redesign must look meaningfully different and better; if before/after images look nearly identical, the job is not complete. If an iPad viewport makes requirements mutually impossible, **show genuinely designed options and their tradeoffs instead of silently adding a forbidden pattern**.

---

# JOB 2 — HOMEPAGE-ONLY MULTILINGUAL SUPPORT

## Exact scope: JUST the homepage; NOT the entire site

- The **existing English DommyDom homepage** is the sole page to receive Google-generated localized versions.
- **Every inner page, article, buying/selling guide, city/neighborhood page, Considerations page, Interior Design page, and other site page remains in English** for now. Do NOT translate 350+ pages or generate additional translated articles.
- The **Contact Dominique conversational chat that visitors can open from the translated homepage** should communicate in that visitor's language. This is separate from translating the entire website.
- Keep the same English homepage content, existing images, videos, wheel, maps, graphs, cards, buttons, animations and structure. Translate user-visible text only, while allowing longer translated text to fit naturally.

## EXACTLY NINE languages — final approved list

**English** is the original/default and a return-to-English choice; it is not counted as a translation. Implement precisely these **nine target languages** and **no others**:

| Number | Approved language name | Label in native writing / useful display | Google locale to confirm |
|---|---|---|---|
| 1 | **Spanish** | Español | `es` |
| 2 | **Farsi** | فارسی | `fa` |
| 3 | **Armenian** | Հայերեն | `hy` |
| 4 | **Mandarin** | 中文 (Mandarin) | `zh-CN` / Google's current written Simplified Chinese code |
| 5 | **Korean** | 한국어 | `ko` |
| 6 | **Tagalog** | Tagalog | `tl` / supported equivalent |
| 7 | **Telugu** | తెలుగు | `te` |
| 8 | **Russian** | Русский | `ru` |
| 9 | **Arabic** | العربية | `ar` |

**CRITICAL NAMING CHANGES:**

- The customer-facing language name is **"Farsi"**, **NOT** "Persian," **NOT** "Persian / Farsi." Its native-script label `فارسی` is correct.
- The customer-facing language choice is **"Mandarin"** (optionally with `中文`), **NOT** two separate "Simplified Chinese" and "Traditional Chinese" choices. Use the appropriate **written Chinese translation** output for Mandarin (normally Simplified Chinese) under this **one** choice. Do not represent Google as providing an audio Mandarin translation; this is a written website.
- There are exactly **NINE translated homepages**, with **English + nine language choices = TEN language options in the selector**. Do not write "approximately ten" or invent a tenth translated language.
- Verify precise language-code support with the official Google Cloud Translation API before connecting. Do not silently substitute a language or dialect.

## Language-selector layout and actions

1. Keep the previously approved compact selector within the existing header beside **Neighborhoods** and **Search**, without introducing another header row or crowding Dominique's signature logo, RISE branding, or contact information.
2. In the header, visibly feature a tasteful globe icon and the three recognizable language names **`Español · فارسی · 中文`**, with no arrows/chevrons/plus signs. These are teaser labels only; the dropdown contains all nine supported translations plus English.
3. **Desktop:** moving the mouse over the language control **automatically opens** the dropdown (no click to expand). Hovering over a language may show a simple invitation in **that same language only**, without English copied below. **One click** on a language immediately chooses it.
4. **iPad/phone:** tapping the control opens the dropdown; tapping a language selects it. Do not require an additional confirmation screen.
5. The dropdown itself must be **compact**, use one consistent **left-aligned column** of language entries, and display only **English + the nine choices**. Respect the proper right-to-left writing of Arabic and Farsi **inside** their rows while keeping overall rows aligned on the same left edge.
6. **Absolutely no redirect to `translate.google.com`**, no Google Translate text-entry page/box, no old discontinued widget, no browser-extension instructions and no giant "Google Translation information" panel. Honor any Google attribution or legal notice requirements unobtrusively elsewhere as appropriate.
7. Selecting a language while on the homepage translates **that homepage in place** while remaining under `dommydom.com`. English remains one selection away. Keep the selected language while the user interacts with the homepage/chat.
8. If a visitor navigates to an **English-only interior page**, the site must **not misrepresent it as translated**. The links work normally. A language selection from an inner page may return to the corresponding translated homepage if that behavior is labeled clearly; do not change existing content URLs behind the visitor's back.
9. Optionally, once translation truly works, politely offer the matching translated homepage if the visitor's browser requests one of the nine languages. This offer must be small, dismissible, and in the visitor's own language; do not open intrusive popups or imply the rest of the site is localized.

## Google translation engine; cache each homepage

- Use **Google's official Cloud Translation technology** for the real homepage translations. **Codex must NOT author or invent the actual nine translations.** The owner and ChatGPT will complete the administrative Google setup outside Codex.
- Use a secure integration appropriate to the current site's actual hosting/Cloudflare setup (e.g., authenticated backend/serverless Worker), with **no Google credentials, service-account files or API keys in public HTML, frontend JS, URLs, or public GitHub**.
- Obtain the English homepage text; produce/store the nine localized strings **once** in local cache/data files (or equivalent durable storage) following authorized Google translation requests. Reuse them for each visitor so each page view does NOT generate new Google charges. Only retranslate affected strings if the source changes and only after authorization.
- **Count the actual translatable characters on the homepage** and estimate Google usage for nine language versions. Google's advertised monthly free credit (commonly described as the first 500,000 characters of standard translation each month) is **not a hard spending cap**. Do not assume that billing is optional or that charges cannot occur.
- Before Google access is available, Codex can implement/test the website interface with clearly labeled nonproduction fixtures, but **must report that actual translations are NOT connected**. Never leave a live-looking selector that secretly opens Google Translate's external text box or claims success with fake translated content.
- English remains the canonical SEO source. Do not promise international SEO or create/crawl translated subpages until they actually exist and are approved.

## EXACT notice on every translated homepage

Add one **small, elegant, unobtrusive sentence block** on the translated homepage only. Translate this **exact English source meaning** into the chosen language using the approved translation flow. Replace `[language]` with the local name of that language and **show only the translated text**, not an English version underneath:

> **Only this homepage is available in [language]. Other pages are currently in English. You can chat with Dominique's assistant in [language] to ask questions or request a consultation.**

Do not add apologies, large banners, generic "Next Steps" copy, or an implication that the entire site is translated. The invitation to chat must be shown as functional **only after the matching chat has actually been connected/tested**. Before then, don't promise a working feature.

## Preserve the approved design while accommodating different text lengths

- The exact existing page compositions, photographs, beautiful card styles, wheel, maps, graphs, video, navigation hierarchy, typography families, and branding remain unchanged.
- Translate visible homepage headings, paragraphs, menus displayed on that page, card titles and descriptions, buttons, tooltips and footers where appropriate. Don't translate proper names, actual phone numbers, email addresses, raw URLs or visitor-submitted text.
- Different languages need different space: **wrap text naturally; allow card heights/sections to grow where necessary; never truncate words, hide copy, shorten meaningful content, shrink fonts to unreadability, or crop text**. Keep existing luxury card styling and coherent row balance.
- Properly implement `lang` and `dir` semantics, especially right-to-left **Farsi** and **Arabic**, and check their text alignment, menus, buttons, punctuation and cards. Preserve normal English and left-to-right behavior in the rest of the site.

---

# MULTILINGUAL "CONTACT DOMINIQUE" — REAL CONVERSATIONAL AI CHAT

A visitor on a translated homepage must be able to contact Dominique **without first having to communicate in English**.

1. **Match the chosen homepage language automatically.** Spanish homepage → Spanish chat; Farsi → Farsi chat; Armenian → Armenian chat; **Mandarin** → natural written Mandarin Chinese chat; Korean, Tagalog, Telugu, Russian and Arabic similarly. English homepage → English chat.
2. The **entire chat experience** is in that language: launcher text, welcome message, questions, labels, suggested prompts, send/close controls, validation and **actual AI replies**. Do **not** merely translate the button label while leaving the conversation in English.
3. This is a real **back-and-forth AI conversation**, not a static translation box, a long form disguised as a chat, a rigid accordion, or a fake pre-scripted success demonstration.
4. The assistant can discuss approved general website information, real estate services, and consultation requests. It should gather the visitor's name, contact details, topic of interest, preferred language and inquiry **in conversation**, and route the inquiry to the existing verified lead/notification path. Do not fake email delivery or promise appointments are booked without a real scheduling connection.
5. Save the **original-language inquiry** and, if supported and tested, include a clearly labeled **English summary for Dominique**. Avoid replacing the original messages. Don't imply Dominique personally speaks these languages or guarantee a human interpreter.
6. Preserve the existing site-specific Contact Dominique chat experience and any existing page-context behavior; integrate language preference into it instead of replacing it with a new generic chatbot. Inspect what actually exists first.
7. Use an existing appropriate chat AI provider if already configured, or describe exactly what is missing. Having a ChatGPT subscription **does NOT** make visitor-facing API chat free. **Google homepage translation and real AI-chat costs are separate.** Do not activate billable chat models, paid provider accounts, or make actual billable requests without approval.
8. Prefer the chat model to answer directly in the selected language so normal chat does not consume Google translation characters. Keep original user text untouched. Handle Farsi and Arabic in right-to-left chat bubbles correctly.
9. Function correctly on desktop, tablet and phones without covering essential contact links or breaking page layouts. Ensure fallback/helpful behavior when a provider is unavailable and clearly show which features are not yet operational.

---

# OWNER DOES THE GOOGLE SETUP SEPARATELY — CODEX DOES THE WEBSITE CODE

- **Do not send the owner through Google Cloud account-creation, pricing, card entry, billing activation or Cloudflare login instructions inside Codex.** The owner and ChatGPT will handle those administration steps together separately.
- First, inspect the existing site files and architecture to prepare the smallest secure implementation that fits the website's real hosting. Implement code and safe local mocks where useful, but **stop before any paid activation/deployment**.
- Do not enable Google billing, make live Cloud Translation requests, deploy Workers/services, activate chat API usage, commit or publish. Do not place secrets in source files. List only the integration data/services needed from the owner at handoff, with **no requirement to disclose secret keys in chat or a public repository**.
- Report separately whether each feature is **(a) implemented and visually testable, (b) implemented but awaiting third-party setup, or (c) not implemented**. Avoid saying translation is "working" based solely on dropdown interaction.

---

# PRESERVATION — DO NOT CHANGE ANYTHING UNRELATED

- Work in **`sun-and-sage` ONLY**. Do not touch StartWeb7, Paradigm Janitorial or Paradigm Security.
- Preserve ALL English page contents and site URLs: homepage, article pages, Neighborhoods, Buy/Sell, Considerations, Life Changes, Contact, Interior Design, Portfolio, Search, SEO/AEO metadata and internal links.
- Preserve all approved photographs, card images, borders, spacing, video/animations, interactive wheel, maps, graphs, portfolio projects, testimonials and functionality.
- Do not rewrite or shorten English text, invent new categories, change consultation routes, create unnecessary pages or rearrange the header beyond the specified tablet refinement and small language selector.
- Do not add arrows, plus signs, fake menus, extra booking steps or marketing language.

# ACCEPTANCE CHECKLIST AND REQUIRED EVIDENCE

- [ ] **Tablet menu:** real BEFORE and AFTER images at 768/820/834/1024/1180, with open and closed submenus; clear substantial visual improvement and consistent top-level type/spacing.
- [ ] **Regression checks:** 1440 desktop and 390/430 phone; correct hover vs tap interactions; no scroll rail, off-screen links, overflowing panels or broken navigation.
- [ ] **Exact language list:** English + **nine** (Spanish, Farsi, Armenian, Mandarin, Korean, Tagalog, Telugu, Russian, Arabic), with no extra Chinese option or "Persian / Farsi" label.
- [ ] **Language UI:** three header teasers, compact left-aligned dropdown, no redirection to Google Translate, no extra language-information panel.
- [ ] **Homepage only:** translated text display ready; every inner page remains English; notice displayed only for translated homepages; card content wraps and does not truncate.
- [ ] **Chat:** corresponding language in buttons/prompt/responses once actual provider is connected; no fake chat, fabricated lead submission or claim of live AI without verified provider.
- [ ] **Security/cost:** no public secrets, no unexpected billable activity, no deployment; Google Cloud and/or chat provider blockers clearly documented.
- [ ] **Preservation:** verify no collateral changes to English pages, URLs, photos, design or SEO.
- [ ] Provide screenshots, a concise list of modified files, and three independent statuses: **iPad menu**, **homepage translations**, and **multilingual AI chat**.
- [ ] **Do not commit, push, publish or activate paid services without explicit approval.**

**This is the final authoritative nine-language brief. Implement these decisions, not earlier conflicting ten-language or site-wide-translation instructions.**
