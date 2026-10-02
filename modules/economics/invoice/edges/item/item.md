# Item

## Model

- Candidate (unconfirmed): `(invoice)-[:invoice_item]->(product)`
- Candidate (unconfirmed): `(product)-[:Added_to_invoice]->(invoice)`

## Policies (rules)

- "Ship service can add as an item to invoice" — a ship service may be sold as a line of the invoice.
- "Each item must check for reserve validity and make action in end of validity" — every item is checked against reserve validity, and an action is taken when validity ends.

## Placement

- **Verdict: the structural edge stays in core `invoice`; the semantics named in the source comment belong to the rule domain; no dedicated module.** Invoice is core-by-necessity — without `(invoice)-[:invoice_item]->(product)` the kernel cannot state what it delivered — but the comment's processing ("check for reserve validity and make action in end of validity") is policy: when the action fires is organization policy inside the Rule, not kernel behavior (Core never knows Rule, owned in [rule.handoff.md](../../../../computer/rule/rule.handoff.md); its §9: fees and charges are rules producing transactions). The generic attachment already filed in this folder is [conditional](../conditional/conditional.md) — attach validity-end actions there; if instead expiry is item state, it surfaces in [status/expired](../../status/expired/expired.md), whose review question asks exactly what sets expiry.
- "Ship service can add as an item" needs no module: what may be a line item is content/configuration of the one item edge, not a processing-semantics difference (parameters vs semantics ⇒ one item edge, configuration decides the kinds).
- The DataModel price chain (Suggested/Discounted/Rule/Payable) is deferred to the dedicated data-model pass ([invoice.md](../../invoice.md) backlog note); `RulePrice` naming stays open in [invoice.handoff.md](../../invoice.handoff.md), and professional pricing is out of the kernel ([product price](../../../product/edges/price/price.md) ⇒ `pricing` module).

## Open questions

- Is reserve-validity expiry a rule (expiry rules producing transactions, per [rule.handoff.md](../../../../computer/rule/rule.handoff.md) §9) or item state?

## Source

> Source: `modules/economics/invoice/edges/item/protocol/data_model.kh` (in code).
