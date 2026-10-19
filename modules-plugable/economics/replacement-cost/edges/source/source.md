# Source

## Model

- `(product)-[:source]->(product)` — this product is replenished by obtaining that product: a bought product points at the supplier's product, and a landed cost points at a service product (transport, customs).
- Fields:
  - `Quantity()` (decimal) — how many units of the source product one unit of this product takes: `0.001` when buying per ton and selling per kilogram, `1/12` when buying a carton of twelve and selling one.
  - `Group()` — sources in one group are alternatives for the same input (several suppliers), of which one is chosen; separate groups are summed (the goods, then transport, then customs).

## Policies (rules)

- Created, changed, and removed only by the organization that owns the subject product. It is the buyer's statement of where it replenishes from.
- A source edge toward another organization's product implies the buyer's [follow](../../../../../modules/identity/thing/edges/follow/follow.md) of that product's [price](../../../../../modules/economics/product/edges/price/price.md) edge, so the supplier is asked: its authorization rule admits, limits, or refuses the follow, and its accounting rule may charge for each delivered price version. A supplier that refuses or later revokes the follow delivers no price; the source still states where the product is replenished from, and the product's replacement cost falls back to [quotes](../quote/quote.md).
- Creating or removing the edge, or changing `Quantity` or `Group`, re-evaluates the subject product's [replacement cost](../../replacement-cost.md).
- A new version of the source product's price, delivered through the follow, re-evaluates every product pointing at it, transitively up through [material](../../../good/edges/material/material.md) edges. This is the automatic part of dealing with sellers: their price change reaches the buyer without anyone re-entering it, under the supplier's authorization and accounting.

## Placement

- **Here, not core `product`:** a product stays priceable without it, and an organization that never evaluates replacement cost removes it with this capability.
- **Named for the relation, not for its first reader:** "where this product is replenished from" is what procurement and inventory reordering also need, and they read this edge rather than define their own.
- **The procurement reading of [supplier](../../../../../modules/economics/product/edges/supplier/supplier.md):** that document's candidate reading 2 asks for a pluggable procurement capability only once processing beyond product nodes and rules is needed. Re-evaluation on a source's price event is that processing. Whether the two are one relation is open in the module's [Unresolved questions](../../replacement-cost.md#unresolved-questions).
- **Not material:** material is what a made product consists of (physical composition, in `good`); source is where a bought product comes from. A product may carry both.
- **The price arrives through thing's follow:** delivering the supplier's price, authorizing it, and metering it belong to [follow](../../../../../modules/identity/thing/edges/follow/follow.md), not to this edge, which states only where from and in what quantity.

## Open questions

- Which price is read when the supplier prices per buyer: its public price, or the price its pricing rules give this buyer?
- Is the follow created with the first source edge toward a product and removed with the last, or does the buyer create and remove it on its own?
