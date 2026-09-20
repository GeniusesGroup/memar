# Status Handoff

## Topic & Purpose
Status as a shared, cross-domain label/edge mechanism — not owned by Transaction or any pair of modules. Migrated from the Organization ideas backlog (2026-09-16).

## Status
Active — shared-concept decision is decided; which module owns Status remains open.

## Decisions

### From Organization ideas backlog

- **Status is a shared concept.** Statuses (draft, authorization-pending, …) ride as labels/edges on any node, unified across transaction kinds; a Transaction must not invent its own lifecycle mechanism — it uses the general Status machinery, and the Status concept is not owned by any two modules. *(decided, module ownership open)*

## Open Questions
- Module ownership of Status (which domain is the canonical home while remaining shared machinery). *(decided, module ownership open)*

## Related Artifacts
- [`README.md`](README.md)
- [`../../economics/transaction/transaction.handoff.md`](../../economics/transaction/transaction.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Bookkeeping domain (Status bullet) (2026-09-16 migration).
