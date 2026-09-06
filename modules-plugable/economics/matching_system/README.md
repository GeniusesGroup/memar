# Matching System
An [order matching system](https://en.wikipedia.org/wiki/Order_matching_system) or simply matching system is an electronic system that matches buy and sell orders for a stock market, commodity market or other financial exchanges. The order matching system is the core of all electronic exchanges and is used to execute orders from participants in the exchange.

Orders are usually entered by members of an exchange and executed by a central system that belongs to the exchange. The algorithm that is used to match orders varies from system to system and often involves rules around best execution.[1]

The order matching system and implied order system or Implication engine is often part of a larger electronic trading system which will usually include a settlement system and a central securities depository that are accessed by electronic trading platforms. These services may or may not be provided by the organization that provides the order matching system.

The matching algorithms decide the efficiency and robustness of the order matching system. There are two states for a market: continuous trading where orders are matched immediately or auction where matching is done at fixed intervals. A common example when a matching system is used in auction state is at the market open when a number of orders have built up.

## Definition in Memar

A matching system is a pluggable module that decides whether and how multiple transaction requests can be related and fulfilled, according to the identities and rules that system recognizes. It is deliberately broader than a securities exchange: currency conversion, goods-for-goods, contract fulfillment, and organizational matching all use the same shape. `trade` describes an outcome of a matching system, not the system itself — which is why the module is not named `trade` (or `order`).

The module owns: `trade`, `deal`, `exchange` edges; `all_or_none` and `instant_withdrawal` loop edges; `fill_or_kill` and `account__by` shortcuts. Cross-unit intent ("give 50$ to get 40€") is two same-unit transactions linked by `exchange` (invariants #4/#5 in [topic-accounting-invariants.md](../../../modules/economics/topic-accounting-invariants.md)).

## Discussion

### Drawbacks

- Same-label-different-identity: two matching systems can both define `all_or_none` with different UUIDs and different rules; a human reading the edge label cannot know which behavior applies.
- The name still carries a market-exchange flavor for users outside finance.

### Rationale and alternatives

- `trade` rejected as module name: contract↔transaction links and currency exchange are also trade-like, and the name drags back the securities-market frame. `order` rejected similarly. `matching_system` chosen for literal and technical fit, with the definition generalized.
- `all_or_none` was first modeled as a generic transaction constraint, then moved here: its meaning only exists for a matching system to interpret; a consumer needing it elsewhere can build its own module.
- `instant_withdrawal` was first considered trade-only, then found relevant for contract-linked transactions too; kept here because its semantics ("debit now, complete later") is an execution policy of the exchange/commitment process — the boundary may still move.

### Prior art

- Order matching systems (Wikipedia; SEC ATS filings): matching rules are per-system — precedent for per-system interpretation of shared labels.

### Unresolved questions

- Final module name (matching_system vs something covering contract-linked conditional execution).
- Shape of `(transaction)-[:trade_by]->(market)`: is market the direct endpoint, or via an intermediate trade node?
- `fill_or_kill` vs `all_or_none`: genuine semantic difference or duplicate labels?
- `account__by` lives here as a shortcut but overlaps core `account__to` semantics — which owns "the account the user wants to receive into"?

### Future possibilities

- A market registry module (which markets exist, their rule sets) separate from the matching engine itself.
