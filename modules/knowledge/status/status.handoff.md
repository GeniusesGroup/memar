# Status Handoff

## Topic & Purpose
Status as a shared, cross-domain label/edge mechanism — not owned by Transaction or any pair of modules. Migrated from the Organization ideas backlog (2026-09-16).

## Status
Active — shared-concept decision is decided; which module owns Status remains open.

## Decisions

### From Organization ideas backlog

- **Status is a shared concept.** Statuses ride as loop-edges on any node. A transaction uses that machinery. *(decided, module ownership open)*
- **A status is a loop-edge.** The per-record fact is the edge type. A query for records that carry it uses that type and does not insert a node. Promotion to a node is for when the status itself is the subject of further relations. *(written in [status.md](status.md); owner asked whether the query's identity forces a node — confirmation still open)*
- **Shared loop-edges live in this module's `edges-loop/`.** Statuses that belong to one domain live in that domain's `status/` folder, same loop-edge shape. *(owner asked where a domain's statuses are defined, after `law/status/` was removed)*

## Open Questions
- Module ownership of Status (which domain is the canonical home while remaining shared machinery).
- Does the owner accept that a query such as "all laws with this status" keeps the status as an edge type, or should that query's identity promote the status to a node?

## Related Artifacts
- [`README.md`](README.md)
- [`../../economics/transaction/transaction.handoff.md`](../../economics/transaction/transaction.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Bookkeeping domain (Status bullet) (2026-09-16 migration).
