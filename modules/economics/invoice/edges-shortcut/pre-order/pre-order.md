# Invoice pre-order
A [pre-order](https://en.wikipedia.org/wiki/Pre-order) is an order placed for an item that has not yet been released.

## Model

- `(invoice)-[:pre_order]->(___)`
- `(time{future})<-[:shipped_in]-(invoice)-[:invoice_item]->(product)-[:produced_in]->(time{future})`

## Policies (rules)

## Fields

## Open questions

- A pre-order keeps its issue-date price until its product exists: does it carry a price-validity window, and what follows when the window passes — [expired](../../status/expired/expired.md), or a new price agreed?
- Paid later or in instalments, a pre-order is a deferred-payment sale, the owner's case of pre-sold apartments paid years later at a fraction of their cost: which warning and which indexed instalments apply — [deferred-payment sales](../../../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales)?
- A pre-order sent to another organization is an exchanged invoice its seller may reject on a price mismatch — [invoice exchange](../../invoice.handoff.md#open-questions).
