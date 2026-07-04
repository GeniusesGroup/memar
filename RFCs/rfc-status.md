---
RFC Number: 495001
Title: "RFC Status Semantics"
Status: Proposed
Start Date: 2026-07-04
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: ""
    task: []
  - name: "Claude"
    uri: "https://claude.ai"
    model: "claude-sonnet-5"
    effort: "Medium - extended thinking enabled"
    contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    task: []
---

## Summary
Defines, in detail, what each value of the `Status` field commits a reader to assuming about an RFC's stability, citability, and dependency-worthiness — beyond the one-line-per-value table already in the RFCs `README.md`, which stays the fast-scan index.

## Motivation
The README's Status table is intentionally compact for quick scanning. But deciding whether to set `Depends_on` or `Extends` on another RFC, or whether to treat its content as settled enough to build on, needs a sharper answer than a single line can give — for example, exactly what a Proposed RFC's Status implies about the chance it still changes before Final, or what obligation (if any) attaches once an RFC reaches Final. Leaving those obligations implicit invites different contributors, over a multi-generational timeline, to infer them inconsistently.

## Guide-level explanation
When reading an RFC, its `Status` field tells you not just "where it is in the process" but specifically what you may safely do with it:

- **Draft** or **Proposed**: treat the content as still capable of changing. Reference it in discussion, but don't build a dependency on it that assumes its current wording is final.
- **Final**: safe to depend on. Other RFCs may point `Depends_on` or `Extends` at it with confidence it won't shift under them.
- **Superseded**: historical only — read the RFC it points to via `Superseded by` instead for current guidance.
- **Rejected**: historical only — kept so the same direction isn't re-evaluated later without new information.

## Reference-level explanation
| Status         | Meaning                                                                                                                                           | Applied to                       | Safe to depend on?                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------- |
| **Draft**      | Direction is not yet settled; real, unresolved questions remain. Each Draft RFC's own "Unresolved questions" section states exactly what is open. | Empty                            | No                                                 |
| **Proposed**   | Design discussion reached consensus; ready for final review before being reflected in canonical documentation.                                    | Empty                            | Not yet — may still be revised during final review |
| **Final**      | Reflected in canonical documentation.                                                                                                             | Lists exactly where              | Yes                                                |
| **Superseded** | Replaced by a newer RFC. See `Superseded by`.                                                                                                     | Unchanged from when it was Final | No — depend on the superseding RFC instead         |
| **Rejected**   | Considered and explicitly not adopted. Kept for the historical record.                                                                            | Empty                            | No                                                 |

Additional rules:
- `RFC Number` is never reused, regardless of status, including Rejected.
- Moving a Final RFC's substance requires a new, superseding RFC — not an in-place edit of the Final RFC's design. What counts as a substance-level change versus a minor correction (e.g. a typo, or a genuinely ambiguous sentence) that can be fixed in place is not defined by this RFC (see Unresolved questions).
- If circumstances change enough that a Rejected idea deserves reconsideration, that is a new RFC with its own number, referencing the rejected one via `Related`, rather than reviving the old one in place.

## Drawbacks
- This creates a second document describing Status semantics alongside the compact table in `README.md`. The two must stay consistent as either evolves, which is an ongoing (if currently small) maintenance obligation, not a one-time cost.
- Elaborates obligations (e.g. "Final is safe to depend on") that were previously left implicit. If a Final RFC needs a genuine correction that falls short of a new design direction, this RFC does not define the exact procedure for that — it only distinguishes "correction" from "supersession" in principle, not in a way precise enough to remove judgment calls.

## Rationale and alternatives
- **Leave only the one-line table, let detailed obligations be inferred informally (rejected)**: informal inference tends to drift inconsistently across a project expected to span multiple generations and contributors.
- **Fold this level of detail directly into `README.md` instead of a separate file (rejected)**: keeps the README from staying a fast, scannable index, which was the stated reason for extracting this content out in the first place.

## Prior art
Several long-running spec processes separate a short status marker from a fuller definition of what that marker commits readers and implementers to — for instance, the distinction between an RFC's short status line and the fuller governing document that defines what each status level actually means for implementers is a pattern that recurs across standards-track processes, not something unique to this project.

## Unresolved questions
1. What precisely distinguishes a "minor correction" that can be applied in place to a Final RFC from a change substantial enough to require a superseding RFC?
2. Should there be a formal mechanism to keep this document and the README's compact table synchronized as both evolve, or is manual vigilance sufficient at the current scale?

## Future possibilities
If a future RFC introduces an additional status value (for example, something between Proposed and Final for "accepted in principle, pending a specific dependency"), this document is where that value's semantics should be added.
