# Economics Analytics

Cross-domain analytical modules over the economics core: knowledge produced from account/transaction/invoice data that belongs to no single domain (e.g. `pair_amount`, `user-credit`, `financial-risk`, [invoice-totals](invoice-totals/README.md)). Domain-specific analytics live inside their own pluggable modules instead (e.g. payroll analytics under payroll; discount usage under [discount/analytics](../discount/analytics/price-payable/README.md)).

## Policies (rules)

- Analytics is always pluggable: it produces discovered/derived data from acquired data; an organization may install none of it (availability boundary: [bookkeeping](../../../modules/economics/account/edges/bookkeeping/README.md) §8).
- A query with its own types, events, storage, and processing is itself a module — no general SQL-style engine mediates it.
- Name modules by the knowledge produced, not by the aggregation mechanics.
- Time: modules work on the canonical `utc_minute` representation; converting a user's calendar expression (Persian/Gregorian day) into that representation is a higher layer's job, not a per-module concern.

## Discussion

### Drawbacks

- Folder count grows with every analytical need; each folder must earn module status (responsibility, not convenience query).

### Rationale and alternatives

- Filing analytics under `modules-plugable/economics/account/...` was rejected: pluggable must not mimic core namespaces.
- One giant `analytics` module was rejected: each analytical responsibility is independently installable/removable.

### Prior art

- Read-models/CQRS projections produce derived views from an event log — same "discovered from acquired" idea, here expressed as pluggable modules rather than a framework layer.

### Unresolved questions

- `pair_amount` vs `pair_amount-utc-minute`: are these two modules or one module with a time-resolution parameter? Naming currently encodes mechanics, not knowledge.
- Should derived values (e.g. `total_blocked`) carry an explicit "cache, not truth" marker in their protocol files?
- Price volatility for the deferred-payment warning: is a product's price movement over recent months, read by the warning rule at an invoice's approval, an analytics module here, or the rule's own computation over the product's price versions ([price index → Deferred-payment sales](../price-index/price-index.md#deferred-payment-sales))?

### Future possibilities

- A shared calendar-interpretation module above all time-bucketed analytics.
- Holding-gain analytics: sale price − replacement cost is the operating margin, and replacement cost − historical cost (FIFO, weighted-average, or batch recorded cost, kept for accounting) is the holding gain inflation produced; shown apart they reveal the real profit ([replacement cost → Future possibilities](../replacement-cost/replacement-cost.md#future-possibilities)).

## Idea backlog

Nothing below is ratified.

### Financial analysis
- **Idea**: a financial-analysis protocol producing reports "use for cost-accounting, Retention rate, ...", report granularity "can make report Daily, Monthly, Yearly, ..."; record fields `PredictionTime uint64` ("Time need to use or deliver, can also use in budget analysis or prebuy!") and `Importance uint8` ("Use in budget analysis").
- **Review questions**: are PredictionTime/Importance inputs this protocol stores, or budget facts read across from [budget](../budget/budget.md)? Does "financial analysis" stay one module or split by the knowledge produced (cost accounting vs retention — name modules by the knowledge produced)? The folder now holds only an empty `financial-analysis/protocol/` skeleton — instantiate the module, or fold the fields into an existing analytics module?

### Campaign analytic
- **Idea**: knowledge about how an advertising campaign performed.
- **Review questions**: is that knowledge its own module (name it by the knowledge, not by a GUI page), or a report inside an existing analytics module?
