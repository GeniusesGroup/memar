# Bookkeeping

The kernel edge between a transaction and an account: the realized effect of processing a transaction on one account. One transaction produces one bookkeeping record per affected account, possibly at different times (withdrawal first, deposit later — see invariant #3 in [topic-accounting-invariants.md](../../../../topic-accounting-invariants.md)).

The term [bookkeeping](https://en.wikipedia.org/wiki/Bookkeeping) is reused here in its general sense of recording quantity changes, not financial recording only.

## Dictionary

bookkeeping  book·keep·ing /ˈbukˌkiːpɪŋ/ n [U]

n.
- the activity of recording business transactions

## Model

- `(transaction)-[:bookkeeping]->(account)`

Open question (deferred to the storage-engine session): whether the reverse traversal `(account)-[:booked_by]->(transaction)` is a second edge record or a representation of the same edge identity with a shared UUID.

## Policies (rules)

- There is no quantity field on this edge: booked quantity always equals the transaction's requested quantity (invariant #7). Any deviation (partial fill, fee, rule-altered amount) is a different transaction with its own bookkeeping.
- A record is never edited or deleted. Reversal is a new bookkeeping record produced by a new (compensating) transaction (invariant #6).
- The account's current balance is the `Balance` of its highest-index record; nothing stores balance on the account node (invariant #8).

## Fields

- `Field_AccountID` — edge endpoint (account side), a UUID reference only.
- `Field_FinancialTransactionUUID` — edge endpoint (transaction side). Part of the record's identity, not a cache: a ledger entry that cannot be traced to its originating transaction is worthless for audit.
- `Field_TransactionIndex` — auto-increment ordinal of this record within its account's history; gives direct access to "the Nth booking of this account" without traversal.
- `Field_Balance` — the account's balance resulting from this record. An immutable historical snapshot (append-only, never recomputed), kept so point-in-time balance is O(1). This is the accepted form of caching; it is categorically different from a mutable derived field like `AvailableBalance`, which was rejected as account state (invariant #8).
- `Field_RequestID` + request audit time — which request produced this record.

## Discussion

### Drawbacks

- A ledger entry cannot answer "how much?" alone; it dereferences the transaction. If the transaction is archived/deleted by retention policy, the entry loses meaning — the ledger is not self-sufficient.
- `TransactionIndex` per account implies a write-serialization point per account (concurrency cost at the engine level).

### Rationale and alternatives

- Book as a separate node was considered (earlier diagrams drew it between Engine and Account) and rejected: nothing needs to reference a bookkeeping record except through its transaction, so an edge with fields is sufficient.
- `Field_FinancialTransactionUUID` is the transaction-side endpoint of the edge (a UUID reference, per [topic-reference-by-uuid.md](../../../topic-reference-by-uuid.md)), not a cache — it is the audit traceability requirement.
- `Field_Balance` is an accepted cache (O(1) point-in-time reads); it is a historical fact of this record, never recomputed.

### Prior art

- Double-entry ledgers record per-posting running balances on ledger pages — same idea, here as edge fields.

### Unresolved questions

- Does the kernel ever allow booked quantity ≠ requested quantity? If yes, a `Field_Quantity` must return as record truth, not cache (invariant #7).
- Reversal test: must a compensating record ever point at a specific bookkeeping edge rather than the originating transaction? If yes, bookkeeping needs its own addressable identity.

### Future possibilities

- Materialized balance checkpoints every N records for very long accounts (pure engine optimization).
