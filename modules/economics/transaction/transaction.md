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

- At most one source and one destination; larger business operations are several transactions linked by edges ([transaction.handoff.md](transaction.handoff.md) §2).
- Both accounts of one transaction share the same count unit ([account.handoff.md](../account/account.handoff.md) §4); cross-unit intent is two transactions linked by matching_system ([matching_system](../../../modules-plugable/economics/matching_system/README.md) §5).
- The source effect must precede the destination effect; the destination effect may be arbitrarily delayed or conditional ([transaction.handoff.md](transaction.handoff.md) §3).
- No rollback: cancelling after a debit creates a compensating transaction ([transaction.handoff.md](transaction.handoff.md) §6).
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
- Allowing multiple accounts per side was considered (classic accounting) and rejected — see [transaction.handoff.md](transaction.handoff.md) §2 rationale.

### Prior art

- Banking apps already show "requests/orders" separately from posted transactions — matches [transaction.handoff.md](transaction.handoff.md) §1.
- Intent-based transaction proposals (DeFi): declare the outcome, let the system find the execution path.

### Unresolved questions

- Which of `account__to` (core) vs `account__by` (matching_system) owns "the account the user wants to receive into"? `account__from` README still describes optional `takes` semantics with pre-matching_system naming; reconcile.
- Canonical status list (draft, authorization, ...): which are kernel defaults, which are organizational?

### Future possibilities

- Transaction-chain views (`followed_by`/`settles`/`exchange`) as a GUI widget module over the graph.

## Idea backlog

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified. Non-edge sources (`services/`, `status/`) stay here; edge sources live in the per-edge docs above.

**Idea** — Transaction query service: "User can limit search by tags, currencies, ..." — `GET apis.sabz.city/financial/v1/{User-UUID}/transaction/?limit=10`.
**Review questions**: which capability owns this query surface - the kernel exposes no such API; is filtering an analytics/query pluggable (analytics is always pluggable) or a transaction read service?

**Idea** — User balance service: "Get user ballance in specific currency." - balance formats: Final, Blocked, Usabable.
**Review questions**: Final balance is the bookkeeping snapshot (see [bookkeeping](../account/edges/bookkeeping/README.md) §8) - are Blocked/Usabable availability evaluations owned by restriction rules rather than stored state? Does the per-currency view cross into matching_system?

**Idea** — Transfer service: "Transfer money to other as any type e.g. to approve an invoice, gift".
**Review questions**: does "any type" ride on the reference-type labels (now in the [reference](edges/reference/reference.md) doc) or on a dedicated transfer capability? Converges with open #1 Transfer-vs-Transaction in [transaction.handoff.md](transaction.handoff.md).

**Idea** — Transfer-to-other-user: immutability constraints - "User can't redo||change|| ... to transaction." and "Currency change can't be in transaction request."; plus a tentative flow - "Transfer can be from blocked balance by justice MS. To do this I think we must unblock first and transfer amount."
**Review questions**: do no-edit and fixed-currency belong to the kernel (immutable request) or to rule evaluation? For blocked-balance transfer - is unblock-then-transfer a restriction rule producing follow-up transactions (Core never knows Rule), and how does it bear on open #1 Transfer-vs-Transaction in [transaction.handoff.md](transaction.handoff.md)?

**Idea** — Status labels: candidate status labels - Pending, Expired, Cancelled, Voided; plus budget statuses Executed, Inspected.
**Review questions**: statuses come from the general status domain (Policies above; open #4 in [transaction.handoff.md](transaction.handoff.md)) - which labels are kernel defaults and which are organizational? Are budget statuses the budget module's vocabulary instead?
