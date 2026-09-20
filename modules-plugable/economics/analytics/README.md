# Economics Analytics

Cross-domain analytical modules over the economics core: knowledge produced from account/transaction/invoice data that belongs to no single domain (e.g. `pair_amount`, `user-credit`, `financial-risk`). Domain-specific analytics live inside their own pluggable modules instead (e.g. payroll analytics under payroll).

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

### Future possibilities

- A shared calendar-interpretation module above all time-bucketed analytics.
