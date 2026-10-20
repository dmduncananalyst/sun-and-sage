# DommyDom multilingual implementation status

## Current local review instruction

The user subsequently authorized generating every language without stopping at
the earlier $20 threshold and instructed that all further work remain local.
No additional budget confirmation is required for this initial generation.
No commit, push, publish or deployment is authorized before the user's review.
The previously created local commits remain unchanged.

Google Cloud sign-in is now complete. The existing project is active, billing
is enabled, all nine requested Translation languages are confirmed by the API,
and the required service APIs have been enabled in that same project. The
existing daily translation quota was read and left unchanged. Credentials are
in the ignored local tools profile and are not included in the site output.

`local_generate.py` now performs the explicitly authorized initial generation
using batched Translation requests, a durable local SQLite deduplication cache,
and permanent `translations.json` output. It makes no Firestore, publishing or
deployment calls. Its initial-generation override is separate from future
automated-workflow limits. `local-generation-report.json` records actual results.
The release workflow is disabled unless `DOMMYDOM_RELEASE_APPROVED` is true.

The repository now contains a static translation builder, incremental translation
worker, GitHub Pages publishing workflow, and an authenticated communications
service architecture. Translation is connected and used for saved local output;
messaging and voice have not been deployed or tested end to end.

## Confirmed environment

The website is static HTML at `dommydom.com`, with GitHub origin
`dmduncananalyst/sun-and-sage`. Existing contact submissions go directly to HubSpot.
Telephone and email links remain intact. There was no chat, user identity system,
voice storage, or calling backend to extend. The `.openai/hosting.json` identifier
is a Sites identifier, not a Google Cloud project. The existing Google Cloud project
`project-2e0d7d9d-d482-4fcf-b6d` is configured and authenticated. Actual NMT requests
have generated the nine saved language sets; see `local-generation-report.json`.

## Saved website translations

`site.py` inventories canonical sitemap pages and English content directories,
extracts text and accessibility/SEO attributes, and preserves scripts and styles.
`local_generate.py` requests only missing content hashes. Successful output is saved
immediately in the local SQLite cache and `translations.json`. The future deployed
`translate.py` adapter uses a Firestore cache. Identical text
across pages shares a translation. Updated text gets a new hash; unchanged text
incurs no translation request.

The builder emits English plus `es`, `fa`, `hy`, `zh-CN`, `ko`, `tl`, `te`, `ru`,
and `ar` directories. It rewrites internal links, language/direction attributes,
canonicals and hreflang, emits ten sitemaps plus a sitemap index, and bundles
static catalogs for dynamically inserted interface labels. The language selector
uses those static files and remembers the visitor's choice. No browser translation
service or Google API credential is included.

Generated pages live in `dist`; permanent translation data remains tracked in
`multilingual/translations.json`. Publication refuses missing translations.
English originals remain unchanged. The workflow detects new/changed source on
main, persists partial progress, then builds and deploys only a complete site.
GitHub Pages must use Actions publishing for that artifact to become the public
site. This repository setting has not yet been verified or changed.

## Cost enforcement

The future automated translation workflow reserves estimated gross NMT cost in a
Firestore transaction, shared between builds and communications. No free credits
are assumed. A verified current-month baseline of existing project translation
spend is mandatory in `dommydom_budget_baselines/YYYY-MM`, with `verified: true`
and `translation_microusd`. This is deliberately not auto-created as zero.
The baseline must be reconciled with existing usage each month before processing.
Other applications sharing the project must participate in this ledger to share
its cap; it cannot independently stop unrelated Google Cloud workloads.

At $15 the service persists a warning and emits a workflow/log warning. At $20 it
blocks further translation requests. The existing Google daily quota is never
modified. An uncertain request keeps its reservation and cannot be retried
automatically, even after a month boundary. An operator must reconcile uncertain
requests against provider logs before releasing them. Voice processing has a
separate default-disabled budget and requires verified rates. Firestore/storage/
hosting costs are separate from translation charges.

The initial local generation was explicitly authorized to proceed without the
earlier monthly threshold stopping it. Its batch ledger is local and its source
character totals are recorded in `local-generation-report.json`. That override
does not automatically authorize a future unattended release or change existing
Google Cloud daily quotas.

## Private messaging and voice architecture

`communications.py` is a separate FastAPI application, packaged by `Dockerfile`.
It verifies Identity Platform/Firebase ID tokens and verified email, checks room
membership on all private operations, and reserves costs before Google calls.
Only the business operator creates conversations. Messages retain originals,
timestamps and translations. Failed translations do not discard messages.
Private caches are room-scoped. Browser clients cannot read Firestore directly.
`firestore.rules` is a deny-all template for these backend-owned collections;
it is not applied automatically to an existing project's other applications.

Voice messages accept bounded 16kHz mono PCM, derive duration from actual bytes,
deduplicate recognition and synthesis, store original recordings in a private
Cloud Storage bucket, and retrieve recordings through membership-checked routes.
No private conversation data is copied into public builds or sitemaps.

The call WebSocket uses actual Speech v2 streaming recognition, translates final
utterances, relays text through the shared private conversation store, and emits
synthesized audio to the other participant. Microphone access is explicit and
bounded queues prevent unbounded buffering. Each stream reserves at most 60
seconds and ends with a reconnect event; the UI offers restarting the next
segment. This is a translated conversation application architecture, not a PSTN
phone provider. Existing telephone links remain available independently.

`multilingual-communications.js` supplies the authenticated contact-panel adapter,
message history, original/translated text, recording, playback, language choices,
and call controls. Its `mount` method attaches to the existing contact form's
container. It requires a deployed API URL, authenticated token callback and
authorized room; it is not activated with a fabricated identity or endpoint.
Existing HubSpot submissions are preserved and are not silently copied into a
new communications service.

## Language and capability verification

Translation language codes are distinct from speech locale codes: Tagalog uses
`tl` for NMT and `fil-PH` for speech; Chinese uses `zh-CN` for NMT and
`cmn-Hans-CN` for recognition. Voice and STT support vary by model and region.
STT remains disabled until `STT_VERIFIED_LANGUAGE_CONFIG` supplies a verified
locale/model/region per language. The runtime queries available Cloud TTS voices
and selects only actual Standard voices; it does not invent Persian or Armenian
voice names. Unsupported synthesis returns a browser-voice fallback, with
translated captions when the device has no matching voice. Full spoken support
for every language therefore remains unverified, not advertised as complete.

Authoritative references reviewed:

- https://cloud.google.com/products/translate/pricing
- https://docs.cloud.google.com/translate/docs/authentication
- https://docs.cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
- https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types

## Exact external access still required

Local Google Cloud authentication and Translation access are verified. The future
private messaging cache and automated cost ledger require a Firestore database
plus Datastore User access. API enablement, billing and existing daily quota were
verified; `cloud-status.json` records the read results. No project, billing account,
database or bucket was created. No release is authorized pending local review.

GitHub automation requires a Workload Identity provider bound to this repository,
a service account authorized for translation and Firestore, and GitHub variables
`GOOGLE_CLOUD_PROJECT`, `GOOGLE_WORKLOAD_IDENTITY_PROVIDER`,
`GOOGLE_SERVICE_ACCOUNT`, plus explicitly enabled paid processing after baseline
verification. Service-account key files are neither needed nor committed.

Communications additionally requires a deployed private-data backend with public
HTTPS ingress and verified application authentication, Identity Platform/Firebase
configuration, an operator user ID, a private audio bucket, Speech and TTS API
access, and verified speech prices/capabilities. Runtime service identity needs
Speech Client and Text-to-Speech synthesis access, Firestore access, and object
access scoped to that private bucket. No live end-to-end call, real translation,
voice synthesis or transcription can be verified without these connections.

## Tests and limits

The automated tests exercise ten locale routes/SEO, RTL, markup preservation,
new-blog detection, changed-content caching, incomplete-publication blocking,
transactional reservation behavior, uncertain-request blocking, warnings, original
message preservation, membership enforcement and Speech SDK configuration.
Provider calls are mocked in these tests. Passing them does not establish cloud
connectivity or actual translation quality. Actual multilingual browser layouts,
mobile microphone permissions, real speech support and end-to-end calls still
require authenticated services and deployed browser testing.
