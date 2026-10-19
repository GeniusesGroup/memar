# Item

## Model

- Candidate (unconfirmed): `(invoice)-[:invoice_item]->(product)`
- Candidate (unconfirmed): `(product)-[:Added_to_invoice]->(invoice)`

## Policies (rules)

- "Ship service can add as an item to invoice" — a ship service may be sold as a line of the invoice.
- "Each item must check for reserve validity and make action in end of validity" — every item is checked against reserve validity, and an action is taken when validity ends.
- A purchase invoice's item is history, never the basis of a later sale price: see the [pricing decision](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#decisions-2026-10-10). Which product edge a sale item copies its price from, and how the item holds it, are in pricing's [Open questions](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#open-questions).

## Placement

- **Verdict: the structural edge stays in core `invoice`; the semantics named in the source comment belong to the rule domain; no dedicated module.** Invoice is core-by-necessity — without `(invoice)-[:invoice_item]->(product)` the kernel cannot state what it delivered — but the comment's processing ("check for reserve validity and make action in end of validity") is policy: when the action fires is organization policy inside the Rule, not kernel behavior (Core never knows Rule, owned in [rule.handoff.md](../../../../computer/rule/rule.handoff.md); its §9: fees and charges are rules producing transactions). The generic attachment already filed in this folder is [conditional](../conditional/conditional.md) — attach validity-end actions there; if instead expiry is item state, it surfaces in [status/expired](../../status/expired/expired.md), whose review question asks exactly what sets expiry.
- "Ship service can add as an item" needs no module: what may be a line item is content/configuration of the one item edge, not a processing-semantics difference (parameters vs semantics ⇒ one item edge, configuration decides the kinds).
- The DataModel price chain (Suggested/Discounted/Rule/Payable) is deferred to the dedicated data-model pass ([invoice.md](../../invoice.md) backlog note); `RulePrice` naming stays open in [invoice.handoff.md](../../invoice.handoff.md), and professional pricing is out of the kernel ([product price](../../../product/edges/price/price.md) ⇒ `pricing` module).

## Open questions

- Is reserve-validity expiry a rule (expiry rules producing transactions, per [rule.handoff.md](../../../../computer/rule/rule.handoff.md) §9) or item state?
- How does an item hold the price it was issued at? As its own fact: the amount, the count unit, and a reference to the stated [price](../../../product/edges/price/price.md) version it came from, never re-read afterwards ([pricing open questions](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#open-questions); answered 2026-10-10, unratified).
- An issued-but-unpaid item keeps its issue-date price while prices move: does reserve validity also bound how long that price holds, so that the item, or the invoice ([expired](../../status/expired/expired.md)), expires when a price-validity window passes?
- When the invoice crosses organizations, which organization's product does an item reference, and does the item or the buyer's replacement-cost source record the mapping between the two identifiers? — [invoice exchange](../../invoice.handoff.md#open-questions).

## Source

> Source: `modules/economics/invoice/edges/item/protocol/data_model.kh` (in code).
