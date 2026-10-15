# English restoration report

## Inspection and recovery reference

Inspected the dirty working tree and five latest Git commits before editing. Git HEAD predates approved work (including removing chat logos), so a full reset would have lost approved changes. Used the saved pre-multilingual English HTML snapshots and the verified pre-AI conversation script instead.

All 352 page sources matched their saved English versions after excluding the two translation asset includes and the homepage AI script include. No written content, page-specific conversation JSON, images, videos, URLs, metadata, or portfolio content required replacement.

## Partial project changes found and removed

- Translation client, globe, featured languages, language dropdown, notices, attribution interface and runtime translation styling.
- Empty translation/chat configuration gates and homepage AI client/UI strings. The AI hook in the original conversation opener was removed by restoring the verified English script byte for byte.
- Incomplete Google translation backend/cache-builder directories and empty homepage locale directory. No translated packs or working new AI backend existed. No paid services were activated.
- Translation script includes removed from all 352 pages; homepage AI include removed from index.html.
- Project-only .gitignore additions reverted. Recovery copies retained under removed-project-files; these are disconnected audit evidence, not loaded website assets.

Navigation styling mixed into the language stylesheet was preserved in assets/tablet-navigation.css. Current shared navigation JavaScript and core responsive stylesheet were left untouched. Only tablet main-link font-family was overridden to Arial, Helvetica, sans-serif, matching Neighborhoods. Existing sizes, weights, line heights, spacing, colors, placement, active styles and submenu behaviors remain.

## Verification

- 352/352 original chats opened and completed successfully; every existing main-page chat trigger was exercised.
- 90 distinct page-specific configurations; 811 option paths passed, including applicable conditional branches and intentional conversation-ending options.
- 1,161 HubSpot submission requests intercepted locally. Original endpoint, lead fields, page context, conversation answers and confirmation retained. Shared submission failure and retry passed.
- 14 additional tablet/phone flows passed for homepage, Contact, Buyer Consultation, Seller Consultation, Free Home Evaluation, Interior Design and Marriage.
- Existing legacy HubSpot script remains unchanged; no active legacy contact/region/valuation form elements were found in the 352 page sources. Current experiences use the restored guided chat.
- All 352 page sources preserve the saved English content byte for byte except the navigation stylesheet reference. Chat script exactly matches its verified English backup.
- Actual before/after screenshots captured at 768, 820, 834, 1024, 1180, 1440 and 390px. Tablet submenus captured open and closed. Loaded CSS verified; computed navigation geometry and sampled non-font styling match before exactly. Every tablet main category now matches the Neighborhoods font family.
- No language controls rendered at tested desktop, tablet or phone widths. No active translation/AI references remain in the 352 pages.

## Remaining limitation

Real HubSpot delivery and account-side acceptance were intentionally not tested: all requests were intercepted to avoid creating leads. The original integration remains intact and passed local request/response checks. Nothing requires Google Cloud or new AI configuration for the restored English chats.

No commit, push, publish, deployment, real lead submission or paid-service activation performed.

[Open before/after screenshot gallery](review.html)
