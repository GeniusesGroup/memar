# Linter Handoff

Open work for `linter.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Topic & Purpose
Resume the 2026-09-15 toolchain-layer rewrite (memory, linter, compiler, runtime moved into `docs/protocols/` and rewritten as language-independent protocols). The originating session's context is full; the owner still has critiques of that rewrite that have not all been stated. This file carries the one critique that was stated, plus the state the next session must not re-derive.

## Status
Paused — rewrite applied, not committed as of the pause; owner review incomplete.

## Ambiguities Resolved

### "Khayyam has no linter rules" did not mean there are no rules
- What was unclear: the session treated the claim as "do not put governance rules on the Khayyam shelf / Khayyam grammar owns none," and then scattered suggested checks into subject documents (`get`/`set` into encapsulation, orphan rule into modularity, type-as-argument into method).
- What is now clear: the claim was that **suggested rules vary by organization**, not that no suggested rules exist. Spreading those suggestions into subject documents both gives each rule a topical home and turns those documents into a place of maybes.
- Evidence: owner's correction, 2026-09-15, after the rewrite landed.

## Decisions

### Subject documents keep what is true of the subject; maybes do not live there by default
- Confidence: Tentative — stated as the criterion the next session should test, not yet applied as a second rewrite.
- Reasoning: Encapsulation's "fields are private" is a fact of the model. "A linter MAY generate get/set on request" is an organizational suggestion about tooling. Mixing them makes the subject document a catalogue of optional policy.
- Rejected for now: leaving the session's scatter as the settled pattern (Error's `Err` prefix stays a valid pattern for a convention the *subject itself* owns; it is not automatically the pattern for every suggested diagnostic).

### A dedicated suggested-rules protocol document is the candidate home
- Confidence: Explored-but-unresolved.
- What was proposed: a protocol-layer document where suggested (non-binding, organization-overridable) governance rules are authored — the owner's sketch name was `khayyam-suggested_rules.md` in `docs/protocols/`.
- Naming constraint if it is created: the protocols folder already carries the category, so a `khayyam-` prefix would re-create the shelf-as-claim problem this session existed to remove. Candidate filename: `suggested_rules.md` (underscore as one conceptual term). Khayyam-specific *instances* of a suggestion cite the language's realization; they do not own the catalog.
- Criteria for membership, still to design: a rule that an organization may adopt or drop without forking a language or a subject document; each entry names the subject it relates to and the check's tier; the [Linter](./linter.md) protocol stays the mechanism (how a linter works, how a rule is authored, configuration), not the catalogue of suggestions.

## Open Questions

### Do suggested rules get a catalog document, stay in subject documents, or split by kind?
- Why it matters: the session's scatter already landed `get`/`set` generation in [encapsulation.md](../khayyam/encapsulation.md), the orphan rule in [modularity.md](../khayyam/modularity.md), and type-as-argument in [method.md](../khayyam/method.md). If the catalog is chosen, those MAY/SHOULD sentences move; the subject's facts stay. If scatter is kept, subject documents remain mixed fact-and-maybe.
- Blocks continuation of further suggested-rule content: yes.
- Path: next session decides the home first, then moves or keeps the three landings as a single pass. Do not add more suggested rules to subject documents until this is decided.

### The rule-authorship notation
- State: required members of a governance rule are stated in [Linter](./linter.md) (subject, tier, default, override); the notation — a configuration schema, a capability interface, or a Syllab-level annotation — is not. If `suggested_rules.md` is created, the notation is that document's problem as much as this one's.
- Next: design after the catalog-versus-scatter decision.

### Should fold state persist per-file, per-project, or reset per session?
Whether fold state should persist per-file, per-project, or reset per session is an IDE UX decision not settled by [Linter → Tooling may present structure first](./linter.md#tooling-may-present-structure-first).

### Should the SHOULD-level body folding degrade for very small files?
Whether the SHOULD-level structural folding should degrade for very small files is an IDE UX decision not settled here.

### Is "local directory" the right boundary unit for the Orphan Rule?
Whether "local directory" is the right unit for the orphan-rule realization in [Modularity in Khayyam](../khayyam/modularity.md) — as opposed to a repository root, an explicitly declared ownership file, or a linter configuration map — is not settled; the directory heuristic is simple but arbitrary at monorepo scale.

### Should generated setters default to bare assignment or route through a validation hook?
Whether generated setters should default to bare assignment or to routing through a validation hook the capsule declares is not settled. Placement of the generation assist itself is in doubt pending the catalog-versus-scatter question above.

### Should the Orphan Rule's boundary unit be configurable, and what does the default ship as?
Should the boundary unit for the orphan rule (directory vs. repository vs. declared ownership) be configurable per organization, and what does the default configuration ship as?

## Assumptions

- The 2026-09-15 rewrite of Memory, Compiler, and Runtime is still under owner review; further unstated critiques exist. Stability: Unexamined — do not treat those three rewrites as accepted until the owner says so.
- Historical changelog pointers to retired paths stay as provenance. Stability: Strong.

## Proposed Next Steps

1. New session. Read this handoff completely before editing. Do not continue the rewrite in the exhausted session's context.
2. Take the remaining owner critiques of Memory / Compiler / Runtime first if they are ready — those documents were rewritten in the same pass and have not been reviewed.
3. Decide catalog versus scatter for suggested rules (the open question above) before moving any more MAY/SHOULD sentences.
4. If the catalog is chosen: propose `docs/protocols/suggested_rules.md` with replacement-ready English text and the list of files that would lose their maybe-sentences; wait for approval before applying.

## Related Artifacts

- [Linter](./linter.md) — Update after the catalog decision.
- [Encapsulation in Khayyam](../khayyam/encapsulation.md) — Review: `get`/`set` MAY paragraph may move.
- [Modularity in Khayyam](../khayyam/modularity.md) — Review: orphan-rule MAY/MUST paragraph may move.
- [Method in Khayyam](../khayyam/method.md) — Review: type-as-argument suggested diagnostic may move.
- [Memory](./memory.md), [Compiler](./compiler.md), [Runtime](./runtime.md) — Review; owner critiques pending.
- Working tree: the rewrite is uncommitted; a fresh session should `git status` before further edits.

## Anticipated Work

- The rule-authorship notation.
- A reference linter configuration, shipped with the first tooling release, encoding flow-correctness checks as defaults-on and conventions as opt-in sets.
- An extension point for organization-defined diagnostics.
- A conformance suite for linter implementations, mirroring the compiler-side suite proposed in [Compiler Handoff](./compiler.handoff.md).
- If created: the suggested-rules catalog and the move of the three maybe-sentences into it.
