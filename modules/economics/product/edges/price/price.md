# Price

## Model

- `(product)-[:price]->(count_unit)`

## Policies (rules)

- It is very simple pricing mechanism, for more professional pricing MUST use `pricing` module
- Never read back from an invoice: see the [pricing decision](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#decisions-2026-10-10).
- Created only by the organization that owns the product ([data_model.kh](protocol/data_model.kh)); another organization reads it through a [follow](../../../../identity/thing/edges/follow/follow.md) and never writes it.
- Never overwritten and never deleted: a change is a new version, kept per product and currency ([storage.kh](protocol/storage.kh)), as [state change is modeled as events](../../../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates).
- Each new version triggers one delivery to each follower whose scope names this edge ([follow](../../../../identity/thing/edges/follow/follow.md#policies-rules)), re-evaluation of the [replacement cost](../../../../../modules-plugable/economics/replacement-cost/replacement-cost.md) of every product whose [source](../../../../../modules-plugable/economics/replacement-cost/edges/source/source.md) points at this product, and recomputation of every [price index](../../../../../modules-plugable/economics/price-index/price-index.md) that has this product as a [component](../../../../../modules-plugable/economics/price-index/edges/component/component.md) — an edge states who creates it and what it triggers ([no bare edges](../../../../modules.md#placement)).

## Placement

- **On product, for now:** a product is the unit of priceability ([product](../../product.md)); the owner's leaning is that a price belongs to the batch, not the product, and price and pricing are not finished — open below.
- **Not pricing:** this edge holds a price its owner states; a price a rule derives is [pricing](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md)'s work, and which edge carries it is open below.
- **Not the invoice item's price:** an item holds the price it was issued at as its own fact, referencing the version of this edge it came from ([pricing open questions](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#open-questions); answered 2026-10-10, unratified).

## Open questions

- Does a price belong to the product or to the batch? The owner leans to the batch; what plays the batch's part for a service (a barber charging by time and place; a slot of staff × place × time) is unsettled — [Pricing Research 001](../../../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions).
- Is a sale price stated by a rule reacting to `replacement_cost_changed` or `price_index_divergence` written into this edge on the owner's behalf, or carried by `(product)-[:pricing]->(count_unit)`? — [pricing open questions](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#open-questions).
- Must every product show a price? May a product instead declare a display basis — a [count unit](../../../../identity/thing/edges/count_unit/count_unit.md), compound where needed (kg·km, t·km, passenger-km, per hour, per month), or a state ("on request", "negotiable", "market") — [Pricing Research 001](../../../../../modules-plugable/economics/pricing/pricing.research.001.md#must-every-product-show-a-price)?
- Does a stated price version carry a valid-until, as a [quote](../../../../../modules-plugable/economics/replacement-cost/edges/quote/quote.md) does, and how old may it be before a buyer's replacement cost marks it stale ([replacement cost policies](../../../../../modules-plugable/economics/replacement-cost/replacement-cost.md#policies-rules))?
