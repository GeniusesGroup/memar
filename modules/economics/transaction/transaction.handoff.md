# Transaction Handoff

## Topic & Purpose
Load-bearing decisions for the Transaction domain: request-vs-effect, cardinality, ordering, compensation, cause reference, processing/retry patterns, and open naming/multiplicity questions. Consolidated from Account & Transaction modeling sessions (2026-08) and the Organization ideas backlog (2026-09-16 migration).

## Status
Active — invariants practiced in README/edges; open questions below still block final naming and Transfer-vs-Transaction clarification.

## Decisions

### From accounting invariants (formerly `modules/economics/accounting-invariants.md`)

#### 1. A transaction is a request, not an operation
A Transaction is an abstraction of one or more users' intent to change bookkeeping state. It may sit in `draft`, never be executed, and be cancelled or deleted without any bookkeeping ever happening. Execution belongs to engines/processors reacting to status changes — never to the Transaction node itself.

Consequences: `Transaction ≠ Booking`, `Transaction ≠ Operation`, `Transaction ≠ Transfer`, `Transaction ≠ Payment`.

#### 2. One source and one destination per transaction
A transaction has at most one `account__from` and at most one `account__to`/`account__by`. Multi-account business operations (splits, fee + transfer, batch payouts) are multiple transactions linked by edges (`followed_by`, `reference`, `settles`, ...), because each leg needs its own status/lifecycle and mapping semantics.

#### 3. Withdrawal precedes deposit; delay is allowed, reorder is not
The source-side effect MUST be booked before (or at the same time as) the destination-side effect. A transaction MAY book the withdrawal now and the deposit days later (check, LC/escrow, deferred settlement). Crediting before debiting creates unbacked quantity — money/stock creation out of nothing — and is forbidden by the kernel.

A transaction also conserves quantity: what leaves the source equals what enters the destination. A non-balanced change set ("sum ≠ 0") has no meaning in this model — rejected outright, since it would undermine the foundation of accounting itself.

#### 6. No rollback; corrections are compensating records
A booked effect is never undone or edited. Cancellation after debit is a new transaction that books the reverse effect and links back to the original. History is append-only and audit-complete.

#### 10. Every transaction has a cause, linked by reference
No transaction exists without a reason (`transaction_reference_is` to any `thing`: invoice, message, contract, court order). The reference is set at registration and is immutable afterwards.

### From Organization ideas backlog (Bookkeeping + Process)

- **Separate the request from its effect.** The record of a change-request is distinct from the actual effect on an Account: checks, trades, conditional orders, future transfers, guarantees (ضمانت), settlements, failed/suspended transactions, and transaction chains all depend on this separation. *(decided)*
- **A Transaction is one coherent accounting request**, not an arbitrary collection of account effects. When a business operation needs several independent accounting requests, the relationship between Transactions models it (`T1 —followed_by→ T2`) — not several effects packed into one Transaction. *(decided)*
- **Domain ordering invariant:** withdrawal from the source must logically precede deposit to the destination (you cannot have paid out what has not yet come in). Distinguish three levels — order in the *model*, order in the *process*, order in the *engine execution*: only the third is an implementation concern; an atomic engine can satisfy the model invariant without literal sequential execution. *(decided)*
- **Guarantees are contingent liabilities.** Modeling them exposes both a performance and a modeling challenge: reporting "how much active guarantee do I have?" over linked pending transactions is a **read-model/reporting** concern, not a data-model concern. *(decided)*
- **Endorsement and bouncing** (چک) are modeled as Service/Process, not independent Entities — even when they affect other domains (credit score). *(decided)*
- **Conditional/asymmetric commitment is a general structural pattern** (one party's effect occurs early; the other's is conditional on a separate approval/event) that explains several apparently different domain instances without a new core Concept per case — before creating a concept, test whether parameterizing existing ones (status + condition + relation) already covers it. *(decided)*
- **Corrections are new records, never deletion.** A fix/reversal of a previously recorded effect is a new compensating record referencing the original; the realized state derives from the whole actual history. *(decided)*
- **Wallet-style processing without global locks.** Transaction-detail recording can be stored independent of outcome (no queue needed); each account's bookkeeping is processed with a lock on *that account* at processing time; with many responsive nodes, accounts map to nodes by consistent hashing and the transaction record travels as an event to the owning node; if the language/OS scheduler allows pinning per-CPU-core, per-account processing can run with zero locks. *(decided, worked example)*
- **Never roll back on the user's behalf.** A failed money transfer does not mean the user gives up — they retry until it works; the process should be transparent and cancellable *by the user*, not silently undone by a mechanism. *(decided)*
- **Retry may be initiated anywhere** — GUI, SDK, server, scheduler, operator, another process — and the continued execution need not return to the same place; a retry request carries the same intent and parameters but is a new occurrence, while the higher-level process stays aware of attempts and their step. *(decided)*

## Ambiguities Resolved
- Modeling Transaction as the operation itself (classical payment processing) — resolved: rejected; drafts, cancelled requests, and multi-day deferred deposits are first-class (check, LC).
- Classical ACID atomic transfer — resolved: rejected; deferred destination effects are the essence of checks, LC/escrow, and future-dated transactions; rollback hides business truth.
- Classic double-entry arbitrary account set per transaction — resolved: rejected for #2 because each side carries its own status/lifecycle, and a bag-of-changes loses the source→destination mapping (A→B 500 + A→C 500 vs A→B 700 + A→C 300 produce the same change set).

## Open Questions
1. **Source/destination multiplicity was contested.** Model A (Transaction = set of bookkeeping entries, no source→destination pairing) loses information for fee-like cases (which withdrawal pairs with which deposit); tentative lean: exactly one source and one destination, multi-party operations lifted to a higher concept. The open question — whether "one source / one destination" is a *Transfer* (a narrower concept) mistakenly conflated with *Transaction* — was declared the central unresolved item of the session; if the org lands on the restriction, it is not general accounting truth and the org must state its own reason. *(open)*
2. Should #10 (every transaction has a cause) be enforced as a mandatory edge or stay a convention?
3. Which of `account__to` (core) vs `account__by` (matching_system) owns "the account the user wants to receive into"?
4. Canonical status list (draft, authorization, ...): which are kernel defaults, which are organizational? (Status domain ownership — see [`../../knowledge/status/status.handoff.md`](../../knowledge/status/status.handoff.md).)
5. ~~`Field_FinancialTransactionUUID` keeps a legacy "financial" prefix~~ — **closed 2026-10-03 by the Khayyam conversion**: the field is now `Field_TransactionID` (accessor `TransactionID`), valued as `ThingUUID` imported from `identity/thing`. See "Khayyam conversion" below.

## Assumptions
- One-source/one-destination (#2) is the org's kernel choice under pressure-test, not claimed as universal accounting truth until open #1 is closed.
- Statuses come from the general status domain; Transaction invents no private lifecycle mechanism.

## Key Definitions Established
- Transaction: request/intent to change bookkeeping state — not booking, not operation, not payment, not (yet settled) transfer.

## Discussion (drawbacks, prior art, future) carried from the former invariants file

### Drawbacks
- One-source/one-destination (#2) multiplies transaction count for splits, fees, and batch payouts; "one business operation" semantics move to edges and are harder to query.
- No atomicity (#3, #6) means users can see intermediate states (withdrawn but not yet deposited); UI and support flows must expose this, not hide it.

### Prior art
- Double-entry bookkeeping: the balance requirement matches #3's anti-creation intent.
- Modern ledger products (e.g. Modern Treasury journal model): Transaction + per-account Entry — similar structure, but they model booked results, not pre-execution requests (#1).
- Intent-based transactions (blockchain/DeFi literature): separation of intent and execution path — aligned with #1.
- Letter of Credit / covered LC practice: source funds reserved at issuance, destination paid on conditions — real-world precedent for #3.
- Banking apps already show "requests/orders" separately from posted transactions — matches #1.

### Future possibilities
- "Cheque" as pure composition (deferred transaction + maturity rule + uri-numbered edge) — no new primitives expected; build it as a test of the model.
- Bouncing/dishonor as an event consumed by reputation/social-score analytics.
- Transaction-chain views (`followed_by`/`settles`/`exchange`) as a GUI widget module over the graph.

## Proposed Next Steps
1. Close Transfer-vs-Transaction (open #1) with an explicit org reason statement.
2. Decide mandatory vs convention for `transaction_reference_is` (open #2).
3. Reconcile `account__to` / `account__by` with matching_system.

## Related Artifacts
- [`README.md`](README.md) — graduated policies
- [`../account/account.handoff.md`](../account/account.handoff.md) — unit on account; availability
- [`../account/edges/bookkeeping/README.md`](../account/edges/bookkeeping/README.md) — realized effect; #7 quantity; Balance snapshot
- [`../../../modules-plugable/economics/matching_system/README.md`](../../../modules-plugable/economics/matching_system/README.md) — cross-unit exchange
- [`../../computer/rule/rule.handoff.md`](../../computer/rule/rule.handoff.md) — fees as rules; multi-point reaction

## Notes
- Provenance: former `accounting-invariants.md` §§1–3, 6, 10 + Discussion fragments that attach to Transaction; Organization ideas backlog Bookkeeping/Process bullets listed under Decisions.

## Khayyam conversion (2026-10-03)

Converted: `protocol/dt-uuid.kh`, `protocol/data_model.kh`, `protocol/model.kh`, `protocol/storage.kh`, `edges/account-from/protocol/data_model.kh`, `edges/reference/protocol/data_model.kh`. All six return `accept` from the Khayyam frontend.

Decisions:

- **`Field_FinancialTransactionUUID` → `Field_TransactionID`**, accessor `TransactionID`, valued as `ThingUUID` imported from `org/modules/identity/thing/protocol/dt-uuid.kh`. This closes open #5 and the same bullet in [transaction.md](transaction.md). The Go's `type UUID record_p.UUID` was **not** carried over as a domain-local `TransactionUUID ab`: the established conversion shape (rule, module, taxon, estate, text, ownership, label) is to import `ThingUUID` rather than declare an empty per-domain UUID abstraction, which rule 6 forbids. No `.kh` outside this domain imported the old name; the only importer, [`../account/edges/bookkeeping/protocol/data_model.kh`](../account/edges/bookkeeping/protocol/data_model.kh), was updated in the same pass.
- **`TransactionModel` composes memar's `Target`**, dropping Go's `Target[DataModel]` type parameter. Khayyam has no generic syntax, so "a transaction target dispatches only transaction events" is no longer expressed at the type level — recorded below rather than papered over.
- **`TransactionStorage` carries one method**, `ListAccountSideIDsByAccountID`, the only uncommented entry in the Go `StorageServices`. `Save` and `Find_TransactionID_BY_AccountIDs` stay commented in the clue block; the latter carries the Go author's own `TODO:::` ("is it worth to uncomment?"). `[]fa_p.UUID` became `Array_ThingUUID` (the named array type imported from `identity/thing`), not a Go `[]T` re-declaration.

Left unconverted, with reasons:

- `services/errors.kh`, `services/service-register.kh`, `services/service-get-transaction.kh`, `services/service-find-transactions-by-day.kh`, `services/register-transaction/business-services.kh`, `internal/storage/ganjine.kh` — **old, non-architectural code** under the migration map's disposition table, not conversion candidates. They are a pre-kernel per-user `FinancialTransaction` record: a hand-rolled `[]byte` capsule with manual Syllab/JSON codecs, a daily-hash index over `libgo/pehrest`, `libgo/ganjine` object-directory storage, a `Lock`/`UnLock` pair whose own comments read `// TODO::: real lock!`, and a SEP POS integration keyed on the first two characters of a `PosID` string. They also model `UserID` + `Amount` + `Balance` on the transaction itself — exactly the duplication [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md) §7/§8 removed, and exactly the `financial` framing open #5 was about. Disposition: delete or re-model from [transaction.md](transaction.md), not convert.
- `edges/account-to/` and `edges/conditional/` — documentation only, no protocol sources in the tree.

Open from this pass:

- **`TransactionModel` no longer constrains its events.** Either memar grows a per-data-type target abstraction, or the transaction domain states in prose that only transaction events reach a transaction target.
- **`edges/account-from`'s record declares only `Observer_Quantity`.** The edge is `(transaction)-[:account__from]->(account)`, but neither endpoint appears in `TransactionAccountFromDataModel`, so the record cannot be traced to the transaction or the account it moved quantity for. The Go had the same gap (only `decimal_p.Field_Quantity`), so this is a source gap, not a conversion loss. The same edge has no `account-to` counterpart file, so the two sides are not modelled symmetrically.
- **`edges/account-from` / `account-to` naming.** The documents call the two sides *from*/*to* while the Go package for the from side is `gives_p` and the prose still uses the pre-matching_system `takes` wording ([transaction.md](transaction.md) open #1). No code decision was taken.
