# Khayyam Rule — Unbound Type Name Handoff
Open state for [unbound-type-name.md](./unbound-type-name.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — decided 2026-09-25 as the fourth outcome, added to the three rerouted ones; recorded as a rule 2026-09-26.

## Decisions
- **The editor's diagnostic surface asks the question too** — Decided (2026-10-03). [lsp/src/unbound-names.ts](../../lsp/src/unbound-names.ts) walks `referencedTypes` ([core/src/sr.ts](../../core/src/sr.ts)) and the visible set `analyzeImports` ([core/src/frontend.ts](../../core/src/frontend.ts)) builds, so the server and the gate cannot disagree about a name; the walk is not a walk of the server's own over signatures, because that would be a second definition of a type reference. The rule's document already stated the check, so nothing in it changed — a rule living in a rules folder is a record, and this is the case where the record and the toolchain agreed before the toolchain asked. What is now true that was not: the gate reaches this question only after every `in` in the unit is accounted for, so on a repository whose imports do not resolve the editor is the only surface that asks it.

## Open Questions
- **Qualified references carry no check.** `pkg.Type` is skipped, so a program may name a type through a qualifier the toolchain never resolves. This is the largest known gap in the toolchain's checking, and it is not a rule question but a semantics question: what a qualifier denotes has never been decided, and the [qualified names rule](../qualified-names/qualified-names.md) assumes a reading this resolver does not yet implement.
- **Method bodies are opaque, so names inside them are unchecked.** The parser carries a `mt` body as text until M3, which means a body's references are invisible to this rule. The rule is therefore currently weaker than its own text, and the matrix row it rests on comes from a signature rather than a body.
- **Whether the visible set is per-unit or per-program.** The rule resolves against what one file declares and includes, so a name supplied by a file that nothing includes is unbound. Whether a unit's closure is its own or its module's is a module-membership question the [manifest handoff](../../../../docs/khayyam/modularity.handoff.md) is working on.
- **Whether a `compiler-gate` or a `governance` rule.** Recorded as compiler-gate because it refuses; the Rule protocol members that would settle the class are provisional.
- **Whether an unbound name and a name of the wrong kind are one condition.** The toolchain's kinds are coarse (see the [kind mismatch rule](../kind-mismatch/kind-mismatch.handoff.md)), and a name brought in as a `vr` cannot currently satisfy a type reference. Whether that is this rule or the kind rule is undecided.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [unbound-type-name.md](./unbound-type-name.md) | Base — the rule | Keep in sync with the resolver |
| [qualified-names.md](../qualified-names/qualified-names.md) | Depends_on — the naming convention whose references this rule does not yet check | Keep in sync |
| [core/src/frontend.ts](../../core/src/frontend.ts) | Implements — the `unbound-type-name` refusal | None (unchanged) |
| [core/test/refusal.test.ts](../../core/test/refusal.test.ts) | Reference — the row that asserts this rule | Keep in sync |
| [khayyam.handoff.md](../../khayyam.handoff.md) | Reference — the qualified-name resolution semantics | Keep in sync |
