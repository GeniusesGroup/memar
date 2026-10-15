# Linter Handoff
Open work for `linter.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Topic & Purpose
Resume the 2026-09-15 toolchain-layer rewrite (memory, linter, compiler, runtime moved into `docs/modules/` and rewritten as language-independent protocols). The originating session's context is full; the owner still has critiques of that rewrite that have not all been stated. This file carries the one critique that was stated, plus the state the next session must not re-derive.

## Status
Paused — rewrite applied and committed; owner review incomplete.

## Decisions

### Subject documents keep what is true of the subject; maybes do not live there by default
- Confidence: Tentative — stated as the criterion the next session should test, not yet applied as a second rewrite.
- Reasoning: Encapsulation's "fields are private" is a fact of the model. "A linter MAY generate get/set on request" is an organizational suggestion about tooling. Mixing them makes the subject document a catalogue of optional policy.
- Rejected for now: leaving the session's scatter as the settled pattern (Error's `Err` prefix stays a valid pattern for a convention the *subject itself* owns; it is not automatically the pattern for every suggested diagnostic).

### A dedicated suggested-rules protocol document is the candidate home
- Confidence: Explored-but-unresolved.
- What was proposed: a protocol-layer document where suggested (non-binding, organization-overridable) governance rules are authored — the owner's sketch name was `khayyam-suggested_rules.md` in `docs/modules/`.
- Naming constraint if it is created: the `docs/modules/` folder already carries the category, so a `khayyam-` prefix would re-create the shelf-as-claim problem this session existed to remove. Candidate filename: `suggested_rules.md` (underscore as one conceptual term). Khayyam-specific *instances* of a suggestion cite the language's realization; they do not own the catalog.
- Criteria for membership, still to design: a rule that an organization may adopt or drop without forking a language or a subject document; each entry names the subject it relates to and the check's tier; the [Linter](linter.md) protocol stays the mechanism (how a linter works, how a rule is authored, configuration), not the catalogue of suggestions.

## Open Questions

### The rule-authorship notation
- State: required members of a governance rule are stated in [Linter](linter.md) (subject, tier, default, override); the notation — a configuration schema, a capability interface, or a Syllab-level annotation — is not. If `suggested_rules.md` is created, the notation is that document's problem as much as this one's.
- Next: design after the catalog-versus-scatter decision.

### Should fold state persist per-file, per-project, or reset per session?
Whether fold state should persist per-file, per-project, or reset per session is an IDE UX decision not settled by [Linter → Tooling may present structure first](linter.md#tooling-may-present-structure-first).

### Should the SHOULD-level body folding degrade for very small files?
Whether the SHOULD-level structural folding should degrade for very small files is an IDE UX decision not settled here.

### Is "local directory" the right boundary unit for the Orphan Rule?
Whether "local directory" is the right unit for the orphan extension (`bundles/khayyam/rules/orphan-extension/orphan-extension.md`) rule — as opposed to a repository root, an explicitly declared ownership file, or a linter configuration map — is not settled; the directory heuristic is simple but arbitrary at monorepo scale.

### Should generated setters default to bare assignment or route through a validation hook?
Whether generated setters should default to bare assignment or to routing through a validation hook the capsule declares is not settled. Placement of the generation assist itself is in doubt pending the catalog-versus-scatter question above.

## Assumptions
- The 2026-09-15 rewrite of Memory, Compiler, and Runtime is still under owner review; further unstated critiques exist. Stability: Unexamined — do not treat those three rewrites as accepted until the owner says so.
- Historical changelog pointers to retired paths stay as provenance. Stability: Strong.

## Proposed Next Steps
1. Take the remaining owner critiques of Memory / Compiler / Runtime first if they are ready — those documents were rewritten in the same pass and have not been reviewed.
2. Decide catalog versus scatter for suggested rules (the open question above) before moving any more MAY/SHOULD sentences.
3. If the catalog is chosen: propose `docs/modules/suggested_rules.md` with replacement-ready English text and the list of files that would lose their maybe-sentences; wait for approval before applying.

## Related Artifacts
- [Linter](linter.md) — Update after the catalog decision.
- Encapsulation in Khayyam (`docs/khayyam/encapsulation.md`) — Review: `get`/`set` MAY paragraph may move.
- orphan extension (`bundles/khayyam/rules/orphan-extension/orphan-extension.md`) — Review: boundary unit open question above.
- Method in Khayyam (`docs/khayyam/method.md`) — Review: type-as-argument suggested diagnostic may move.
- [Memory](../memory/memory.md), [Compiler](compiler.md), [Runtime](runtime.md) — Review; owner critiques pending.

## Anticipated Work
- The rule-authorship notation.
- A reference linter configuration, shipped with the first tooling release, encoding flow-correctness checks as defaults-on and conventions as opt-in sets.
- An extension point for organization-defined diagnostics.
- A conformance suite for linter implementations, mirroring the compiler-side suite proposed in [Compiler Handoff](compiler.handoff.md).
- **Static-concept identity checks.** Enforcement of [Type Practice](../../type.practice.md)'s rule that each static concept is its own Type is heuristic today: structural linters can flag missing-field and generic-`Init` patterns, and the authoritative checkpoint is the code generator's input layer, where static or dynamic intent is explicit by construction. Moved here 2026-10-10 from Type Practice.
- **Rule analysis tooling**: static analysis to verify invariants, detect rule conflicts, and identify over-constraining. Moved here 2026-10-10 from Type's handoff, with the next two.
- **AI-assisted delegation generation**: instant, auditable scaffolding of forwarding methods.
- **Ownership-clarity metrics**: IDEs and linters could compute and display an "ownership clarity score" for each component — a measure of how easily a reader can determine the origin of each behavior.
