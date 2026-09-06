# Topic: Accounting Invariants

Status: consolidated from the Account & Transaction modeling sessions (2026-08). These are the load-bearing rules of the core economics domains. Each one is a decision that was pressure-tested against real requirements (check, LC, legal block, fee, exchange, payroll); violating it breaks those scenarios.

## 1. A transaction is a request, not an operation

A Transaction is an abstraction of one or more users' intent to change bookkeeping state. It may sit in `draft`, never be executed, and be cancelled or deleted without any bookkeeping ever happening. Execution belongs to engines/processors reacting to status changes — never to the Transaction node itself.

Consequences: `Transaction ≠ Booking`, `Transaction ≠ Operation`, `Transaction ≠ Transfer`, `Transaction ≠ Payment`.

## 2. One source and one destination per transaction

A transaction has at most one `account__from` and at most one `account__to`/`account__by`. Multi-account business operations (splits, fee + transfer, batch payouts) are multiple transactions linked by edges (`followed_by`, `reference`, `settles`, ...), because each leg needs its own status/lifecycle and mapping semantics.

## 3. Withdrawal precedes deposit; delay is allowed, reorder is not

The source-side effect MUST be booked before (or at the same time as) the destination-side effect. A transaction MAY book the withdrawal now and the deposit days later (check, LC/escrow, deferred settlement). Crediting before debiting creates unbacked quantity — money/stock creation out of nothing — and is forbidden by the kernel.

## 4. Unit belongs to the account, not the transaction

The count unit is declared once per account via the general `(thing)-[:count_unit_is]->(count_unit)` edge. Both accounts of one transaction MUST share the same count unit; the transaction stores only a quantity.

## 5. Cross-unit exchange is two transactions, not one

"1000 EUR for 1500 USD" is two same-unit transactions linked by an exchange/deal relation (owned by matching_system). A single transaction never mixes units.

## 6. No rollback; corrections are compensating records

A booked effect is never undone or edited. Cancellation after debit is a new transaction that books the reverse effect and links back to the original. History is append-only and audit-complete.

## 7. Booked quantity equals requested quantity

The kernel never alters the quantity of a transaction at booking time. Partial fulfilment, fees, or amount-changing conditions are separate transactions produced by rules/processors. Therefore the `bookkeeping` edge stores no quantity of its own.

## 8. Balance snapshot is a record fact; availability is not account state

Each `bookkeeping` record caches the resulting `Balance` — an immutable, historical fact of that record (accepted materialization; avoids O(n) recompute). `AvailableBalance`-style values are derived from mutable global constraints (legal blocks, pending reservations) and MUST NOT be stored as account fields; they are evaluated from rules (see `modules-plugable/economics/restriction`).

## 9. Fees and charges are rules producing transactions

A fee policy ("1% up to 10") is a Rule reacting to a transaction, producing an additional transaction (possibly conditional on the original's outcome). It is not a field on the transaction and not a second destination.

## 10. Every transaction has a cause, linked by reference

No transaction exists without a reason (`transaction_reference_is` to any `thing`: invoice, message, contract, court order). The reference is set at registration and is immutable afterwards.

## Related

- [topic-core-vs-pluggable.md](topic-core-vs-pluggable.md)
- [account/README.md](account/README.md), [transaction/README.md](transaction/README.md), [bookkeeping edge](account/edges/bookkeeping/README.md)
