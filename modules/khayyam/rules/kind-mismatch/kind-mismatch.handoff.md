# Khayyam Rule — Kind Mismatch Handoff
Open state for [kind-mismatch.md](./kind-mismatch.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — decided 2026-09-25 as one of the three outcomes rerouted out of the language documents; recorded as a rule 2026-09-26.

## Open Questions
- **The toolchain's kinds are coarser than the language's.** [core/src/frontend.ts](../../core/src/frontend.ts) reduces a declaration to `"tp"` or `"vr"`, so `cp`, `mt`, `ab`, and `sc` are one kind here. The rule is therefore *weaker* than the language could be, and whether a future engine distinguishes the subtypes — refusing a `tp` form naming a method, or accepting a form that may bring in any of them — is undecided.
- **Whether the language should state the distinction at all.** The two forms exist and the documents do not say whether they may be mixed. Until they do, this rule enforces a tool's reading of the distinction, which is exactly the situation the rule catalog exists for and also the reason the reading should be written down here rather than left in the code.
- **Whether a `compiler-gate` or a `governance` rule.** Recorded as compiler-gate because it refuses; the Rule protocol members that would settle the class are provisional.
- **Interaction with a name brought in by two routes.** If one file includes both a `tp` and a `vr` under one name — currently impossible to express, since the name is the key — the resolver's map holds one entry per name. Whether a collision at the importer is this rule or the [unbound type name rule](../unbound-type-name/unbound-type-name.md) is undecided.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [kind-mismatch.md](./kind-mismatch.md) | Base — the rule | Keep in sync with the resolver |
| [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) | Depends_on — the two line forms | None (read) |
| [Type → Type Categories Are Not a Hierarchy](../../../../docs/type.md#type-categories-are-not-a-hierarchy) | Reference — why the kinds are not one | None (read) |
| [core/src/frontend.ts](../../core/src/frontend.ts) | Implements — the `kind-mismatch` refusal | None (unchanged) |
| [core/test/refusal.test.ts](../../core/test/refusal.test.ts) | Reference — the row that asserts this rule | Keep in sync |
