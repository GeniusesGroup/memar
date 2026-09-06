# Settlement

Settlement is tiered bookkeeping: an effect booked on a lower account must also be represented on the account(s) that reference it — a bank's customer accounts against its central-bank account, a sub-ledger against a general ledger, a branch warehouse against master inventory. The pattern is unit-general, not securities-specific.

The term [settlement](https://en.wikipedia.org/wiki/Settlement_(finance)) is kept for its general meaning ("discharging obligations"); the module is NOT limited to the financial clearing/settlement pipeline.

## Model

- `(account)-[:settlement_reference_is]->(account)` / `(account)-[:settlement_reference_of]->(account)` — current edge form (see open question below).
- `(transaction)-[:settles]->(transaction)` — many downstream transactions settled by one settlement transaction; transaction level, not book level.

## Policies (rules)

- A settlement transaction is created as an ordinary transaction immediately; a transaction only ever affects the accounts named on it. Batching/netting many small movements into one is an Engine optimization, never a model change.
- The reference edge never implies equal amounts across tiers; the upper-tier amount is decided by rules (netting, ratio policies) expressed as separate transactions with their own units.
- Settlement is independent of legal ownership: who owns a balance is `rights/ownership`; where it settles is this module.
- The module owns all its edges; the account kernel knows nothing about settlement.

## Open questions

- Edge shape: direct account→account vs. a shortcut from account into this module (`(account)-[:settlement_is]->(settlement)`) so multi-path/tiered topologies stay entirely inside the module (leaning: module-mediated; undecided).
- `endorsement` and `guarantor` currently live here only because "settlement_system" was a placeholder name for "the processing machine behind conditional fulfilment"; their final home is undecided.
- Internal structure (clearing vs settlement, netting rules) not yet modeled.
