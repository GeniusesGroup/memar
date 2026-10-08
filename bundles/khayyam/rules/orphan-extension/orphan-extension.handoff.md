# Khayyam Rule — Orphan Extension Handoff
Open state for [orphan-extension.md](./orphan-extension.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — rule added 2026-09-29 from the rules-in-docs audit, whose session file was not kept in the repository.

## Open Questions
- **Cross-file visibility within a module** — what the importer of a type may attach across files of one module boundary (see [Modularity handoff](../../../../docs/khayyam/modularity.handoff.md)).

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [orphan-extension.md](./orphan-extension.md) | Base — the rule | Keep in sync |
| [Modularity in Khayyam → Inclusion Is Not Module Definition](../../../../docs/khayyam/modularity.md#inclusion-is-not-module-definition) | Depends_on — local-directory extension syntax | Link only |
| [Inheritance in Khayyam → Linter Rules](../../../../docs/khayyam/inheritance.md#what-the-linter-may-add) | Depends_on — linter-rules pointer | Link only |
| [linter.handoff.md](../../../../docs/modules/computer/linter.handoff.md) | Reference — boundary configuration | Keep in sync |
