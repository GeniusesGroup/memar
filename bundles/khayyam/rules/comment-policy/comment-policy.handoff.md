# Khayyam Rule — Comment Policy Handoff
Open state for [comment-policy.md](./comment-policy.md). See the repository's [handoff.practice.md](../../../../modules-plugable/knowledge/documentation/handoff/handoff.practice.md) for what a handoff is.

## Status
Active — the header clause is already universal across this repository's `.kh` files; the documentation fallback was retired (2026-10-30, owner).

## Open Questions
- **How thoroughly a declaration is documented.** Undecided, and it is the reason this rule is a rule rather than a habit: with the language silent on density, a repository either says how much prose a declaration carries or leaves every file to the author of the day. The candidates are a minimum (a summary per public abstraction), a maximum (no comment longer than the signature it documents), or a naming convention instead of a count. Nothing in the language documents or the toolchain bears on the choice, which is why it is unanswered.
- **Whether the header is a rule or a source-rewrite obligation.** As stated it is a governance rule a reader or a checker asserts. It could instead be a `source-rewrite` rule — the engine inserting or repairing the header — which the accepted rule model admits; the model is provisional, so the class is not settled.

## Decisions
- **A license header on every `.kh` file** — Decided (2026-09-25, owner, with the ported sources). Every file in this repository opens with it and the `LEGAL` reference was verified.
- **Documentation falls back to comments only where no documentation method exists** — Decided (2026-09-26, owner). The alternative — forbidding comments now — was rejected because it would have deleted the sources' only prose; the conversion is the owner's stated next step.
- **Comments are not allowed in code at all** — Decided (2026-10-30, owner). The fallback of 2026-09-26 is removed; the [Type rule](../../../../modules/computer/type/rules/no-comments-in-code/no-comments-in-code.md) owns the condition, and older files are repaired when a task changes them.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [comment-policy.md](./comment-policy.md) | Base — the rule | Keep in sync with the conversion |
| [comment-forms.md](../comment-forms/comment-forms.md) | Reference — how the prose is marked | None (read) |
| [Khayyam → Self-Documenting Code and Naming](../../../../docs/khayyam/khayyam.md#self-documenting-code-and-naming) | Depends_on — the mechanism a comment falls back from | None (read) |
| [khayyam.handoff.md](../../../../docs/khayyam/khayyam.handoff.md) | Reference — the conversion's state and the declarations that shape it | Keep in sync |
