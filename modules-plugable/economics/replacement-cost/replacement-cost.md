# Replacement Cost

Replacement cost is what an organization would pay today to obtain one more unit of a product it sells: the current stated price of what it buys that product from, or of what it makes it out of. Where money loses value faster than stock turns over — the Iranian rial, where steel and by now most goods are repriced daily — a sale price derived from the purchase invoice of stock already held sells each unit below the cost of replacing it, and the organization shrinks in real terms while its books show a profit. This module derives a product's replacement cost from prices already stated in the graph and announces every change, so that a [pricing](../pricing/pricing.md) rule can set the sale price from it. It never sets a price itself.

## Model

- Replacement cost is discovered, never acquired: it is computed from acquired facts and nobody states it by hand. Its inputs are:
  - the current version of a source product's [price](../../../modules/economics/product/edges/price/price.md), stated by the organization that owns that product — for a bought product, the supplier ([source](edges/source/source.md)) — and delivered to the buyer through its follow of that price. The price storage already keeps versions per product and currency (`modules/economics/product/edges/price/protocol/storage.kh`);
  - a [quote](edges/quote/quote.md), where what is bought has no product in the graph;
  - for a made product, its [material](../good/edges/material/material.md) quantities, each material valued at its own replacement cost.
- Evaluation:
  - a bought product: the sum over its source groups of `Quantity` × the current price (or latest valid quote) of the source chosen in that group. Sources in one group are alternatives — several suppliers of the same input — and one is chosen; separate groups are summed, which is how landed costs (transport, customs, insurance) enter: a service product with its own price, in a group of its own;
  - a made product: the sum over its materials of `BaseQuantity` × the material's replacement cost, plus conversion cost (open);
  - a product with no source, quote, or material has no replacement cost and is stale.
- Every value carries its as-of, the time of the oldest acquired input it was computed from, and the list of input versions it was computed from: the source price versions, quotes, and material edges.
- Event: `replacement_cost_changed` (product, new value, as-of, input versions), raised when an input changes — a new price version on a source product, a purchase of a source product at the price agreed at its issue ([invoice exchange](../../../modules/economics/invoice/invoice.handoff.md)), a new or retracted quote, a changed material or source edge. The product kernel does not know this module.

## Policies (rules)

- The historical cost of stock held is never the basis of a price — decided in [pricing](../pricing/edges/pricing/pricing.md#decisions-2026-10-10); this module is how that decision is evaluated.
- This module never writes a product's price. A pricing rule attached by `(rule)-[:process_pricing_for]->(product)` reacts to `replacement_cost_changed` and states the new sale price, referencing the input versions the replacement cost was computed from, so the price stays traceable to acquired facts. Which edge, and which node — product or batch — carries a rule-stated sale price is open in [pricing](../pricing/edges/pricing/pricing.md#open-questions). Replacement cost stays per product either way, because it is the cost of obtaining another unit, whichever batch that unit joins. What the rule does is the organization's policy: apply at once; apply only past a threshold of change; apply at a set time of day; send the change to a staff member for approval; whether a fall in replacement cost lowers the price.
- Staleness: an organization sets a maximum age per product or per product group. When a product's as-of is older than that, the product is stale: its replacement cost is reported with that mark, and a pricing rule may refuse to sell it or request a fresh quote. This is what makes a six-month-old purchase unusable as a price basis.
- Propagation between organizations is automatic once the supplier admits it, through the [follow](../../../modules/identity/thing/edges/follow/follow.md) a [source](edges/source/source.md) edge implies; what the supplier may admit, charge for, refuse, or revoke, and the fallback to quotes, are that edge's policies. When the supplier states a new price, every buyer whose follow it admits receives it and is re-evaluated; no buyer re-enters a supplier's price. The same holds one level up: this organization's new price reaches its own trading customers' replacement cost under its own rules.
- Evaluation refuses a cycle through material or source edges and reports the product where the cycle closes.

## Placement

- **Pluggable, not core `product`:** a product stays priceable through its price edge alone, and an organization working in stable money removes this capability whole.
- **Not a pricing module:** pricing modules decide a price, which is policy; this module computes a cost basis, which is a discovered value. Several pricing rules (markup, threshold, approval) and analytics (inventory valuation) read the same value, so it is computed once here rather than once per reader.
- **Not batch [cost](../batch/edges/cost/cost.md):** batch cost records what a produced lot actually cost, which is accounting history; replacement cost is what producing or buying it again costs today. Which of the two the batch's Markup/Margin chain starts from is stated in [cost](../batch/edges/cost/cost.md).
- **Existing relations are reused:** price (product) and material (good). Only `source` and `quote` are added, the two acquired facts the graph lacked.
- **The value is not stored by default.** If evaluation has to be cached, the cache is an `edges-shortcut/` whose document names `source`, `quote`, `material`, and the price edge as the edges it recomputes from.

## Discussion

### Drawbacks

- It depends on suppliers keeping their prices current in the graph and admitting their buyers' follows, which they may charge for. A supplier outside the graph has to be tracked through quotes, which are manual work or a feed.
- Sale prices change as often as their inputs. In an inflationary market this is the fact itself made visible, but customers see it.
- Replacement cost is not the accounting cost of goods sold. Every report has to say which of the two it uses.

### Rationale and alternatives

- Pricing from the last purchase invoice of stock held — rejected: an invoice is history, and the gap between it and today's cost grows with every day the stock is held. That gap is the loss this module exists to prevent.
- Pricing from weighted-average or FIFO cost — rejected for pricing, kept for accounting: both lag further behind than the last purchase does.
- A replacement-cost field that purchasing staff edit — rejected: a discovered value stated by hand loses the inputs it came from and cannot be recomputed when one of them changes.
- Pegging a sale price automatically to a single reference (a foreign currency, gold) — not this module's basis: the owner does not want a price tied automatically to one reference. Judging a price against a basket the organization chooses and can change is the [price-index](../price-index/price-index.md) module, which a pricing rule may read beside replacement cost.

### Prior art

- NIFO (next-in, first-out) costs a sale at the replacement cost of the next unit to be bought. Businesses use it internally to set prices during inflation, outside GAAP, while reporting under FIFO or LIFO ([Investopedia](https://www.investopedia.com/terms/n/next-in-first-out.asp), [CFI](https://corporatefinanceinstitute.com/resources/accounting/next-in-first-out-nifo/)).
- IAS 29, *Financial Reporting in Hyperinflationary Economies*, applies to Iran as of June 2026, with a three-year cumulative inflation of 216% to March 2026 ([EY](https://www.ey.com/content/dam/ey-unified-site/ey-com/en-gl/technical/ifrs-technical-resources/documents/ey-gl-ifrs-developments-249-hyperinflationary-economies-04-2026.pdf)). IAS 29 restates financial statements and sets no price; this module is the management-side counterpart.
- Price-adjustment (escalation) clauses in long contracts tie a contract's price to a stated index. That is contract-level indexing; here the same effect comes from sources and quotes with a validity.

### Unresolved questions

- Conversion cost of a made product (labour, overhead): taken from the batch cost shares, from current payroll rates, or from service products as sources?
- A service sold by time and place (a barber's slot of staff × place × time; [Pricing Research 001](../pricing/pricing.research.001.md#a-barber-charging-by-time-and-place)): does it have a replacement cost — the staff's current rate for the expected duration plus the place's current cost for that time — or no replacement cost, priced by rule alone?
- A source priced in a different currency from the sale: is a party's currently stated offer to sell a currency — an ask on [trade](../matching_system/edges/trade/trade.md) — a price a source may point at? How a currency's price is represented has to respect the money model, in which money, if debt-based, is to be modeled precisely; the same question is open for currency components in [price-index](../price-index/price-index.md#unresolved-questions). Until answered, a cross-currency source is refused.
- Within a source group, which alternative is chosen (preferred, lowest, highest, most recently stated), and is that choice configuration of this module or a pricing rule?
- Converge [source](edges/source/source.md) with the product-side [supplier](../../../modules/economics/product/edges/supplier/supplier.md) candidate: one relation, which this module and procurement both read, or two?
- Does the staleness mark belong to this module or to each pricing rule?
- When the alternatives in one source group are stale at different times, is the group stale only when every alternative is, or as soon as the chosen one is?
- Which reports read replacement cost and which read historical cost — cost of goods sold, inventory valuation, the IAS 29 restatement, holding-gain analytics — and is the basis a report uses a field of the report, so that no report shows one as the other?
- Under replacement-cost pricing, is VAT computed on the invoiced sale price as for any sale, and is income tax assessed on the profit over historical cost, so that the holding gain (see Future possibilities) is taxed as profit though it buys no more stock? Which Iranian tax rules apply, and whether the module must show the tax due on that gain, is for a session that reads them.
- Do Iranian consumer-protection rules, or a government price cap or registered price on a product, limit raising the price of stock already held to its replacement cost? If so, is that limit a rule attached through `condition_is` that refuses or warns, and which module owns it?
- The sale side: an issued but unpaid invoice or a pro-forma keeps the price of its issue date. Does it expire within the organization's price-validity window ([expired](../../../modules/economics/invoice/status/expired/expired.md), the reserve validity in [item](../../../modules/economics/invoice/edges/item/item.md))? A deferred-payment sale is paid in money worth less than at issue; its warning, its indexed instalments, and where their rules attach are in [price-index → Deferred-payment sales](../price-index/price-index.md#deferred-payment-sales). Open here: may a deferred-payment warning or instalment also read the product's replacement cost at each due date, beside an index?

### Future possibilities

- Holding-gain analytics: the sale price less replacement cost is the operating margin, and replacement cost less the historical cost of the unit sold is the holding gain that inflation produced. Shown apart, they reveal the real profit. This is analytics, filed under the economics analytics namespace when built.
- Automatic request for quote: when a product turns stale and its source has no product in the graph, open a task with the [negotiation](../../../modules/management/task/edges/negotiation/negotiation.md) label to the supplier.
- Market feeds: a commodity exchange's price for steel, cement, or the like, received by an authorized integration as quotes or as a source product's price.
