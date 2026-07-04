# RFC Status Legend

> Note to Omid: I could not find a "Status legend" section in the copy of README.md I have access to — the version uploaded to me only contains Goals, Not Goals, How, Transition period, Enterprise, Related Projects, Word, and RFCs sections. This draft is built only from the `Status` enum already present in `000000-rfc-template.md` (`Draft | Proposed | Final | Superseded | Rejected`). If the live README has additional or different detail, please share it so this can be reconciled rather than becoming a second, conflicting source of truth.

This document defines what each `Status` value in an RFC's front matter means, when it applies, and what is (and is not) safe to assume about an RFC in that status.

## Draft

The RFC is being actively written or discussed. Content, scope, and even the core proposal may still change substantially, including in ways that invalidate earlier discussion.

- Safe to reference in ongoing conversation by title/slug.
- Not safe to treat as a stable external citation — anything depending on a Draft RFC should expect it may change or be withdrawn.
- The RFC Number exists (per RFC on numbering) but its existence does not imply stability of content.

## Proposed

The RFC's core design questions have been resolved through discussion and the author considers it complete and ready for formal review/acceptance, but it has not yet been accepted.

- Same caution as Draft applies: content can still change based on review feedback.
- This status signals "ready for a decision," not "decided."

## Final

The RFC has been accepted as the settled decision. Its content is not expected to change; any further change is handled either by a superseding RFC or, for very minor corrections (e.g. typos), through the normal repository edit process rather than reopening the design.

- Safe to cite and depend on from other RFCs and from implementation code.
- Other RFCs may set `Depends_on` or `Extends` pointing at a Final RFC with confidence that it will not shift under them.

## Superseded

The RFC was once Final (or, in rare cases, Draft/Proposed and abandoned in favor of a replacement) but has been replaced by a newer RFC. The superseding RFC's `Supersedes` field should point back to this one, and this RFC's `Superseded by` field should point to the new one.

- A Superseded RFC remains in the repository for historical record; it is not deleted.
- New work should depend on the superseding RFC, not the superseded one.

## Rejected

The RFC was considered and explicitly not accepted. It remains in the repository as a record of a design direction that was evaluated and why it wasn't taken, which is useful so the same path isn't re-litigated without new information.

- A Rejected RFC's `RFC Number` is not reused.
- If circumstances genuinely change such that the idea deserves reconsideration, this should be a new RFC (with its own number) that references the rejected one via `Related`, rather than reviving the old one in place.

## Unresolved questions

- Is there an intermediate status needed between Proposed and Final for something like "accepted in principle, pending a specific dependency landing first"? Not addressed here.
- Should `Rejected` distinguish between "rejected outright" and "rejected for now, worth revisiting later," or is that better captured in the RFC's own text (e.g. its Future possibilities section) rather than as a status value?
