# Task relation invoice

## Model

- Candidate (unconfirmed): `(task)-[:relation]->(invoice)` (name/direction unconfirmed) carrying the label `Negotiation` — source was a label-only file, no edge code.

## Policies (rules)

- `Negotiation` — "for invoice price, ..." — price negotiation over the task's invoice.
- `invoices(CRM)` — CRM-flavored note on the relation.

## Placement

- **Correct here as recorded — the relation is the task's own edge file; the negotiation *semantics* (offers, acceptance, resulting price) are not task-kernel material** (module skeleton: `task/edges/`; prefer existing homes over inventing new modules).
- Price negotiation touches the invoice side: the structural link may stay task-side, but who may negotiate and what an accepted negotiation *does* (price change, new offer nodes) is policy/processing — price authority is rule material (core never knows Rule); invoice identity stays in [invoice](../../../../economics/invoice/invoice.md).
- CRM is a pluggable capability, never kernel — the `invoices(CRM)` note marks audience, not a CRM inside task.

## Open questions

- Does Negotiation produce invoice-state changes (rule → invoice status) or standalone offer content?
- One task-invoice edge with a Negotiation label, or a negotiation capability with its own nodes (parameters-vs-semantics)?
- Intersect the task-assignment/fee text in [task.md](../../task.md) ("specific fee") — is fee negotiation decided here or in pricing ([pricing](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md))?
- Direction/naming unconfirmed — nothing ratified.
- Is a negotiation the path after a seller rejects an exchanged invoice on a price mismatch ([invoice exchange](../../../../economics/invoice/invoice.handoff.md#open-questions)), and does an accepted negotiated price become a new version of the seller's stated [price](../../../../economics/product/edges/price/price.md), or only the price the invoice item holds as its own fact, leaving the price and the [pricing](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md) rules untouched?

