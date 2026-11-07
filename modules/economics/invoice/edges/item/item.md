# Item

## Model

- Candidate (unconfirmed): `(invoice)-[:invoice_item]->(product)`
- Candidate (unconfirmed): `(product)-[:Added_to_invoice]->(invoice)`

## Policies (rules)

- "Ship service can add as an item to invoice" — a ship service may be sold as a line of the invoice.
- "Each item must check for reserve validity and make action in end of validity" — every item is checked against reserve validity, and an action is taken when validity ends.
- A purchase invoice's item is history, never the basis of a later sale price: see the [pricing decision](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#decisions-2026-10-10).
- An item holds the price it was issued at as its own fact: the amount, the count unit, and a reference to the stated [price](../../../product/edges/price/price.md) version it came from, never re-read afterwards.

## Placement

- **Verdict: the structural edge stays in core `invoice`; the semantics named in the source comment belong to the rule domain; no dedicated module.** Invoice is core-by-necessity — without `(invoice)-[:invoice_item]->(product)` the kernel cannot state what it delivered — but the comment's processing ("check for reserve validity and make action in end of validity") is policy: when the action fires is organization policy inside the Rule, not kernel behavior (Core never knows Rule; fees and charges are rules producing transactions). The generic attachment already filed in this folder is [conditional](../conditional/conditional.md) — attach validity-end actions there; if instead expiry is item state, it surfaces in [expired](../../labels/expired/expired.md).
- "Ship service can add as an item" needs no module: what may be a line item is content/configuration of the one item edge, not a processing-semantics difference (parameters vs semantics ⇒ one item edge, configuration decides the kinds).
- Professional pricing is out of the kernel ([product price](../../../product/edges/price/price.md) ⇒ `pricing` module).

## Source

> Source: `modules/economics/invoice/edges/item/protocol/data_model.kh` (in code).
