# Account Relationship
Pluggable policies and preferences between accounts (or between an account and a user): who may transfer to whom, which account is the default for a purpose. These are not account-kernel facts — an organization can run the entire core without a single one of them.

## Model
- [limit-transfer](edges/limit-transfer/README.md) — `(account)-[:limit_transfer_to/from]->(account)` allow-list between accounts.
- [main_account-give](edges/main_account-give/README.md) / [main_account-take](edges/main_account-take/README.md) — default account per user per purpose/unit.
- [limit-amount](edges-loop/limit-amount/README.md) — amount limits on transfers between accounts.

## Policies (rules)
- The edges are data; enforcement is by rules attached to them (e.g. reject a transaction whose from/to pair lacks a `limit_transfer_to` edge).
- One active "main/primary" relation per user per type.

## Discussion

### Drawbacks
- One module holding heterogeneous edges (restriction vs preference) risks becoming a "miscellaneous account edges" bucket.

### Rationale and alternatives
- Kept together because the volume of account-to-account relationship needs is small; splitting into `account_restriction` + `account_preference` was considered and deferred until edge count forces it.
- Filing these under the account core was rejected: they are policy, not identity. A pluggable module owns its complete capability (edge + processing together); differences in processing semantics belong in pluggable modules, not in the account kernel.

### Prior art
- Banking beneficiary/payee registration (linked accounts lists) — same allow-list pattern.

### Future possibilities
- Named beneficiary lists as sibling edges once more relationship needs surface.
