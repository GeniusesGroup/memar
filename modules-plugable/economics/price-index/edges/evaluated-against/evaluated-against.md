# Evaluated Against

## Model

- `(product)-[:evaluated_against]->(price_index)` — the product's owner tracks this product's price relative to the index.
- Fields:
  - Threshold (optional) — how far the relative series may move from its value at the index's base date before a divergence is raised, as a percentage either way.
- The relative series is discovered: the product's price version in force at `t` divided by the index value at `t`, scaled to 100 at the index's base date. Nobody states it.

## Policies (rules)

- Created, changed, and removed only by the organization that owns the product, and only toward an index it owns or [follows](../../../../../modules/identity/thing/edges/follow/follow.md).
- Creating the edge starts the relative series; a new price version on the product or a `price_index_changed` on the index recomputes it.
- When the relative series crosses the threshold, the module raises `price_index_divergence` (product, index, relative value, as-of, input versions). A [pricing](../../../pricing/pricing.md) rule attached to the product, or a staff member it is routed to, may react; the event itself changes no price.
- Removing the edge ends the relative series from that time; past divergence events stay as facts.

## Placement

- **Here, not on `product`:** a product is priced without any index, and an organization in stable money removes this capability whole.
- **Here, not in pricing:** the edge produces a discovered series and an event; what to do about a divergence is a pricing rule's policy.

## Open questions

- Is the threshold measured from the base date, or over a rolling window (the movement in recent months)?
- May one product be evaluated against several indices, each with its own threshold, and is one divergence event raised per index?
