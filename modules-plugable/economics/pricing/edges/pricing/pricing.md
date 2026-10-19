# Pricing

## Model

- `(product)-[:pricing]->(count_unit)` (note: rule)
- `(rule)-[:process_pricing_for]->(product)`

## Policies (rules)

- Attached and removed only by the organization that owns the product, through `(rule)-[:process_pricing_for]->(product)`: only that organization states the product's [price](../../../../../modules/economics/product/edges/price/price.md), so no organization attaches a pricing rule to another's product.
- Attaching starts evaluation: the rule is evaluated on `replacement_cost_changed` from [replacement cost](../../../replacement-cost/replacement-cost.md) and `price_index_divergence` from [evaluated-against](../../../price-index/edges/evaluated-against/evaluated-against.md) for the product it is attached to; neither event changes a price by itself. Which edge carries the output is open ([Open questions](#open-questions)).
- The rule starts from current stated prices, never from the historical cost of stock held ([decision](#decisions-2026-10-10)).
- A price the rule states is a new version, never an overwrite, and references the input versions it was computed from — the replacement cost's input versions, the index values it read — so it stays traceable to acquired facts.
- A price version the rule states triggers what any new price version triggers: delivery to the price's followers ([follow](../../../../../modules/identity/thing/edges/follow/follow.md)), re-evaluation of the replacement cost of every product whose [source](../../../replacement-cost/edges/source/source.md) points at it, and recomputation of every index holding it as a [component](../../../price-index/edges/component/component.md).
- What the rule does on an event — apply at once, past a threshold, at a set time, or route to a staff member for approval — is the owning organization's policy, as [replacement cost → Policies](../../../replacement-cost/replacement-cost.md#policies-rules) lists.

## Placement

- **Pluggable, not core `product`:** a product stays priceable through its price edge alone; a rule that decides a price is policy, attached per product, and an organization that states prices by hand removes this capability whole ([pricing](../../pricing.md)).
- **Not [replacement cost](../../../replacement-cost/replacement-cost.md) or [price index](../../../price-index/price-index.md):** those discover values and raise events; this module decides a price from them.
- **Not invoice-level:** an invoice-level adjustment changes an invoice's payable, not the product's price ([decision 2026-09-16](#decisions-from-organization-ideas-backlog-2026-09-16); [discount](../../../discount/discount.md)).
- **Attached on the product, output not yet placed:** the rule attaches to the product as the kind it prices; whether the price it states lands on the product or on a batch (the owner's leaning) is open ([Open questions](#open-questions)).

## Decisions from Organization ideas backlog (2026-09-16)

- **Pricing is a module family, not one module.** A transportation service's price varies by city, hour, route, zone, demand — hundreds of independently evolving pricing modules for one organization (Uber example), all attached to the Product level while invoice-level rules (zeroing a user's bill) are a *different* level: an Invoice-level rule making the payable zero does not make the service's price zero. *(decided)*

## Decisions (2026-10-10)

- **A price is derived from current stated prices, never from the historical cost of stock held.** The basis of a pricing rule is the price currently stated on a product in the graph — the supplier's own product for a bought product, the materials for a made one — evaluated as [replacement cost](../../../replacement-cost/replacement-cost.md). The purchase invoices of stock held record what was paid on their dates: they stay for accounting and audit and are never the basis of a price. Where money loses value, a unit bought for 2000 whose replacement now costs 3000 is not sold from 2000, however long it has been held. Applies to producers and to trading organizations alike. *(decided)*

## Open questions

- Which edge carries a sale price a rule states — the product's simple [price](../../../../../modules/economics/product/edges/price/price.md), written on the owner's behalf, or this module's `(product)-[:pricing]->(count_unit)` — and therefore which one an invoice item copies when the invoice is issued? The owner now holds that a price belongs to the batch of goods, not to the product; what plays the batch's part for a service (a barber charging by time and place, transport by weight and distance) is unsettled. The scenarios, the candidate models, and the questions only the owner can decide are in [Pricing Research 001](../../pricing.research.001.md).
- How does an invoice item hold the price it was issued at: re-read from the price edge, or as its own fact? As its own fact: the agreed price is acquired at issue and is the item's history, so the item records the amount, the count unit, and a reference to the stated price version (and, for a rule-stated price, the input versions) it came from, and never re-reads the price edge afterwards. (answered 2026-10-10, unratified)
- If the price moves to the batch, what does a buyer's replacement-cost [source](../../../replacement-cost/edges/source/source.md), or an index [component](../../../price-index/edges/component/component.md), point at and follow: the seller's product, with a price discovered from its batches, or a batch the buyer cannot know before it buys?
- When the owner removes a rule's attachment, does the last price the rule stated stand until the owner states another, or is it withdrawn with the rule?
- Does this edge's `count_unit` endpoint carry the product's display basis — a count unit, compound where needed (kg·km, passenger-km, per hour, per month) — or a state such as "on request", "negotiable", or "market" where no price is shown; and is a compound unit a count_unit node of its own? ([Pricing Research 001 → Open Questions](../../pricing.research.001.md#open-questions))
- Does a rule-stated price carry a valid-until, so that a price whose inputs passed their maximum age ([replacement cost → Policies](../../../replacement-cost/replacement-cost.md#policies-rules)) is withdrawn rather than left standing; and does an issued-but-unpaid invoice keep its issue-date price only within that window ([replacement cost → Unresolved questions](../../../replacement-cost/replacement-cost.md#unresolved-questions))?
