# Quote

## Model

- `(product)-[:replacement_quote]->(count_unit)` — a price for obtaining this product, stated by someone outside the graph and recorded by the product's owner. Fields: amount, quantity and the unit it was quoted in (a per-ton quote stays per ton; evaluation converts it), quoted by (the supplier's name or organization), recorded at, valid until.

## Policies (rules)

- Created by the owning organization's staff in a purchasing role, or by an integration that organization authorizes (a market-price feed).
- Never edited or deleted: a newer quote is a new fact, and the latest valid one is the input. A mistaken quote is retracted by a new fact that references it, recorded by the same roles; the retraction re-evaluates the product as a new quote does.
- A quote past its valid-until, or older than the product's maximum age, is not an input, and the product turns stale.
- Creating or retracting a quote re-evaluates the product's [replacement cost](../../replacement-cost.md).
- A quote is not an invoice: an invoice records a purchase that happened; a quote records what buying now would cost.
- Each quote is its recorder's own observation: two buyers recording the same supplier hold two observations, not one fact twice.

## Placement

- **Here:** an acquired fact this module consumes and nothing else reads.
- **Not the product's [price](../../../../../modules/economics/product/edges/price/price.md):** a price is stated by a product's owner for selling it; a quote is a third party's selling price recorded by the buyer.

## Open questions

- Should a supplier outside the graph rather be registered as its own organization with its own product node, so that its price is a price edge and a [source](../source/source.md) points at it, leaving this edge for one-off offers only?
- A purchase between two organizations re-evaluates replacement cost as an event, at the price agreed at its issue ([invoice exchange](../../../../../modules/economics/invoice/invoice.handoff.md)), and needs no quote. Still open: may a fresh purchase from a supplier truly outside the graph be recorded as a dated quote, under the same maximum age, so that it is evidence of today's price rather than the historical cost of stock held?
- Who authorizes a feed integration, and is its quote distinguishable from one a staff member recorded?
