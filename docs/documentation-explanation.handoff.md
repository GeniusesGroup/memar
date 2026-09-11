# Documentation — Explanation Handoff

## Topic & Purpose
Open questions and anticipated work for the Explanation facet's governing specification (`documentation-explanation.md`), relocated there when the documentation method removed unresolved-question lists from base documents' bodies.

## Status
Active

Open work for `documentation-explanation.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Should the Optional Sections catalog gain further entries?
- State: raised while drafting the catalog; never resolved. Candidate entries named in the original working note: `Evidence Against (the Idea)`, `Design Principles`, `Consequences`, `Open Questions` itself.
- Consideration: an `Open Questions` catalog entry is now complicated by the body's own rule that unresolved questions live in handoffs, not in documents — a catalog entry for it may be self-defeating or may be exactly the sanctioned home for documents that legitimately need it. This tension is the reason the item is still open.
- Next: evaluate each candidate against real documents that felt the absence of it.

### Is `Future possibilities` still a legitimate Discussion wrapper?
- State: raised while removing `Prior art` and `Unresolved questions` from the Discussion pattern. By the same [Relevance discipline](./documentation-explanation.md#relevance-discipline) criterion, future-speculative content serves neither the current-state reader nor the audit reader cleanly — it is roadmap, i.e. working state. It was kept in the pattern for now because removing it was beyond the directive that prompted the change.
- Next: decide independently whether `Future possibilities` migrates to handoffs (as anticipatory work) or stays as a boundary statement.

### Should this consolidated spec itself be split again once the loading cost of one long document starts to matter?
- State: carried from the document's former Unresolved questions list at the migration that removed that list.
- Next: revisit when document count or session-loading evidence makes the cost measurable.

### ID collision resolution tooling
- State: two or more documents drafted in the same hour is expected and normal, and manual resolution is a stopgap. A small helper script or shell alias that prints the current hour-value and checks for an existing collision would help; replacing manual resolution with an algorithmic mechanism is preferable long-term, but the specific tooling and workflow is not decided.
- Next: build once the number of contributors or documents justifies the tooling investment.

### Is the three-section fixed skeleton sufficient for Explanation-facet documents?
- State: raised 2026-09-10 while removing the Results section, following the Discussion section's removal (2026-09-06). The removal round's research shows every scientific-skeleton (IMRAD) content type has a named home - the fixed trio carries the artifact's current state, anticipated results route to the Abstract claim, derived results to `Implications`, and observed results to the changelog, inline evidence, research records, or the handoff (see [documentation.md → Results routing](./documentation.md#results-routing)) - but whether future documents will feel the absence of a fixed home for a genuinely new content type is untested.
- Next: watch real documents for content that fits neither the fixed trio nor an Optional Sections entry; judge candidates by the [Relevance discipline](./documentation-explanation.md#relevance-discipline) criterion, not by skeleton-completeness intuition.
