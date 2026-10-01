# Khayyam Rule — Code Scope Placement Handoff
Open state for [scope-placement.md](./scope-placement.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — ruled 2026-09-26 (owner): the outcome stands, its kind changed from a language rule to this toolchain's rule.

## Decisions
- **A code scope is placed only inside a method body** — Decided (2026-09-26, owner), twice over: first as a language rule with the reason that inertness requires it, then as a toolchain rule with the same reason and a narrower reach. The toolchain behavior never changed between the two answers.
- **The upstream level is Type's Scope section** — Decided (2026-09-26, owner), then reversed 2026-09-26 under the shape decision: a base document does not carry a reminder about a tool's rule, so the level that may lift the limitation is recorded here and in [Type → Scope](../../../../docs/type.md#scope--type-as-semantic-boundary) as a fact about the category rather than as a standing request.

## Open Questions
- **What the accept row actually proves at M1.** The parser treats `mt` bodies as opaque text — control flow is M3's subject — so a `sc` inside a method body is carried as body text and never parsed as a declaration. The in-body accept row therefore shows that the toolchain tolerates the text, not that it has checked the scope; the rule is not yet testable from the inside, and it becomes so when M3 parses bodies.
- **Whether a dropped rule would need a meaning for a file-level `sc`.** Dropping the rule is stated above as a real option, but it is only real if something can say what a scope outside a method body *is* — driven by whom, entered how. No document in this repository supplies that, and the honest form of the answer is that an organization dropping the rule also has to supply the meaning.
- **Whether the rule is a `compiler-gate` or a `governance` rule once the engine exists.** It is recorded as compiler-gate because it refuses, but the distinction the accepted model draws is about who may disable it, and that question is part of the unfinished Rule protocol work.
- **Interaction with qualified references.** The resolver skips a qualified type reference (`pkg.Type`) without a binding check; whether a `sc` may name such a reference is undecided and is entangled with the qualified-name resolution semantics the [toolchain handoff](../../execution.handoff.md) carries.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [scope-placement.md](./scope-placement.md) | Base — the rule | Keep in sync with the parser and the matrix |
| [core/src/parse.ts](../../core/src/parse.ts) | Implements — the `scope-placement` refusal | None (unchanged) |
| [core/test/refusal.test.ts](../../core/test/refusal.test.ts) and [core/test/form.test.ts](../../core/test/form.test.ts) | Reference — the two rows that assert this rule | Keep in sync |
| [Type → Scope](../../../../docs/type.md#scope--type-as-semantic-boundary) | Depends_on — the category the rule is not a claim about | None (read) |
| [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) | Depends_on — the inertness the rule rests on | None (read) |
| [execution.handoff.md](../../execution.handoff.md) | Reference — where the reversal is recorded | Keep in sync |
