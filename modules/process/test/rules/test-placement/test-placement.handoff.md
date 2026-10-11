# Test Rule — Test Placement Handoff
Open state for [test-placement.md](./test-placement.md). See the repository's [documentation-handoff.md](../../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — rule added 2026-09-30 from the Test protocol's decision to state no structural condition of its own.

## Open Questions
- **Whether the Rule is checkable at all in its current form.** "A Test lives in the `tests/` folder of the module that owns the Process it names" is decidable only if a Test's subject is machine-readable; today it lives in the Test's own text. Whether the naming Rule below should require a subject marker for exactly this reason is undecided.
- **What a Test is placed against when a module is a folder of folders.** A Test naming a Process that spans two sibling modules under one parent has no single owning module under this rule. Nothing in this repository has needed it; the Rule has no answer.

## Related Artifacts
- [test.md](../../../../../docs/modules/process/test.md) — the subject this Rule checks, and the document that owns the definition.
- [test-naming](../test-naming/test-naming.md) — the sibling Rule, on what a Test's artifacts are called.
- [modules/README.md](../../../../README.md) — the membership criterion and the kind of responsibility a module folder names.
- [rule.md](../../../../../docs/rule.md) — the concept this Rule is an instance of.
