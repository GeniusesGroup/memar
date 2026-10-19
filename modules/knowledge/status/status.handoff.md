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

## Pointer to Label Research 001 (2026-10-18)
[`../label/label.research.001.md`](../label/label.research.001.md) reads status together with label and edge. Tentative, not ratified: a status is a label of kind `Status` taken as a loop-edge, plus a transition event and a synchronous-read guarantee, so there is one attachment mechanism and not two (its choice 2); the shared vocabulary splits into flags that stay (`draft`, `hidden`, `lock`, `read-only`, `block`, `optional`, `deleted`), readings that are derived (`edited`), user-ended relations that become an `approval` capability (`request`, `suggest`, `approved`, `approval_needed`) and domain outcomes that go to their domains (`failed`, the estate, request and quiddity vocabularies). It bears on both open questions above and on survey ruling R4; the owner questions are 3, 12, 13, 14 and 15 of the label handoff. Nothing in this domain was changed by it.

## Related Artifacts

- [`README.md`](README.md)
- [`../../economics/transaction/transaction.handoff.md`](../../economics/transaction/transaction.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Bookkeeping domain (Status bullet) (2026-09-16 migration).
