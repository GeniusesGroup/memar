# Pricing Changelog

## Changelog

### Prices derived from current stated prices, not the historical cost of stock held
- Time: 2026-10-10T11:50:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- [edges/pricing](edges/pricing/pricing.md#decisions-2026-10-10) records the decision: a price is derived from current stated prices in the graph, evaluated as [replacement cost](../replacement-cost/replacement-cost.md), never from the purchase invoices of stock held. Where money loses value, a unit bought for 2000 whose replacement costs 3000 is not sold from 2000, for producers and trading organizations alike. Nothing in the tree stated a basis before; the only cost-to-price chain, batch cost with markup, named none.
- `product` → `price`, `invoice` → `item`, `batch` → `cost`, and `product` → `supplier` link the decision where they touch it.
- Which edge carries a rule-stated sale price is recorded as open beside the decision.

#### Considered and not done
- Pricing from the last purchase invoice, or from FIFO or weighted-average cost — not taken: each is history, and under inflation each lags today's cost by the time the stock is held.

### Research on who owns a price; the owner's batch position recorded as open
- Time: 2026-10-10T13:50:00Z
- Type: added
- Cited:
  - [Pricing Research 001](pricing.research.001.md) - Evidence: scenarios, candidate models, and the owner's questions behind the extended open bullet
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - An AI agent in Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- [pricing.research.001.md](pricing.research.001.md) is added: who owns a sale price — product, batch, or a general supply instance — and on what basis a price is displayed. It works ten scenarios and four candidate models, and ends in a recommendation the owner has not ratified and the questions only the owner can decide.
- The open bullet in [edges/pricing](edges/pricing/pricing.md#decisions-2026-10-10) now records the owner's position that a price belongs to the batch of goods, not to the product, with the analogue for services unsettled, and links the research. The decided bullet is unchanged.

### The open item moved to Open questions; price-ownership questions
- Time: 2026-10-10T14:20:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the audit
  - An AI agent in Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — audited and drafted

#### What changed
- The open bullet under Decisions (2026-10-10) in [edges/pricing](edges/pricing/pricing.md#open-questions) moved, unchanged in substance, to a new Open questions section, where [Modules → Edge folder](../../../modules/modules.md#edge-folder) keeps an edge's uncertain notes. The links to it in [replacement-cost](../replacement-cost/replacement-cost.md), [pricing.research.001.md](pricing.research.001.md), and invoice [item](../../../modules/economics/invoice/edges/item/item.md) follow it.
- Two questions were added: how an invoice item holds the price it was issued at, answered unratified, and what a replacement-cost source or an index component points at and follows if a price moves to the batch.

### The pricing edge states who attaches it and what it triggers; lessons added as questions
- Time: 2026-10-10T14:45:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided the lessons
  - An AI agent via Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- [edges/pricing](edges/pricing/pricing.md#policies-rules) gains Policies (rules), so it is no longer a bare edge: only the product's owner attaches and removes a rule, through `process_pricing_for`; the rule is evaluated on `replacement_cost_changed` and `price_index_divergence`; a price it states is a new version that references its inputs and triggers delivery to followers and re-evaluation of the replacement costs and indices that read it. What the rule does on an event is the organization's policy.
- [edges/pricing](edges/pricing/pricing.md#placement) gains Placement: pluggable rather than core product; not replacement cost or price index, which discover values; not invoice-level; attached on the product, with where its output lands still open.
- Three Open questions were added to [edges/pricing](edges/pricing/pricing.md#open-questions): what removing a rule's attachment leaves of the price it stated; whether the `count_unit` endpoint carries the product's display basis (compound units, or a state such as "on request"); and whether a rule-stated price carries a valid-until.
- [pricing.md](pricing.md) now points to the open questions on who owns a price and on what basis it is shown, and to [Pricing Research 001](pricing.research.001.md).
- The same lessons were added, each linking back here, to `money`, `batch`, `inventory`, `good`, `production`, `service`, `discount`, `vat`, `credit`, `settlement`, `matching_system`, `analytics`, and `refund`, each recorded in its own changelog.
