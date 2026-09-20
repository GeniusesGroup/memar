# Rule Handoff (economics-consumer decisions)

## Topic & Purpose
Decisions about how Rules interact with Transactions and Accounts, captured during economics modeling and the Organization ideas backlog. The general Code/Rule principle lives in Memar; this handoff holds org-application decisions that must not be lost when category-level economics files were retired.

## Status
Active — mechanics already partly in [`README.md`](README.md); this file preserves backlog provenance and fee/constraint decisions.

## Decisions

### From accounting invariants (formerly `modules/economics/accounting-invariants.md`)

#### 9. Fees and charges are rules producing transactions
A fee policy ("1% up to 10") is a Rule reacting to a transaction, producing an additional transaction (possibly conditional on the original's outcome). It is not a field on the transaction and not a second destination. When the fee applies — on attempt, on success, on failure, after authorization, after settlement — is organization policy inside the Rule; the kernel does not fix it.

Rationale: fee as a second destination was rejected — it breaks one-source/one-destination on Transaction and loses "fee depends on the original transaction's outcome".

### From Organization ideas backlog

- **Rules react at multiple points**, not only as preconditions: before processing, after processing, on status change, in response to a service, or to another Transaction. "condition_is" is one relation among Rule's possible ones. *(decided)*
- **A rule's operational effect** (e.g. blocking part of an asset) is recorded as a distinct Transaction after the main one — the rule never mutates the incoming Transaction itself. *(decided)*
- **Fee is a policy, not a baked-in transaction.** Three shapes were examined: (1) fee as its own Transaction, (2) an extra destination inside the same Transaction, (3) a Rule/Process that conditionally generates a second Transaction per policy — fee-on-attempt / fee-on-success / fee-on-failure / after-authorization / after-settlement. Option (3) preferred because it does not jam the fee into the Transaction concept. *(decided)*
- **Modules like Discount are event-attached:** something must emit the event and the module listens; no new Event data model is needed — a Type declares itself an EventTarget and uses the existing request/response models. *(decided)*
- **Core never knows Rule** (placement criterion, owned here as a Rule-domain consumer rule): Core domains do not reference the rule domain directly; generic edges (e.g. `(transaction)-[:condition_is]->(rule)`) connect subjects to rule nodes, and the rules-engine decides semantics. *(decided)*

## Open Questions
- Unresolved Memar-owned Rule representation / conflict-resolution / temporal validity questions remain in Memar — do not silently answer them here (see README).

## Related Artifacts
- [`README.md`](README.md)
- [`../../economics/transaction/transaction.handoff.md`](../../economics/transaction/transaction.handoff.md)
- [`../../../modules-plugable/economics/restriction/README.md`](../../../modules-plugable/economics/restriction/README.md)

## Notes
- Drawback carried from invariants: #7-style quantity purity pushes partial fulfilment and fees into rules/pluggable modules; the kernel cannot express "book half of this transaction" as a mutation of the original.
