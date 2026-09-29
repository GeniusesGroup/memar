# Khayyam Rule — Type as Argument Handoff
Open state for [type-as-argument.md](./type-as-argument.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — rule added 2026-09-29 from [rules-in-docs audit](../../../../chats-context/memar-go-migration/decisions/rules-in-docs-audit.md).

## Open Questions
- **Exact linter conditions** for distinguishing legitimate type-level `sc`/`mt` arguments from bare-type smells.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [type-as-argument.md](./type-as-argument.md) | Base — the rule | Keep in sync |
| [Method in Khayyam → Type-level arguments](../../../../docs/khayyam/method.md#type-level-arguments-for-sc-and-mt) | Depends_on — compiler acceptance | None (read) |
| [linter.handoff.md](../../../../docs/protocols/computer/linter.handoff.md) | Reference — linter protocol | Keep in sync |
