# Local multilingual review

Review the repository's actual `index.html`, including opening it directly from
Explorer. All changes remain local: no commit, push, publication or deployment.

October 20 review update:

- Home, Search, then the globe and native language name appear together in the
  header. There is no visible "Language" label. Explorer and HTTP switching pass.
- Six complete supplied articles and their exact original photos were added,
  with 60 saved article versions across English and the nine translations.
- The 19 broken legacy blog URLs now redirect locally; 38 real browser redirect
  checks preserve query strings/fragments. All 360 locale aliases pass checks.
- Eleven marketing-page alt texts and 32 required-city search forms were fixed.
  Reversed price ranges are rejected and can be corrected without reloading.
- All original photo bytes are preserved. At the user's subsequent request, the
  six new preview photos fill their card frames with centered `object-fit:cover`.
  Full article photos retain their original aspect ratios without cropping.
- All English internal file references resolve. Existing base tags are honored
  and placed before assets so nested pages and translated pages retain styling.
- 80 desktop/mobile browser cases and 60 additional Explorer/layout/photo cases
  pass, with zero paid browsing API calls and zero JavaScript errors.
- 27 Python tests and the JavaScript runtime checks pass. Two HubSpot payloads
  were intercepted and checked locally; no external submission was sent.
- HubSpot's public configuration request returned HTTP 200 but its callback
  reports status 403 with `form:null`. This does not establish submission
  acceptance. An authenticated HubSpot account with access to portal 247079925
  and its forms/contact records is needed to investigate and verify live receipt.

Reports: `october-audit-review.json`, `editorial-review.json`, `alias-review.json`,
`redirect-review.json`, `form-review.json`, and `source-browser-review.json`.
Screenshots: `.translation-state/october-review/` and
`.translation-state/source-browser-review/`.

The selector is now embedded directly in the actual root `index.html` and all
356 English source pages. All nine translated directories (`es/`, `fa/`, `hy/`,
`zh-CN/`, `ko/`, `tl/`, `te/`, `ru/`, `ar/`) and static catalogs are installed
beside those source pages. The normal website preview now includes the complete
language system; it does not require opening a separate generated copy.

All 356 inventoried English pages, including 36 blogs, have saved versions in
Spanish, Farsi, Armenian, Simplified Chinese, Korean, Tagalog, Telugu, Russian,
and Arabic. English remains the default. There are 58,680 permanently saved
translation segments and 3,560 language pages, plus retained redirect aliases.

The website source and `dist/` both contain the complete language system. Saved Google translations are in
`multilingual/translations.json`; the local incremental cache and request ledger
are in the ignored `.translation-state/` directory. Browsing and switching
languages use static files and never generate Translation API requests.

Verification evidence:

- `verification.json`: zero missing segments in every language; all 3,560 saved
  language pages passed rendering/SEO checks.
- `browser-review.json`: 80 real Chrome checks at desktop and mobile widths;
  language URLs, RTL, selector choices, canonical/hreflang, mobile menus and
  translated validation passed; no paid API attempts or JavaScript errors.
- `source-verification.json` and `source-browser-review.json` verify the actual
  website source and root language directories, rather than only the build copy.
- `local-generation-report.json`: actual generation completed with no failures.
- The 27 Python tests and JavaScript runtime checks passed, including checks
  that a page reuses its visible HTML selector and retains its selected language.
- Review screenshots are in `.translation-state/browser-review/`.

The existing Google Cloud project and billing account were reused. Daily quotas
were read and not changed. Credentials remain outside the public output and
outside Git. The user explicitly authorized the initial generation to continue
without the previous monthly threshold stopping it.

All work since the user's local-only instruction remains uncommitted. Nothing
was pushed, published or deployed. The release workflow requires the separate
`DOMMYDOM_RELEASE_APPROVED` flag and is not authorized for release now.

Messaging, recorded voice and streaming-call integration code is present locally.
No new messaging database, audio bucket, identity application or hosted backend
was created under the local-only instruction. End-to-end real messaging and
voice calls therefore remain unverified. Saved page translations are machine
translations; a native-speaker editorial review has not been performed.
