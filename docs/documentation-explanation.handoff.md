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

## Anticipated Work

### Second migration wave: retire `## Discussion` from the remaining base documents
- State: 22 of the 28 base documents were migrated on 2026-09-08 (each recorded in its own paired changelog under a "Second migration wave" entry; the final audit pass dissolved a missed topic-level `#### Discussion` wrapper in `knowledge.md`, repointed stale pointers into retired sections in migrated bodies and Practice companions, and fixed cross-document references created by the wave). Six documents remain un-migrated: `content.md` — its changelog is currently off-limits for an owner-assisted remediation item (see [documentation-changelog.handoff.md → Anticipated Work](./documentation-changelog.handoff.md)), so the per-document migration entry the pattern requires cannot be appended; owner decision needed on allowing the append or handling the document separately. The other five carry in-progress edits from other sessions outside their `## Discussion` section and were skipped per the foreign-edit rule: `khayyam-polymorphism.md`, `protocols/abstraction-implements.md`, `protocols/control-flow.md`, `protocols/giti.md`, `protocols/lexer.md`.
- Files (remaining): `content.md`, `khayyam-polymorphism.md`, `protocols/abstraction-implements.md`, `protocols/control-flow.md`, `protocols/giti.md`, `protocols/lexer.md`.
- Pattern: follow the first wave (commit 32c44e0) and the completed 2026-09-08 second-wave entries. Route each block by [Relevance discipline](./documentation-explanation.md#relevance-discipline): premise evidence stays inline at the claim it supports; considered-and-not-done and prior-art surveys go to the changelog entry that made the decision; open questions and anticipated work go to the paired handoff; content already graduated into the body is dropped, not copied; every topic-level `#### Discussion` wrapper is dissolved the same way, not just the document-level `## Discussion`.
- Caution: check `git status` first — the remaining documents were skipped because their base files carried in-progress edits outside `## Discussion`; confirm those edits have landed before migrating. The 2026-09-07 changelog-remediation reformatting of these documents' changelog files is working state to append on top of, not reformat.
- Related: the `Future possibilities` disposition question above is part of this wave's routing decision — the 2026-09-08 pass routed all `Future possibilities` content to the paired handoffs as Anticipated Work (consistent with wave 1), leaving the wrapper-legitimacy question itself open.
- Next: follow-up session for the six remaining documents, one sub-agent per document with this entry as the brief, then an owner audit pass.
