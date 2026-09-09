# Transaction

A transaction is an abstraction of a request by one or more users for a bookkeeping change. It is a request, not an operation: it may be drafted, approved, partially processed, deferred, cancelled, or deleted, and none of that execution logic lives in this node. Processing belongs to engines/processors reacting to status changes and rules.

## Model

- A transaction is a `thing`.
- `Quantity` is a field of the transaction record — the single source of truth for the amount (the `bookkeeping` edge deliberately stores no copy).
- `(transaction)-[:account__from]->(account)` — the single source account (optional at registration).
- `(transaction)-[:account__to]->(account)` — the single destination account (optional at registration).
- `(transaction)-[:bookkeeping]->(account)` — realized effects; the edge is owned by the account domain ([bookkeeping](../account/edges/bookkeeping/README.md)).
- `(transaction)-[:transaction_reference_is]->(thing)` — the cause/subject of the request.
- `(transaction)-[:condition_is]->(rule)` — execution governed by an external rule.

## Policies (rules)

- At most one source and one destination; larger business operations are several transactions linked by edges (invariant #2).
- Both accounts of one transaction share the same count unit (invariant #4); cross-unit intent is two transactions linked by matching_system (invariant #5).
- The source effect must precede the destination effect; the destination effect may be arbitrarily delayed or conditional (invariant #3).
- No rollback: cancelling after a debit creates a compensating transaction (invariant #6).
- Statuses (draft, authorization, ...) come from the general status domain; a status change may trigger processes via rules — the kernel hard-codes no workflow.
- Generic statuses like `issued`, `blocked`, `bounced` apply to ANY transaction, not just cheques: a transaction awaiting processing is "issued"; a court can block any of them; a failed fulfilment bounces with consequences (e.g. social-credit rules). Cheque-specific vocabulary is labels, not new lifecycle states.
- Transactions relate to each other through edges (`followed_by`, `exchange`, `settles`, `endorsement_in_favor_of`, ...), most of them owned by pluggable modules.

## Discussion

### Drawbacks

- Because a transaction is a request, "transaction history" and "what actually happened" are different queries (transactions vs bookkeeping); consumers must understand both.
- Optional from/to at registration means the kernel cannot fully validate a transaction alone; validity emerges at processing time via rules.

### Rationale and alternatives

- Modeling Transaction as the operation itself (classical payment processing) was rejected: drafts, cancelled requests, and multi-day deferred deposits are first-class requirements (check, LC), and an operation-only model must fake them with extra concepts.
- A transaction-owned status enum was rejected in favor of the general status domain, so organizations extend lifecycles without touching core.
- Allowing multiple accounts per side was considered (classic accounting) and rejected — see invariant #2 rationale.

### Prior art

- Banking apps already show "requests/orders" separately from posted transactions — matches invariant #1.
- Intent-based transaction proposals (DeFi): declare the outcome, let the system find the execution path.

### Unresolved questions

- Which of `account__to` (core) vs `account__by` (matching_system) owns "the account the user wants to receive into"? `account__from` README still describes optional `takes` semantics with pre-matching_system naming; reconcile.
- Canonical status list (draft, authorization, ...): which are kernel defaults, which are organizational?
- `Field_FinancialTransactionUUID` keeps a legacy "financial" prefix although the domain is unit-general; rename pending.

### Future possibilities

- Transaction-chain views (`followed_by`/`settles`/`exchange`) as a GUI widget module over the graph.

## Idea backlog from edge code comments

Raw proposal from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Reference types - edges-shortcut/transaction.go
- **Idea**: reference-type labels for transactions: TransactionFee, Prize, Donate, Charity, Tip, Commission, Reward, Profit, Credit, Loan, BadDebt (debt default), Installment, Compensation, RentalFee, Bill, Asset, Stock, Invoice (both buy and refund via ReturnInvoice). Explicitly rejected in comments (digital-era banking, no cash support): RevolvingFund, SameBankTransfer, ForeignBankTransfer, POSTransfer, WebTransfer - "not the goal, just the way of transaction that can be checked by RequestID".
- **Budget labels**: Materials, Labor, Investments (Equipment), Markup (the % added to cost for wholesale price), WholesaleProfit, Margin (the % of product price for retail price), RetailProfit, Cost.
- **Review questions**: do reference types belong to the reference edge (transaction_reference_is) as labels, or to the originating domains? Are budget labels the budget module's data? The Item-ingredient and item-seat business-service comments (listing query services) are data-model pass material.