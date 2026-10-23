# Price Index

A price index is a basket of priced things that an organization defines for itself, together with the series of that basket's value over time, against which it judges a price. Pricing against a basket of assets is not a bad method; what matters is that the basket is the organization's own and can be changed. An organization selling solar panels, for example, knows the price its producer tells it, and besides that it wants to see that price against the US dollar's price in rial, the price of PVC, and the price of silver, so that it decides more transparently. The producer may follow the same basket. Building a basket and reading its parity chart is the same work as a ratio or relative-strength chart in capital-market technical analysis, and a basket can be shared. This module holds the basket, discovers its series from prices already stated in the graph, and announces divergence; it never sets a price itself.

It serves three uses:

1. A seller's decision aid: a product's own price is tracked against an index, and a [pricing](../pricing/pricing.md) rule or a staff member reacts when the two diverge.
2. A producer and its sellers judging by the same reference: the producer shares its index, and a seller follows it.
3. Deferred-payment sales, where a fixed amount paid later is the loss itself ([Deferred-payment sales](#deferred-payment-sales)).

## Model

- `price_index` — a vertex with its own identity, owned by the organization that defines it. Fields: name (a label), base date, and the count unit its series is read in (a currency).
- Its basket is its [component](edges/component/component.md) edges: each points at a product whose price is stated in the graph — a commodity such as silver or PVC, or a currency offered for sale by a dealer or an exchange — and carries a quantity. Whether another index may be a component is open in [component](edges/component/component.md#open-questions).
- The basket composition is acquired and versioned. Adding, changing, or removing a component is a new fact with its time; it never overwrites the earlier composition, so every past value of the index can be explained by the composition in force when it was computed.
- The series is discovered, never acquired: nobody states an index value by hand. The value at time `t` is the sum over the components in force at `t` of quantity × the component's [price](../../../modules/economics/product/edges/price/price.md) version in force at `t`, divided by the same sum at the base date, × 100. At the base date the index equals 100. The price storage already keeps versions per product and currency, which is what makes any past value recomputable.
- Every value carries its as-of, the time of the oldest price version it was computed from, and the list of component price versions and the composition version it was computed from.
- Event: `price_index_changed` (index, new value, as-of, input versions), raised when an input changes — a new price version on a component product, or a new composition version.
- A product is tracked against an index through [evaluated-against](edges/evaluated-against/evaluated-against.md); an organization other than the owner reads an index by following it through thing's [follow](../../../modules/identity/thing/edges/follow/follow.md), with the index's [component](edges/component/component.md) edges in its scope, and receives every composition version and `price_index_changed`.
- Charts — the index series, a product's price relative to an index, a basket's parity with another — are presentation of the series, not part of the model.

## Policies (rules)

- Only the owning organization defines an index and changes its basket; a follower reads it and never edits it.
- Sharing an index is admitting a [follow](../../../modules/identity/thing/edges/follow/follow.md) of it. The owner's visibility rule is that follow's authorization rule: an index the rule admits nobody to is private to its owner. The follower reads every composition version, not only the current one, so it sees what the index was made of when each value was computed; it reads the owner's index as the owner keeps it, not a snapshot. An index the follower follows may be the target of its [evaluated-against](edges/evaluated-against/evaluated-against.md) edges.
- This module never writes a product's price. A pricing rule attached by `(rule)-[:process_pricing_for]->(product)` may read an index value or react to `price_index_divergence`, and the price it states references the index values it read, so the price stays traceable to acquired facts.
- An index whose base date precedes a component's first stated price has no value until the owner moves the base date; a component with no price version in force at `t` makes the value at `t` absent, not zero.
- A component priced in a count unit other than the index's is refused until the question on currency components below is answered.
- Evaluation refuses a cycle through components and reports the index where the cycle closes, if indices are admitted as components.

### Deferred-payment sales

This project's owner pre-sold apartments; the money paid for them years later was worth, in effect, a tenth of what building them had cost him, and at the time he did not see the problem. A system cannot force an organization to use a particular method, but it can first make the problem visible and then offer the right method, and that is what this module is for here.

- At the approval of an invoice with deferred payment — instalments, post-dated cheques, a pre-sale — a rule may warn the approver that the product's price has moved strongly in recent months, so that a fixed-amount instalment is a poor method. The movement is discovered from the product's own price versions or from an index the product is evaluated against; which measure and which window is the rule's configuration.
- An organization may offer instalments whose amounts are indexed to a chosen price index: each instalment is its stated amount × the index value at its due date ÷ the index value at the invoice's issue.
- Where these rules attach is open: neither [credit](../credit/credit.md), which defers debt-based money to a dedicated chat, nor [settlement](../settlement/settlement.md), which is tiered bookkeeping, models deferred payment. The invoice's [conditional](../../../modules/economics/invoice/edges/conditional/conditional.md) attachment is the existing point at which an invoice rule attaches.

## Placement

- **Pluggable, not core:** a product stays priceable without any index, and an organization working in stable money removes this capability whole.
- **Not [money](../money/money.md):** money is how an amount is represented; an index is a reference an organization chooses for judging prices.
- **Not [replacement-cost](../replacement-cost/replacement-cost.md):** replacement cost is what obtaining another unit of a product costs through its sources; an index is a reference the organization chooses to judge a price against. A pricing rule may read both.
- **Not analytics only:** an index has its own identity, an owner, a composition lifecycle, and authorization for sharing. A query with its own types, events, storage, and processing is itself a pluggable module ([Modules → Placement](../../../modules/modules.md#placement)).
- **Not a pricing module:** pricing modules decide a price, which is policy; this module discovers a reference series and announces divergence.

## Discussion

### Drawbacks

- The basket is a judgment. A badly chosen basket misleads with the authority of a number, and the module cannot tell a good basket from a bad one.
- The series is only as current as its components' prices. A component whose owner stops stating prices, or refuses or revokes the index owner's follow of them, leaves the index stale.
- A chart invites reading a correlation as a cause; the index shows that two prices moved apart, not why.
- Indexed instalments move the risk of a falling currency from the seller to the buyer, and a buyer may refuse them.

### Rationale and alternatives

- Pegging a sale price automatically to one reference — a foreign currency or gold — is not this module's basis: the owner does not want a price tied automatically to any single reference. An index judges a price; a pricing rule or a staff member decides it.
- An index value that staff state by hand — rejected: a discovered value stated by hand loses the inputs it came from and cannot be recomputed when one of them changes.
- Editing a basket in place — rejected: past index values would no longer be explainable by the composition that produced them.
- Only official published indices, such as a consumer price index — not enough: an organization judges its own products by the inputs that matter to them, which no published basket chooses for it.

### Prior art

- Fixed-basket [price indices](https://en.wikipedia.org/wiki/Price_index) of the Laspeyres type, which value a basket chosen at a base period at later prices and set the base to 100, are the basis of most consumer price indices. The series here is the same formula over a basket the organization chooses.
- [Relative-strength](https://en.wikipedia.org/wiki/Relative_strength) or ratio charts in technical analysis divide one price by another or by an index to show how they move apart. A product tracked against an index is that chart.
- Index-linked contracts and [inflation-indexed bonds](https://en.wikipedia.org/wiki/Inflation-indexed_bond) adjust a payment by a stated index between agreement and payment. Indexed instalments here do the same with an index the seller chooses.

### Unresolved questions

- Currency components: how is the US dollar's price in rial represented as a priced thing? It has to respect the money model — money, if debt-based, is to be modeled precisely, and [credit](../credit/credit.md) defers that model — so whether a dealer's or an exchange's currently stated offer to sell a currency (an ask on [trade](../matching_system/edges/trade/trade.md)) is a price a component may point at is not decided here.
- When the basket changes, does the series continue by chain-linking — the new basket scaled to the old value at the change — or restart at 100 from a new base date?
- When the owner moves the base date, are past values restated against the new base as a new series version beside the old, and which version does a follower, or a contract that cites the index, read?
- Copying a followed index into an index of one's own (a fork): allowed, and does the copy keep a reference to the original's composition version?
- When the owner revokes a follow of an index, what happens to the follower's evaluated-against edges toward it?
- Does a follower of an index receive its series values as the owner computes them, or only its composition, computing the values itself through its own follows of each component's price under each component owner's authorization?
- May an owner admit everyone to follow its index, publishing it, and how does a reader tell a published private index from an official one such as a central bank's consumer price index?
- A shared index's owner can move its series by changing the basket or, owning a component product, that product's price. Must composition changes be announced before they take effect for followers, and how is such manipulation made visible to a follower?
- When two organizations name an index as a contract term — indexed instalments, a supply price — which composition version binds: the one in force at signing, frozen for the contract, or whatever the owner later makes it?
- Where deferred-payment rules attach — the invoice's conditional attachment, a pricing rule, or a deferred-payment capability of its own that owns instalments ([Deferred-payment sales](#deferred-payment-sales)).
- What measure and window does the deferred-payment warning use by default — the product's own price movement or an evaluated-against index, over how many months, past what percentage — and may an organization switch the warning off, or only change its threshold?
- Is an instalment indexed to an index the seller defines enforceable under Iranian law, and how is the buyer's consent to that index, and to the composition version in force at issue, recorded on the invoice?
- Must the seller admit the buyer's follow of the index its instalments are indexed to, for the term of the instalments? Yes: each amount owed is computed from that index, the price is agreed at issue between both parties, and a buyer that cannot read the index cannot verify what it owes; a seller that refuses that follow cannot offer the indexed method. (answered 2026-10-10, unratified)
- Does an index carry a maximum age for its component prices, as [replacement cost](../replacement-cost/replacement-cost.md#policies-rules) does per product, so that a value computed from a price version older than that is marked stale rather than shown as current, and is that age set by the index owner or by each follower?
- Pre-sale of real estate, the owner's own case: is the indexed amount tied to a construction-cost basket (steel, cement, labour) or to a general index, and does the pre-sale invoice's item point at an estate that does not exist yet, as a [pre-order](../../../modules/economics/invoice/edges-shortcut/pre-order/pre-order.md) does for a product?

### Future possibilities

- Published indices, such as an official consumer price index, received by an authorized integration, once their representation as a priced thing or a component is settled.
- Holding-gain analytics measured against an index as well as against [replacement cost](../replacement-cost/replacement-cost.md).
- A catalog of shared indices that organizations in one sector follow, so a producer and its sellers read the same reference by default.
