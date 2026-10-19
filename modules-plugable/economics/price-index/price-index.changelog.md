# Price Index Changelog

## Changelog

### Module proposed
- Time: 2026-10-10T13:50:00Z
- Type: created
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested; the module is proposed and awaits review

#### What changed
- [price-index](price-index.md) lets an organization define a basket of priced things — commodities, a currency offered for sale — with a base date at which the index equals 100. The series is discovered from the versions of its components' prices, and the basket composition is acquired and versioned, so every past value stays explainable. It adds three edges: [component](edges/component/component.md), [evaluated-against](edges/evaluated-against/evaluated-against.md), which follows a product's price against an index and raises `price_index_divergence`, and `follow`, which shares an index with another organization.
- It states the owner's case for deferred-payment sales: a rule may warn the approver of an invoice with deferred payment that the product's price has moved strongly, and instalments may be indexed to a chosen index. Where those rules attach is open, since neither credit nor settlement models deferred payment.

#### Considered and not done
- Pegging a sale price automatically to one reference, a foreign currency or gold — not taken: the owner does not want a price tied automatically to a single reference; an index judges a price and a rule or a person decides it.
- Filing the index under analytics — not taken: it has identity, an owner, a composition lifecycle, and sharing authorization.
- Deciding how a currency's price in another currency is represented — left open, so as not to settle the money model here.

### Sharing an index is thing's follow
- Time: 2026-10-10T14:10:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- The module's own `follow` edge is gone; following an index is now thing's [follow](../../../modules/identity/thing/edges/follow/follow.md), scoped to the index's component edges. [price-index.md](price-index.md) and [evaluated-against](edges/evaluated-against/evaluated-against.md) point there.
- The sharing semantics moved into [price-index.md](price-index.md)'s Policies: the owner's visibility rule is the follow's authorization rule, the follower reads every composition version as the owner keeps it, and a followed index may be the target of the follower's evaluated-against edges.
- The unresolved question on where the visibility rule lives is answered by that move and is replaced by the question the removed edge left open: what a revocation does to the follower's evaluated-against edges. The fork question stays open.
- [component](edges/component/component.md) gained an open question: whether a component toward another organization's product implies following that product's price, as a replacement-cost source now does.

### A component implies a follow; the module audited
- Time: 2026-10-10T14:20:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided that a component implies a follow; requested the audit
  - An AI agent in Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — audited and drafted

#### What changed
- [component](edges/component/component.md) no longer says the product's owner is neither asked nor told. A component toward another organization's product implies the index owner's [follow](../../../modules/identity/thing/edges/follow/follow.md) of that product's price edge, under that organization's authorization and accounting; the owner may admit, limit, charge for, or refuse it, and a refused follow leaves the index without a value. The open question that asked this is closed. Its Open questions now ask whether the follow is created and removed with the components, what a revoked follow leaves the index, and whether a refused component may rest on the index owner's own observation.
- "Followed against" is now "tracked against" in [price-index.md](price-index.md) and [evaluated-against](edges/evaluated-against/evaluated-against.md), so that "follow" names only thing's relation.
- Whether another index may be a component, and the refusal of a component in another count unit, were each stated in both the module and component; each now has one home.
- The Unresolved questions gained questions for separate sessions: moving the base date, how a follower receives the series, publishing an index, manipulation of a shared index, an index as a contract term, the deferred-payment warning's defaults, the legality of indexed instalments and the buyer's consent, and the pre-sale of real estate. One — whether the seller must admit the buyer's follow of an instalment index — is answered, unratified.

### A maximum age for component prices asked
- Time: 2026-10-10T14:45:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided the lessons
  - An AI agent via Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- The [Unresolved questions](price-index.md#unresolved-questions) gained one: whether an index carries a maximum age for its component prices, as replacement cost does per product, so that a value computed from an old price version is marked stale, and whether the index owner or each follower sets that age.

#### Surveyed
- The module and its [component](edges/component/component.md) and [evaluated-against](edges/evaluated-against/evaluated-against.md) edges were checked against the lessons of the 2026-10-10 pricing session: the customizable basket, deferred-payment sales, the follow a component implies, and currency components are already held. Only staleness of component prices was missing; the edges needed nothing.
