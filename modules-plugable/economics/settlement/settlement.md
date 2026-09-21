# Settlement

Settlement is tiered bookkeeping: an effect booked on a lower account must also be represented on the account(s) that reference it — a bank's customer accounts against its central-bank account, a sub-ledger against a general ledger, a branch warehouse against master inventory. The pattern is unit-general, not securities-specific.

The term [settlement](https://en.wikipedia.org/wiki/Settlement_(finance)) is kept for its general meaning ("discharging obligations"); the module is NOT limited to the financial clearing/settlement pipeline.

Stage separation (often conflated in the chats; keep them distinct):

- **Matching** — finding compatible requests (owned by [matching_system](../matching_system/README.md)).
- **Clearing** — computing/netting the obligations between parties before anything is booked (owned by this module's rules; not yet modeled).
- **Settlement** — producing the final effect as ordinary transactions + bookkeeping (this module's core job).

Bank, warehouse, and securities scenarios must all pass through the same three-stage shape before this module's design is finalized.

## Model

- `(account)-[:settlement_reference_is]->(account)` / `(account)-[:settlement_reference_of]->(account)` — current edge form (see open question below).
- `(transaction)-[:settles]->(transaction)` — many downstream transactions settled by one settlement transaction; transaction level, not book level.

## Policies (rules)

- A settlement transaction is created as an ordinary transaction immediately; a transaction only ever affects the accounts named on it. Batching/netting many small movements into one is an Engine optimization, never a model change.
- The reference edge never implies equal amounts across tiers; the upper-tier amount is decided by rules (netting, ratio policies) expressed as separate transactions with their own units.
- Settlement is independent of legal ownership: who owns a balance is `rights/ownership`; where it settles is this module.
- The module owns all its edges; the account kernel knows nothing about settlement.

## Discussion

### Drawbacks

- Creating settlement transactions immediately doubles write volume; netting only happens as an engine optimization, so the graph stays noisy.
- With the leaning module-mediated shape, "where does this account settle?" is a traversal through the module, not one direct edge.

### Rationale and alternatives

- Direct account→account `settlement_reference_is` was the first shape; the shortcut-into-module shape is favored because multi-path/tiered topologies (a bank settling both via a clearing house and directly at the central bank) would otherwise leak cardinality rules into the account domain.
- Aggregating at the Book level was considered and rejected: a transaction only ever affects the accounts named on it, so `settles` stays at transaction level.
- The reserve-ratio scenario was first misread as "different amounts on one transaction across tiers"; corrected: it is separate transactions with their own units — reinforcing invariants #4/#5.
- "Money creation from nothing" was rejected as a primitive: it is two transactions between two accounts with two different units (legal-reserve unit vs currency unit).

### Prior art

- Fed funds / central-bank settlement accounts (Federal Reserve payments systems docs).
- Securities clearing: netting and novation between trade and settlement; T+1/T+2 cycles.
- Sub-ledger → general-ledger rollups inside one organization — same tiered pattern, which is why the concept must not be limited to cross-organization cases.

### Unresolved questions

- Edge shape: direct account→account vs. `(account)-[:settlement_is]->(settlement)` shortcut (leaning: module-mediated; undecided).
- `endorsement` and `guarantor` live here only because "settlement_system" was a placeholder name for "the processing machine behind conditional fulfilment"; their final home is undecided.
- Internal structure (clearing vs settlement, netting rules) not yet modeled.
- Can one account have parallel settlement paths? (Module-mediated shape answers trivially; direct-edge shape needs an explicit cardinality decision.)

### Future possibilities

- A `market` registry (which markets exist, their rule sets) shares the tiered pattern with matching_system's `trade_by`; revisit both together.
