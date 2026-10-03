# Bookkeeping

The kernel edge between a transaction and an account: the realized effect of processing a transaction on one account. One transaction produces one bookkeeping record per affected account, possibly at different times (withdrawal first, deposit later — see ordering decision in [transaction.handoff.md](../../../transaction/transaction.handoff.md) §3).

## Reference by UUID, not aggregates (cross-domain modeling rule)

Discovered in this domain, general enough to govern all of Memar: **domain models MUST NOT embed or return each other's types.** A cross-domain link is held as a UUID reference only; a separate service resolves UUID → record when the full object is needed. This edge is the working example: it holds `Field_AccountID` and `Field_TransactionID` — UUIDs, nothing more. Account does not carry Transaction objects; Transaction does not carry Account objects.

Why (from the Account & Transaction modeling session, 2026-08):

- Account ↔ Transaction is a genuinely mutual conceptual dependency (a transaction names accounts; a ledger entry names its transaction). Fighting it with shared abstraction packages or interfaces only hides the cycle or throws away type information. With UUID-only fields there is no bidirectional *type* dependency at all — the "cycle" was never a domain problem; it is an artifact of aggregate-style modeling (DDD) that embeds child records inside one owner.
- Caching: the consumer of a UUID decides whether/how to resolve and cache; an embedded aggregate forces the producer's freshness semantics onto every consumer.
- Embedded/edge deployment: a module compiled as a library at the edge can hold references without co-locating the other domain's storage.
- Language note: Go forbids import cycles at package level, which pressures developers into string-typed IDs or artificial abstractions. Khayyam measures dependencies at type level, so this rule is naturally enforceable there. The Go constraint is a representation limit, not a domain principle.
- Related identity principle: human-readable identifiers (username, cheque number, sayyad code) are also not fields on a node — they are edges from the node to a `uri` domain record; the same "reference, not embed" logic applied to naming.
- Rejected alternatives: shared abstraction package holding both interfaces (only good if the relationship itself is a real domain concept, not a cycle-breaking device); dependency inversion via interfaces (hides, does not resolve); DDD aggregate root owning bookkeeping entries (forces one domain to own another domain's records).
- Costs (drawbacks): reading a transaction with its accounts costs several fetches instead of one aggregate load; without discipline, "just UUIDs" degenerates into primitive string typing that throws away all type information.
- Open: does a bidirectional edge (bookkeeping traversed from both sides) share one edge UUID or exist as two records? (model question above); should UUID→record resolution be a generated per-domain service or one generic graph resolver? Candidate future: formalize as a Memar-wide modeling rule with lint/codegen support.

The term [bookkeeping](https://en.wikipedia.org/wiki/Bookkeeping) is reused here in its general sense of recording quantity changes, not financial recording only.

## Dictionary

bookkeeping  book·keep·ing /ˈbukˌkiːpɪŋ/ n [U]

n.
- the activity of recording business transactions

## Model

- `(transaction)-[:bookkeeping]->(account)`

Open question (deferred to the storage-engine session): whether the reverse traversal `(account)-[:booked_by]->(transaction)` is a second edge record or a representation of the same edge identity with a shared UUID.

## Policies (rules)

- Cardinality: one transaction produces one bookkeeping record per affected account — two for a from+to transaction, one while only the source effect has realized (§3 deferral in [transaction.handoff.md](../../../transaction/transaction.handoff.md)), zero if it is never processed past draft.
- Sign convention: the effect's direction and sign come from WHICH side of the transaction the account sits on — an `account__from` record subtracts the quantity, an `account__to` record adds it. The edge direction is always transaction→account; quantity itself is never stored here (§7 below).
- There is no quantity field on this edge: booked quantity always equals the transaction's requested quantity (§7 below). Any deviation (partial fill, fee, rule-altered amount) is a different transaction with its own bookkeeping.
- A record is never edited or deleted. Reversal is a new bookkeeping record produced by a new (compensating) transaction ([transaction.handoff.md](../../../transaction/transaction.handoff.md) §6).
- The account's current balance is the `Balance` of its highest-index record; nothing stores balance on the account node (§8 below).

## Fields

- `Field_AccountID` — edge endpoint (account side), a UUID reference only.
- `Field_TransactionID` — edge endpoint (transaction side). Part of the record's identity, not a cache: a ledger entry that cannot be traced to its originating transaction is worthless for audit. (Declared `Field_FinancialTransactionUUID` in the Go record; renamed on conversion — see [account.handoff.md](../../account.handoff.md).)
- `Field_TransactionIndex` — auto-increment ordinal of this record within its account's history; gives direct access to "the Nth booking of this account" without traversal.
- `Field_Balance` — the account's balance resulting from this record. An immutable historical snapshot (append-only, never recomputed), kept so point-in-time balance is O(1). This is the accepted form of caching; it is categorically different from a mutable derived field like `AvailableBalance`, which was rejected as account state (§8 below).
- `Field_RequestID` + request audit time — which request produced this record.

## Discussion

### Drawbacks

- A ledger entry cannot answer "how much?" alone; it dereferences the transaction. If the transaction is archived/deleted by retention policy, the entry loses meaning — the ledger is not self-sufficient.
- `TransactionIndex` per account implies a write-serialization point per account (concurrency cost at the engine level).

### Rationale and alternatives

- Book as a separate node was considered (earlier diagrams drew it between Engine and Account) and rejected: nothing needs to reference a bookkeeping record except through its transaction, so an edge with fields is sufficient.
- `Field_TransactionID` is the transaction-side endpoint of the edge (a UUID reference, per the reference-by-UUID rule above), not a cache — it is the audit traceability requirement.
- `Field_Balance` is an accepted cache (O(1) point-in-time reads); it is a historical fact of this record, never recomputed.

### Prior art

- Double-entry ledgers record per-posting running balances on ledger pages — same idea, here as edge fields.

### Load-bearing decisions migrated here (formerly accounting-invariants §§7–8 + backlog)

#### 7. Booked quantity equals requested quantity
The kernel never alters the quantity of a transaction at booking time. The requested quantity lives on the transaction record itself — `Transaction.Quantity` is the single source of truth; the `bookkeeping` edge stores no copy of it (repeating it there would be a redundant cache). Partial fulfilment, fees, or amount-changing conditions are separate transactions produced by rules/processors.

#### 8. Balance snapshot is a record fact; availability is not account state
Each `bookkeeping` record caches the resulting `Balance` — an immutable, historical fact of that record (accepted materialization; avoids O(n) recompute). `AvailableBalance`-style values are derived from mutable global constraints (legal blocks, pending reservations) and MUST NOT be stored as account fields; they are evaluated from rules (see `modules-plugable/economics/restriction`).

#### Backlog — book edge state *(open remnants kept verbatim)*
- **The `book` edge carries state** (quantity, balance, transaction index). Balance ("the balance resulting from this booking") is an immutable property of the bookkeeping record itself; **AvailableBalance** = actual minus pending transactions, and is *not* treated as fundamental truth until the precise effect of pending Transactions on the Account is defined. Open TODO: per-entry cached balance vs. recomputed-on-read from all transactions. *(open)*
- Note: the backlog's "actual minus pending" formulation and the invariant's "derived from global constraints / restriction rules" formulation are both preserved; reconciling them is part of the AvailableBalance trust question on [account.handoff.md](../../account.handoff.md).

#### Embedded graph engine *(direction — affects bookkeeping deployment)*
- **Embedded graph engine (edge computing).** True domain autonomy when the graph engine compiles *into* each domain as a library rather than living in one central database; new requirements attach as new edges and evolve independently, and a domain can ship its own GUI without polluting a central model. *(direction)*

### Unresolved questions

- Does the kernel ever allow booked quantity ≠ requested quantity? #7 currently answers "no"; a real counterexample forces `Field_Quantity` back onto the bookkeeping edge as record truth, not cache.
- Reversal test: must a compensating record ever point at a specific bookkeeping edge rather than the originating transaction? If yes, bookkeeping needs its own addressable identity.
- Is `TransactionIndex` a domain contract (stable across storage engines, exposed in reports/APIs, meaningful to consumers) or a pure storage detail that the domain model must not promise?
- Code comment inconsistency to fix: `protocol/dt-balance.kh` currently describes Balance as "the total of all the transactions on the account including any pending transactions" — that contradicts the realized-effect semantics agreed here (a bookkeeping record is a booked fact, not a projection over pending state). The comment must be corrected in code. *(Still open: the Khayyam conversion deliberately did not carry the Go comment into the `.kh`, so the wrong description now lives only in the Go clue block. The wording above — "the account's balance resulting from this record" — is the text that should replace it.)*
- AvailableBalance trust + pending-effect definition (shared with account/restriction).

### Future possibilities

- Materialized balance checkpoints every N records for very long accounts (pure engine optimization).

## Placement

- **Verdict: stays in this core module.** Bookkeeping is the account kernel's single edge — core-by-necessity holds: without the realized transaction→account effect the kernel would have to fabricate a surrogate link between a transaction's request and an account's state, distorting both foundational concepts ([account.md](../../account.md): "The kernel of this domain is exactly one edge").
- The migrated source is this edge's own `protocol/` stub (package `bookkeeping_p`, no processing claimed elsewhere) — nothing moves under "a pluggable owns its complete capability". Not analytics (no derived or discovered data), and it carries no rule knowledge: booked quantities and availability are evaluated by rules, not stored as kernel semantics (§7–§8 above; [restriction](../../../../../modules-plugable/economics/restriction/restriction.md)).
- Request-side semantics (ordering, compensation, cause) stay with [transaction.handoff.md](../../../transaction/transaction.handoff.md) §§3/6/10 — bookkeeping only records them; the kernel never learns rule logic (Core never knows Rule).

