---
Title: "Accounting Invariants"
Status: Proposed
Start Date: 2026-08-04
ID: 082916
---

# Accounting Invariants

Status: consolidated from the Account & Transaction modeling sessions (2026-08). These are the load-bearing rules of the core economics domains. Each one is a decision that was pressure-tested against real requirements (check, LC, legal block, fee, exchange, payroll); violating it breaks those scenarios. Category-level document: both `account` and `transaction` reference it, so it lives beside the modules rather than inside either - keeping the modules independent of each other.

## 1. A transaction is a request, not an operation

A Transaction is an abstraction of one or more users' intent to change bookkeeping state. It may sit in `draft`, never be executed, and be cancelled or deleted without any bookkeeping ever happening. Execution belongs to engines/processors reacting to status changes — never to the Transaction node itself.

Consequences: `Transaction ≠ Booking`, `Transaction ≠ Operation`, `Transaction ≠ Transfer`, `Transaction ≠ Payment`.

## 2. One source and one destination per transaction

A transaction has at most one `account__from` and at most one `account__to`/`account__by`. Multi-account business operations (splits, fee + transfer, batch payouts) are multiple transactions linked by edges (`followed_by`, `reference`, `settles`, ...), because each leg needs its own status/lifecycle and mapping semantics.

## 3. Withdrawal precedes deposit; delay is allowed, reorder is not

The source-side effect MUST be booked before (or at the same time as) the destination-side effect. A transaction MAY book the withdrawal now and the deposit days later (check, LC/escrow, deferred settlement). Crediting before debiting creates unbacked quantity — money/stock creation out of nothing — and is forbidden by the kernel.

A transaction also conserves quantity: what leaves the source equals what enters the destination. A non-balanced change set ("sum ≠ 0") has no meaning in this model — rejected outright, since it would undermine the foundation of accounting itself.

## 4. Unit belongs to the account, not the transaction

The count unit is declared once per account via the general `(thing)-[:count_unit_is]->(count_unit)` edge. Both accounts of one transaction MUST share the same count unit; the transaction stores only a quantity.

## 5. Cross-unit exchange is two transactions, not one

"1000 EUR for 1500 USD" is two same-unit transactions linked by an exchange/deal relation (owned by matching_system). A single transaction never mixes units.

## 6. No rollback; corrections are compensating records

A booked effect is never undone or edited. Cancellation after debit is a new transaction that books the reverse effect and links back to the original. History is append-only and audit-complete.

## 7. Booked quantity equals requested quantity

The kernel never alters the quantity of a transaction at booking time. The requested quantity lives on the transaction record itself — `Transaction.Quantity` is the single source of truth; the `bookkeeping` edge stores no copy of it (repeating it there would be a redundant cache). Partial fulfilment, fees, or amount-changing conditions are separate transactions produced by rules/processors.

## 8. Balance snapshot is a record fact; availability is not account state

Each `bookkeeping` record caches the resulting `Balance` — an immutable, historical fact of that record (accepted materialization; avoids O(n) recompute). `AvailableBalance`-style values are derived from mutable global constraints (legal blocks, pending reservations) and MUST NOT be stored as account fields; they are evaluated from rules (see `modules-plugable/economics/restriction`).

## 9. Fees and charges are rules producing transactions

A fee policy ("1% up to 10") is a Rule reacting to a transaction, producing an additional transaction (possibly conditional on the original's outcome). It is not a field on the transaction and not a second destination. When the fee applies — on attempt, on success, on failure, after authorization, after settlement — is organization policy inside the Rule; the kernel does not fix it.

## 10. Every transaction has a cause, linked by reference

No transaction exists without a reason (`transaction_reference_is` to any `thing`: invoice, message, contract, court order). The reference is set at registration and is immutable afterwards.

## Related

- [core-vs-pluggable.md](core-vs-pluggable.md)
- the reference-by-UUID rule (now in [bookkeeping](account/edges/bookkeeping/README.md))
- [account/README.md](account/README.md), [transaction/README.md](transaction/README.md), [bookkeeping edge](account/edges/bookkeeping/README.md)

## Discussion

### Drawbacks

- One-source/one-destination (#2) multiplies transaction count for splits, fees, and batch payouts; "one business operation" semantics move to edges and are harder to query.
- No atomicity (#3, #6) means users can see intermediate states (withdrawn but not yet deposited); UI and support flows must expose this, not hide it.
- #7 pushes partial fulfilment entirely into pluggable modules; the kernel cannot express "book half of this transaction".

### Rationale and alternatives

- #2: classic double-entry allows an arbitrary account set per transaction. Rejected here because each side carries its own status/lifecycle, and a bag-of-changes loses the source→destination mapping (A→B 500 + A→C 500 vs A→B 700 + A→C 300 produce the same change set).
- #3: the classical ACID atomic transfer was rejected: deferred destination effects are the essence of checks, LC/escrow, and future-dated transactions; rollback hides business truth.
- #4/#5: per-change `(quantity, unit)` was considered and rejected: the unit is a stable account property; repeating it per transaction adds no information and permits unbalanced mixed-unit transactions.
- #8: per-account `AvailableBalance` was the legacy model (~10 years old); rejected because a global constraint (one judicial block of 1000) copied per account multiplies it (100 accounts × 1000).
- #9: fee as a second destination was rejected: it breaks #2 and loses "fee depends on the original transaction's outcome".

### Prior art

- Double-entry bookkeeping: the balance requirement matches #3's anti-creation intent.
- Modern ledger products (e.g. Modern Treasury journal model): Transaction + per-account Entry — similar structure, but they model booked results, not pre-execution requests (#1).
- Intent-based transactions (blockchain/DeFi literature): separation of intent and execution path — aligned with #1.
- Letter of Credit / covered LC practice: source funds reserved at issuance, destination paid on conditions — real-world precedent for #3.
- Wage garnishment / bank levy regulation (e.g. US 31 CFR 212.7): one order against a person applied across multiple accounts — precedent for #8 and the restriction module.

### Unresolved questions

- Does the kernel ever allow booked quantity ≠ requested quantity? #7 currently answers "no"; a real counterexample forces `Field_Quantity` back onto the bookkeeping edge.
- Should #10 (every transaction has a cause) be enforced as a mandatory edge or stay a convention?

### Future possibilities

- "Cheque" as pure composition (deferred transaction + maturity rule + uri-numbered edge) — no new primitives expected; build it as a test of the model.
- Bouncing/dishonor as an event consumed by reputation/social-score analytics.
