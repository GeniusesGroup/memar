# Khayyam Rule — Name Not Declared Handoff
Open state for [name-not-declared.md](./name-not-declared.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — decided 2026-09-25 as one of the three outcomes rerouted out of the language documents; recorded as a rule 2026-09-26; renamed from *name-not-exported* 2026-09-30, the label having been read wrong on a real corpus fault.

## Open Questions
- **Whether a file offers only some of what it declares.** The rule as implemented makes every declaration in a file available to any importer, which is a stronger and simpler model than a chosen subset. Whether Khayyam's inclusion eventually grows a way for a file to name which declarations others may reach is open where module membership is worked out ([dependency management](../../../../docs/protocols/modules/dependency-management.handoff.md) — the manifest's obligations, one of which is what belongs to the module); if it does, this rule's condition changes shape. **The question was phrased for a year as "whether a file has a published surface", and that phrasing is what the rename removed**: the language has no publication step, so asking whether one exists invites an answer about a mechanism the language has not got.
- **Whether a name may be passed on by including it.** Nothing in the toolchain answers it, and it interacts with the [qualified names rule](../qualified-names/qualified-names.md): if a file re-includes a name it got from elsewhere, the name a third file sees is a name two files from its declaration.
- **Whether a `compiler-gate` or a `governance` rule.** Recorded as compiler-gate because it refuses; the distinction waits on the provisional Rule protocol members.
- **What the diagnostic should say.** Deferred with the rest of the diagnostics contract, and here the gap is sharper than elsewhere, because the useful message names the file that should have declared the name — which needs a resolution fact the analysis input does not yet carry.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [name-not-declared.md](./name-not-declared.md) | Base — the rule | Keep in sync with the resolver |
| [unresolved-import.md](../unresolved-import/unresolved-import.md) | Sibling — the same lookup, one step earlier | Keep in sync |
| [core/src/frontend.ts](../../core/src/frontend.ts) | Implements — the `name-not-declared` refusal | None (unchanged) |
| [core/test/refusal.test.ts](../../core/test/refusal.test.ts) | Reference — the row that asserts this rule, and the check that no label borrows a mechanism the language lacks | Keep in sync |
| [dependency-management.handoff.md](../../../../docs/protocols/modules/dependency-management.handoff.md) | Reference — the membership and manifest questions, which is where the open surface question now lives | Keep in sync |
