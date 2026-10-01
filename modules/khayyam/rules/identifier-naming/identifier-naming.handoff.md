# Khayyam Rule — Identifier Naming Handoff
Open state for [identifier-naming.md](./identifier-naming.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — conventions stated 2026-09-29 from [rules-in-docs audit](../../../../chats-context/memar-go-migration/decisions/rules-in-docs-audit.md); not yet enforced as an automated gate on the full corpus.

## Decisions
- **Naming style, transliteration, script choice, and casing are the organization's, not the grammar's** — Decided (2026-09-25, owner, under the rule-first test), after the ASCII repertoire restriction was withdrawn from the language documents. A repertoire restriction does not change what a program means, and a developer writing Persian or Chinese names would have been blocked by the specification itself.
- **The rule lives here rather than in the language documents** — Decided (2026-09-26, owner, under the base-documents rule): a rule catalog entry is where an organization's convention belongs, and the language document states the shape of an identifier and nothing about style.

## Open Questions
- **How strictly the stated conventions apply to the ported corpus.** The rule now states PascalCase and domain-meaningful naming; the corpus still carries Go-inherited spellings and qualified names from the port — reconciliation is incremental, not a single gate flip.
- **Whether a linter rule preferring a script is wanted.** Considered on 2026-09-25 and not written, because where suggested rules are catalogued was itself open in the [Linter handoff](../../../../docs/protocols/computer/linter.handoff.md). The question is now answerable in principle — this folder is where a Khayyam rule lives — and remains unasked.
- **Whether the rule should be per-organization or per-language.** The subject here is this repository's own sources; the same subject in another project is that project's rule. Whether a rule this shape belongs in a shared catalog at all, or only in each project's own repository, is undecided and is the same question the catalog's own standing raises.
- **How it meets the [qualified names rule](../qualified-names/qualified-names.md).** Two naming rules over one name, with no stated relation: qualification is a collision remedy, style is a preference, and an organization could hold either without the other. Nothing yet says which wins when a style would produce a collision.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [identifier-naming.md](./identifier-naming.md) | Base — the rule | Keep in sync with the corpus |
| [qualified-names.md](../qualified-names/qualified-names.md) | Sibling — the other naming rule, over collisions | Keep in sync |
| [Khayyam → Language Keyword in a Glance](../../../../docs/khayyam/khayyam.md#language-keyword-in-a-glance) | Depends_on — the shape of an identifier | None (read) |
| [linter.handoff.md](../../../../docs/protocols/computer/linter.handoff.md) | Reference — where the catalog question was raised | Keep in sync |
