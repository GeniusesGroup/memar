# Transaction

A transaction is an abstraction of a request by one or more users for a bookkeeping change. It is a request, not an operation: it may be drafted, approved, partially processed, deferred, cancelled, or deleted, and none of that execution logic lives in this node. Processing belongs to engines/processors reacting to status changes and rules.

## Model

- A transaction is a `thing`.
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
- Transactions relate to each other through edges (`followed_by`, `exchange`, `settles`, `endorsement_in_favor_of`, ...), most of them owned by pluggable modules.

## Open questions

- `Field_FinancialTransactionUUID` keeps a legacy "financial" prefix although the domain is unit-general; rename pending.
- `account__from` README still describes optional `takes` semantics with pre-matching_system naming; reconcile with `account__by` (matching_system).
