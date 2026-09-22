# Bundles Handoff

## Topic & Purpose
Leftovers after the Memar `docs/society` transfer closed. The transfer itself has graduated into [`bundles.md`](bundles.md) and [`bundles.changelog.md`](bundles.changelog.md). This file now holds only placement and rewrite questions a later session still needs.

## Status
Paused — transfer session closed 2026-09-21. Resume from Open Questions, not from the transfer narrative.

## Ambiguities Resolved
- Did the twelve Memar theme folders (`governance`, `economy`, `form-and-land`, …) carry a rule that should be rebuilt here? No. They grouped requirement pages in a notebook. The landing table in `bundles.md` is the whole record. Owner asked; the skipped `docs/society/README.md` was corpus operating rules, not a map of those folders.
- Did deleting the two Memar society commits drop mixed edits in other files, in particular `docs/README.md`? No. `d5888fd` modified `docs/README.md` by adding only the three-line `society/` subsection (commit message: "register the society/ folder"). No later Memar commit touched that file. After invert-path, `HEAD:docs/README.md` is blob `e28f1f0`, identical to parent `15a9413`. `e064798` listed only paths under `docs/society/`. No other Memar file outside that tree and that three-line register was in either commit.
- **Wholesale bundle→plugable after the society import.** Fifty-eight imported modules classified against kernel / plugable / bundle. High-confidence wholesale `git mv`: only `law-validity` → `modules-plugable/rights/law-validity` (done). No imported page is a missing kernel type. Settlement fabric (land, buildings, energy, water, food, travel, logistics, Ensan venues, Health watch, Dideban perimeter, security crisis posture) stays in-bundle. Duplicate *types* already exist for some pages and must not be moved as if they were the type: judiciary vs kernel `case`; membership vs kernel identity/group plus plugable society/government IDs; land-housing-tenure vs kernel `ownership`; payment-rails vs plugable economics. *(How: classification pass this session; owner exemplar was duration; do not treat the fifty-eight-row inventory as a document to keep — the filesystem is the list.)*

## Open Questions
- **Split, do not `git mv` the folder** (medium; owner has not confirmed): extract a general membership/attestation capability from `government/modules/membership-and-identity` into plugable, leave Geniuses.Group citizenship/lifestyle gates in government; extract reusable ADR from `justice/modules/judiciary-and-dispute` into plugable, leave this package's venue ladder in justice, do not replace kernel `case`. `decision-and-deliberation-process` stays in government as this package's constitution process, not a reusable org type.
- Which remaining `bundles/` names should retire or merge after the same test that retired `economy/` as a destination? Candidates: `economy/` (retire into government modules that use kernel economics), `society/` (composition index only, if kept at all). Does not block using the imported modules.
- Is `travel/` a lasting bundle, or should person-movement join `logistics/` later?
- Is `security/` a lasting bundle, or does `autonomy-in-crisis` belong under government?
- Is Dideban the right home for `securing-sensitive-spaces`, or does that page need a narrower watch/surveillance module name inside Dideban?
- When each imported requirement-notebook is rewritten as a module Explanation document plus computer code, which rival approaches survive as code and which drop? Until then, the skipped README rules still apply: requirement as a question that favors no answer; rejected approaches stay visible; network pages name no consumer; consumer pages declare needs toward the network; approach headings keep their section-id suffix.

## Assumptions
- New bundle names opened for this landing (`energy`, `water`, `food`, `buildings`, `land`, `travel`, `security`) are honest enough to receive files now and cheap enough to rename later. Stability: Weak.
- Kernel `modules/economics/` already covers economic *types*; nothing in the society economy pages needs to become a new kernel type. Stability: Strong.

## Next Steps
- Retarget intra-corpus links in the imported pages: they still use Memar sibling paths (`../governance/`, `../economy/`, same-folder slugs). This is the first mechanical job of a later session that touches those files.
- Retire `bundles/economy/` once government modules are using kernel economics types and nothing else still points at that folder.
- Keep the one-line bundle documents for `energy`, `water`, `food`, `buildings`, `land`, `travel`, and `security` as composition sentences only; do not treat those names as a finished taxonomy.
- GitHub may still serve old Memar SHAs (`d5888fd`, `e064798`, `50e15b1`) by exact hash until garbage collection; `main` no longer points at them. Open a GitHub support request only if dangling objects must disappear from the API, not as part of editing these modules.
- Placement of duration is `modules-plugable/rights/law-validity`. No further wholesale `git mv` from this import until the owner confirms a split of membership or judiciary.

## Related artifacts
- Governing: [`bundles.md`](bundles.md)
- Record: [`bundles.changelog.md`](bundles.changelog.md)
- Session close slip: `____Chats/2026-09-21-society-transfer.md` (gitignored)
- Local Memar backup (not on GitHub): `C:\Sync\Persons\Geniuses.Group\github.com\memar-backup-before-society-purge.git`
