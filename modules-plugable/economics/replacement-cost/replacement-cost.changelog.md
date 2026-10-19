# Replacement Cost Changelog

## Changelog

### Module proposed
- Time: 2026-10-10T11:50:00Z
- Type: created
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested; the module is proposed and awaits review

#### What changed
- [replacement-cost](replacement-cost.md) evaluates a product's replacement cost from its suppliers' current prices, from quotes, and from its materials. It raises `replacement_cost_changed`, to which a pricing rule reacts, and it never writes a price itself. It adds two edges, [source](edges/source/source.md) and [quote](edges/quote/quote.md), and reuses `price` and `good` → `material`.
- A reviewer sub-agent that had not seen the work checked links, placement, and modeling; its findings were applied, and the questions that need the owner are in the module's Unresolved questions.

#### Considered and not done
- Putting the evaluation inside `pricing` or `batch` — not taken: it is one discovered value read by several pricing rules and by analytics, while batch cost records accounting history.

### Owner's corrections and answers
- Time: 2026-10-10T13:50:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- The reasoning against pegging a price to a currency or gold was wrong. It said pegging was not taken because [money](../money/money.md) rejects exchange rates as stored facts; that statement concerns the design of the project's own currency — not repeating the mistake of a gold standard pegged through the US dollar, and modeling money precisely if it is debt-based — and is no reason about pricing. The [Rationale and alternatives](replacement-cost.md#rationale-and-alternatives) bullet now gives the owner's own reason: he does not want a sale price tied automatically to a single reference. Judging a price against a basket the organization chooses is the new [price-index](../price-index/price-index.md) module. The cross-currency question no longer cites money as the reason, and states only that a currency's price has to respect the money model.
- A purchase is an event: a purchase between two organizations is one invoice that reaches every involved organization, issued at the seller's current price, and the seller rejects one registered at an old price as a process error. A purchase re-evaluates replacement cost, and the price is agreed at issue. The open question on recording a fresh purchase as a quote, here and in [quote](edges/quote/quote.md), is narrowed to a supplier truly outside the graph.
- The sale-side question on deferred payment links to [price-index → Deferred-payment sales](../price-index/price-index.md#deferred-payment-sales) and records the owner's position: no method can be forced on an organization; modules have to help it see the problem and choose.
- The policy on which edge carries a rule-stated sale price records the owner's leaning: price belongs to the batch, with an analogue for services, not to the product. Replacement cost stays per product, because it is the cost of obtaining another unit.

### A supplier's price reaches the buyer through follow
- Time: 2026-10-10T14:10:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- [source](edges/source/source.md) no longer says the source product's owner is neither asked nor told. A source edge toward another organization's product implies the buyer's [follow](../../../modules/identity/thing/edges/follow/follow.md) of that product's price edge, under the supplier's authorization and accounting; the supplier may admit, limit, charge for, refuse, or revoke it, and a refused or revoked follow leaves the product's replacement cost to [quotes](edges/quote/quote.md). Its Placement says delivery, authorization, and metering belong to follow, and its Open questions ask whether the follow is created and removed with the source edges.
- [replacement-cost.md](replacement-cost.md)'s propagation policy, its Model line on the source price, and its drawback on suppliers say the same.

### The module audited: one home per statement, questions for separate sessions
- Time: 2026-10-10T14:20:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the audit
  - An AI agent in Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — audited and drafted

#### What changed
- [replacement-cost.md](replacement-cost.md)'s propagation policy points at [source](edges/source/source.md)'s policies instead of restating them; the owner's batch leaning is left to [pricing](../pricing/edges/pricing/pricing.md#open-questions), whose open item now sits in its Open questions; which cost the batch's Markup/Margin chain starts from is left to batch [cost](../batch/edges/cost/cost.md).
- Questions asked in two homes now have one: converging with supplier and the choice within a group stay in the module; the price read when a supplier prices per buyer stays in source; recording a fresh purchase as a quote stays in [quote](edges/quote/quote.md). That a purchase re-evaluates replacement cost at the price agreed at issue is in the Model's event line, linked to invoice exchange.
- A supplier outside the graph is "tracked", not "followed", through quotes, so that "follow" names only thing's relation.
- New Unresolved questions: staleness within a source group, which reports read which cost basis, VAT and income tax under replacement-cost pricing, Iranian consumer-protection rules or price caps, and replacement cost at each due date of a deferred-payment sale.

### A service's replacement cost asked
- Time: 2026-10-10T14:45:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided the lessons
  - An AI agent via Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- The [Unresolved questions](replacement-cost.md#unresolved-questions) gained one: whether a service sold by time and place — a barber's slot of staff × place × time — has a replacement cost from the staff's current rate and the place's current cost, or none, priced by rule alone.

#### Surveyed
- The module was checked against the lessons of the 2026-10-10 pricing session: the price basis, staleness and validity, the accounting and holding-gain split, tax basis and price caps, and the representation of a currency's price are already held in its Policies, Unresolved questions, and Future possibilities. Only the service case was missing.
