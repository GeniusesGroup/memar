# Component

## Model

- `(price_index)-[:component]->(product)` — this product is one item of the index's basket. The product is any thing with a price stated in the graph: a commodity such as silver or PVC, or a currency offered for sale by a dealer or an exchange.
- Fields:
  - `Quantity()` (decimal) — how many units of the product the basket holds: `0.5` kilograms of silver, `10` kilograms of PVC. It is the component's weight in the index.
  - Valid from — the time this component, or this quantity, enters the basket.

## Policies (rules)

- Created, changed, and removed only by the organization that owns the index.
- A component toward another organization's product implies the index owner's [follow](../../../../../modules/identity/thing/edges/follow/follow.md) of that product's [price](../../../../../modules/economics/product/edges/price/price.md) edge, so the product's owner is asked: its authorization rule admits, limits, or refuses the follow, and its accounting rule may charge for each delivered price version. A follow the owner refuses delivers no price, so the component has no price version in force and the index has no value ([price index → Policies](../../price-index.md#policies-rules)).
- A change is a new fact, never an overwrite: a new quantity or a removal ends the earlier component version at its time and starts the next composition version, so every past index value is explained by the composition in force when it was computed.
- Creating, changing, or removing a component recomputes the index's series from the change onward and raises `price_index_changed` on the [price index](../../price-index.md).
- A new version of the component product's price, delivered through the follow when another organization owns the product, recomputes every index holding that product.

## Placement

- **Here, not on `product`:** the basket is the index owner's statement; a product is priced without knowing which baskets hold it.
- **Not [source](../../../replacement-cost/edges/source/source.md):** a source says where a product is replenished from and enters its replacement cost; a component says what an organization chooses to judge prices by.
- **The price arrives through thing's follow:** delivering another organization's price, authorizing it, and metering it belong to [follow](../../../../../modules/identity/thing/edges/follow/follow.md), not to this edge, which states only which product and in what quantity.

## Open questions

- May the target be another price index, so that baskets compose? If so, a cycle is refused.
- Should a weight stated as a share of the basket's value at the base date be accepted, converted to a quantity at the base date's prices?
- Is the follow created with the first component toward a product and removed with the last, across all the owner's indices, or does the index owner create and remove it on its own?
- When the product's owner revokes the follow, does the index keep computing from the last delivered price version, marked stale, or does its value become absent from the revocation's time?
- May an index owner replace a component whose follow is refused or charged too much by a quote-like observation it records itself, and is the index then marked as resting on its owner's observation?
