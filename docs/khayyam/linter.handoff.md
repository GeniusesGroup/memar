# Khayyam Linter & Tooling Rules Handoff

Open work for `linter.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Should fold state persist per-file, per-project, or reset per session?
Whether fold state should persist per-file, per-project, or reset per session is an IDE UX decision not settled by the folding rules in [Khayyam Linter & Tooling Rules](./linter.md#ide-behavior--visual-formatting). (Migrated from that topic's retired Unresolved questions.)

### Should the SHOULD-level body folding degrade for very small files?
Whether the SHOULD-level structural folding should degrade for very small files is an IDE UX decision not settled here. (Migrated from the IDE Behavior & Visual Formatting topic's retired Unresolved questions.)

### Is "local directory" the right boundary unit for the Orphan Rule?
Whether "local directory" is the right unit for the [Orphan Rule](./linter.md#cross-file-methods--the-orphan-rule-monkey-patching-prevention) boundary — as opposed to a repository root, an explicitly declared ownership file, or a linter configuration map — is not settled; the directory heuristic is simple but arbitrary at monorepo scale. (Migrated from the Cross-file Methods — The Orphan Rule topic's retired Unresolved questions.)

### Should generated setters default to bare assignment or route through a validation hook?
Whether generated setters should default to bare assignment or to routing through a validation hook the capsule declares (e.g., a designated `Set`-guard method) is not settled; the latter preserves domain invariants but adds a convention to be specified. (Migrated from the Boilerplate Generation topic's retired Unresolved questions.)

### Where does each diagnostic fall on the compiler/linter enforcement line, and which are default-ON?
What is the concretely specified boundary between compiler-enforced and linter-enforced for each diagnostic this document mentions — in particular which diagnostics MUST be on by default in a reference linter, versus opt-in? The [syntax/governance principle](./khayyam.md#separation-of-syntax-and-governance-a-principle) supplies the test ("existence vs. flow"), but per-rule classification needs a settled pass. (Migrated from the document-level retired Unresolved questions.)

### Should the Orphan Rule's boundary unit be configurable, and what does the default ship as?
Should the boundary unit for the [Orphan Rule](./linter.md#cross-file-methods--the-orphan-rule-monkey-patching-prevention) (directory vs. repository vs. declared ownership) be configurable per organization, and what does the default configuration ship as? (Migrated from the document-level retired Unresolved questions.)

## Anticipated Work

- A reference linter configuration, shipped with the first tooling release, encoding the MUST-level rules as defaults and the suggested diagnostics as opt-in sets. (Migrated from the document-level retired Future possibilities.)
- An extension point for organization-defined diagnostics, so custom governance rules plug into the same machinery rather than living in ad-hoc scripts. (Migrated from the document-level retired Future possibilities.)
- A conformance suite for linter implementations, mirroring the compiler-side one proposed in [Khayyam Compiler Handoff → Anticipated Work](./compiler.handoff.md#anticipated-work). (Migrated from the document-level retired Future possibilities; the link re-pointed from `khayyam-compiler.md#discussion`, whose target section that document has since retired.)
