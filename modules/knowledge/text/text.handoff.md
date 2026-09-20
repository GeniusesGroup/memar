# Text Handoff

## Topic & Purpose
Identity & Text ownership: human-readable text lives only in the Text domain; other domains relate to it. Migrated from the Organization ideas backlog (2026-09-16).

## Status
Active — both bullets decided.

## Decisions

### From Organization ideas backlog — Identity & Text ownership

- Human-readable text may be stored only in the Text domain; every other domain holds a relation to it (username, email, titles, comment bodies); identity attributes like email are entities linked to User, not owned fields. *(decided)*
- Identity is independent of location: content-derived or immutable-at-creation stable reference — the org's conclusion from the Git analysis; Content Addressability is the one Git property worth keeping. *(decided)*

## Open Questions
None recorded in the migrated passage.

## Related Artifacts
- [`README.md`](README.md) (if present)
- [`../content/content.handoff.md`](../content/content.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Knowledge / Content / Task → Identity & Text ownership (2026-09-16 migration).
- Token-as-smallest-knowledge-unit and Text-only human-text arguments expanded in Content handoff + [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md) (Discussion — Modeling method, entry points, and documentation facets).
