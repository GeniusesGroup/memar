# Khayyam Rule — Comment Forms Handoff
Open state for [comment-forms.md](./comment-forms.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — ruled 2026-09-26 (owner), reversing the same day's decision to write the forms into the grammar; recorded as a rule 2026-09-26.

## Decisions
- **The forms are a tool's rule** — Decided (2026-09-26, owner). Khayyam legislates only what a program's meaning requires, and a comment may be absent, present, or forbidden without any program becoming ill-formed. The earlier argument — that a comment decides which programs exist, so the markers are the grammar's — answered a different question than the one the test asks.
- **The scanner is unchanged** — State. [core/src/scan.ts](../../core/src/scan.ts) implements both forms and the unterminated-block refusal. A rule living in this folder does not change what the scanner does.

## Open Questions
- **Whether a second toolchain may nest block comments.** Nothing in this repository's corpus needs it — `/* … */` appears once per file, as the license header — so the corpus neither supports nor refutes a nesting rule, and the question is a rule an organization answers for itself.
- **Compiler input, or a compiler-gate rule?** As implemented the forms are compiler input: the scanner drops them before the parser sees anything, and no row of [core/test/form.test.ts](../../core/test/form.test.ts) or [core/test/refusal.test.ts](../../core/test/refusal.test.ts) asserts their behavior. Whether the rule engine should own them — so a second frontend could differ without forking the scanner — waits on the Rule and rule-engine members, which the [toolchain handoff](../../execution.handoff.md) records as provisional.
- **Whether lexical trivia belongs in this catalog at all.** An unterminated string and an unterminated block comment are both lexical, and neither is a condition a linter or a governance rule would want to evaluate. If the catalog's scope narrows to the semantic rules, the lexical refusals stay the scanner's and this rule folds into the comment policy's file.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [comment-forms.md](./comment-forms.md) | Base — the rule | Keep in sync with the scanner |
| [comment-policy.md](../comment-policy/comment-policy.md) | Depends_on — what a comment says, as against how it is marked |
| [execution.handoff.md](../../execution.handoff.md) | Reference — where the reversal and the owner's reasoning are recorded | Keep in sync |
| [Khayyam → Language Keyword in a Glance](../../../../docs/khayyam/khayyam.md#language-keyword-in-a-glance) | Reference — the language's own lexical statement, which says nothing about comments | None (read) |
