# Test Rule — Test Placement Handoff
Open state for [test-placement.md](./test-placement.md). See the repository's [documentation-handoff.md](../../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — rule added 2026-09-30 from the Test protocol's decision to state no structural condition of its own.

## Open Questions
- **Whether the plural is a repository-wide convention.** The rule argues it from the role folders this repository already carries and settles the name only for the folders it governs. Whether the two singular role folders in Khayyam's toolchain (`core/test/`, `targets/*/test/`) are the same case or a drift is undecided, and no document owns the question. Mirrored in the [protocol handoff](../../../../../docs/protocols/process/test.handoff.md).
- **Whether the Rule is checkable at all in its current form.** "A Test lives in the `tests/` folder of the module that owns the Process it names" is decidable only if a Test's subject is machine-readable; today it lives in the Test's own text. Whether the naming Rule below should require a subject marker for exactly this reason is undecided.
- **What a Test is placed against when a module is a folder of folders.** A Test naming a Process that spans two sibling modules under one parent has no single owning module under this rule. Nothing in this repository has needed it; the Rule has no answer.

## Related Artifacts
- [test.md](../../../../../docs/protocols/process/test.md) — the subject this Rule checks, and the document that owns the definition.
- [test-naming](../test-naming/test-naming.md) — the sibling Rule, on what a Test's artifacts are called.
- [modules/README.md](../../../../README.md) — the membership criterion and the kind of responsibility a module folder names.
- [rule.md](../../../../../docs/rule.md) — the concept this Rule is an instance of.
