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
- State: the 2026-09-06 finalization and the first wave (commit 32c44e0, 14 documents) left 28 base documents still carrying a top-level `## Discussion` section whose content the Relevance discipline now routes to the paired changelog and handoff. The specification's own stale references to the retired section were fixed on 2026-09-08.
- Files: `agency.md`, `content.md`, `framework.md`, `immutable_infrastructure.md`, `knowledge.md`, `modularity.md`, `system.md`, `terminology.md`, `khayyam.md`, `khayyam-abstraction.md`, `khayyam-agency.md`, `khayyam-compiler.md`, `khayyam-control_flow.md`, `khayyam-encapsulation.md`, `khayyam-inheritance.md`, `khayyam-linter.md`, `khayyam-metaprogramming.md`, `khayyam-method.md`, `khayyam-modularity.md`, `khayyam-polymorphism.md`, `khayyam-runtime.md`, `khayyam-variable.md`, `protocols/abstraction-implements.md`, `protocols/chapar.md`, `protocols/control-flow.md`, `protocols/filesystem.md`, `protocols/giti.md`, `protocols/lexer.md`.
- Pattern: follow the first wave (commit 32c44e0). Route each block by [Relevance discipline](./documentation-explanation.md#relevance-discipline): premise evidence stays inline at the claim it supports; considered-and-not-done and prior-art surveys go to the changelog entry that made the decision; open questions and anticipated work go to the paired handoff; content already graduated into the body is dropped, not copied.
- Caution: the 2026-09-07 changelog-remediation campaign left uncommitted reformatting of these documents' changelog files (bare Contributors tags, claim-shaped outcomes, `Deliberation` sections). The migration session adds new entries on top of that working state - it does not reformat again - and checks `git status` first: several base documents here (e.g. `framework.md`, `khayyam-polymorphism.md`, `immutable_infrastructure.md`, some `protocols/` files) may carry in-progress edits from other sessions.
- Related: the `Future possibilities` disposition question above is part of this wave's routing decision.
- Next: dedicated session, one sub-agent per document with this entry as the brief, then an owner audit pass - the first wave needed one (its changelog records "a final audit found several blocks that the earlier passes missed").
