# Securities

Holding and transferring shares or bonds is plain bookkeeping: an account whose `count_unit` is "shares of X" or "bonds of Y", moved by ordinary transactions. No new accounting primitive is needed — "securities" itself may end up being just a label. What this module owns is what is genuinely specific to securities: issuer identity, corporate actions (dividends, splits, capital increases), voting rights.

## Model

- [securities-for](edges/securities-for/README.md) — draft edge relating an account to the issuing organization (under review).
- [shareholder](edges/shareholder/README.md) — draft edge (under review).

## Policies (rules)

- Custody/holding relations (an account held at depository Z for person A, mirrored against A's entry at issuer X) belong to `rights/ownership`, not here — the pattern applies to any asset, not just securities.
- The sync/correspondence between two independent ledgers is a settlement-tier concern (see [settlement](../settlement/README.md)), not an asset-type concept.

## Discussion

### Drawbacks

- The remaining boundary ("everything generic is bookkeeping, only issuer mechanics live here") is thin; if corporate actions turn out to be invoice/transaction compositions too, this module may collapse into labels.

### Rationale and alternatives

- A securities-as-own-domain model (per-asset-type accounts, statuses, processes — the typical finance-software approach) was rejected: endorsement, bouncing, blocking all generalized to plain transactions with edges; per-asset-type domains would duplicate them.

### Prior art

- Central securities depositories (CSD), nominee/omnibus accounts — the custody layer is institution-specific, hence ownership-domain.

### Unresolved questions

- Which edges survive after moving custody relations to `rights/ownership`?
- Ledger correspondence (same holding recorded at two organizations): ownership edge, settlement edge, or a new `corresponds_to`?

### Future possibilities

- Corporate actions as rule modules producing invoices/transactions (dividend = issuer invoicing holders).
