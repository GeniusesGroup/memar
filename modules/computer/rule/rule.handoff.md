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
- **A law is typically realized as Rule nodes.** [Law](../../rights/law/law.md) is the signed instrument; this module's Rule is how it executes. They are layers. The Rule set named by a law's `computer_code` is inside that law's payload digest, so adding a Rule after voting is a new law. *(decided — owner, law-type review 2026-09-21)*

## Open Questions
- Unresolved Memar-owned Rule representation / conflict-resolution / temporal validity questions remain in Memar — do not silently answer them here (see README).

## Related Artifacts
- [`README.md`](README.md)
- [`../../economics/transaction/transaction.handoff.md`](../../economics/transaction/transaction.handoff.md)
- [`../../../modules-plugable/economics/restriction/README.md`](../../../modules-plugable/economics/restriction/README.md)

## Notes
- Drawback carried from invariants: #7-style quantity purity pushes partial fulfilment and fees into rules/pluggable modules; the kernel cannot express "book half of this transaction" as a mutation of the original.

## Go → Khayyam conversion (protocol layer)

### Status
Three `.kh` files accept under the Khayyam frontend; one is deliberately left unconverted and one composition is blocked on `computer/software`.

### Converted
- `protocol/dt-uuid.kh` — `Field_RuleID` + `RuleID () (t ThingUUID)`
- `protocol/model.kh` — `RuleModel`, composing `ThingModel` and `Field_RuleID`
- `edges/authorization/protocol/dt-authorized-by.kh` — `Field_AuthorizedBy` + `AuthorizedBy () (t ThingUUID)`

### Unblocks

`[rights/delegate](../../../rights/delegate/delegate.handoff.md)`: `DelegateDataModel` composes nothing for the rule it delegates to, because `computer/rule` declared no `Field_RuleID`. That is now declared, and its handoff records the one-line change:

```
tp Field_RuleID in "org/modules/computer/rule/protocol/dt-uuid.kh"
```

`[rights/contract](../../../rights/contract/contract.handoff.md)`: `ContractTermsModule` returns a bare `ThingUUID` where the Go's `Data` struct had `moduleID module_p.UUID`. `computer/module` now declares `Field_ModuleID`, and that field's accessor is where the bare return becomes a composition. Not this domain's file to change.

### Decisions

1. **`Field_RuleID` returns `ThingUUID` and no `RuleUUID` abstraction was declared.** The Go wrote `type UUID record_p.UUID` — the repository-wide identifier alias, of which about ninety copies exist and which is owned by [identity/thing](../../../identity/thing/protocol/dt-uuid.kh) as `ThingUUID`. Adding a rule-domain value abstraction would have been a second owner of one concept.
2. **`RuleModel` composes `Field_RuleID`, which the Go's `Model` did not.** The Go's `Model` was `thing_p.Model` + `software_p.Model` only. This follows the pattern [knowledge/edge/protocol/model.kh](../../../knowledge/edge/protocol/model.kh) already set, where `EdgeModel` carries `Field_EdgeID` although the Go's `Model` did not, and it is what [rule.md](./rule.md) needs: "which entities are subject to Rule X" is answerable by traversal only if the rule node knows its own identity. A reviewer who disagrees loses one line.
3. **`Field_AuthorizedBy` returns `ThingUUID` rather than the rule domain's type.** The Go's `AuthorizedBy() rule_p.UUID` reached the rule domain's identifier alias, and [authorization.md](edges/authorization/authorization.md)'s TODO asks whether `label_p.UUID` or `form_p.UUID` should serve as the rule identifier instead. The repository's UUID-ownership decision answers it: those are one concept, not alternatives, so the answer is no and `ThingUUID` is what the field returns. The TODO's own wording (`RuleUUID??`) is a pre-decision spelling of the question.

### Findings

1. **`RuleModel` cannot compose `SoftwareModel`.** The Go's `Model` embedded `software_p.Model`, and [computer/software](../../../computer/software/protocol/model.kh) is not converted. That file's Go is `thing_p.Model` with a commented `Modules() []module_p.UUID`, so what converts as `SoftwareModel` is `ThingModel` alone — a composition that would add nothing over `ThingModel` until `computer/module` decides whether a software carries its modules (see `module.handoff.md`). Declaring `SoftwareModel` here would be a second abstraction claiming a concept the software domain owns. **What is needed elsewhere:** `computer/software/protocol/model.kh` declares `tp SoftwareModel ab { ThingModel }`, and `RuleModel` then adds it to its composition block.
2. **`status/rule-status.kh` is left unconverted.** It holds three status labels and a terminator — `Status_AutoGenerated`, `Status_PartlyUsed`, `Status_FullyUsed`, `End` — and nothing else. A `.kh` that is only label vocabulary stays as it is; that is the same ground `identity/organization/edges/` and the rights label folders were left on. Nothing here is a method, a composition, or an identity field.
3. **The `status/` folder has no document and [rule.md](./rule.md) does not place it.** Every other folder in this domain is a documented edge; `status/` is a bare `.kh` with no `README.md` and no `<name>.md`, so there is nothing saying what a rule's status *means* — only three names. The migration map's high-confidence kind-error class also puts statuses under `edges-loop/`, not a folder of their own, so the placement is undecided in two directions at once. **What is needed:** a decision on what these three statuses classify and where the folder belongs; then a `status/rule-status.md`, and the vocabulary read through `knowledge/status` like any other label set.
4. **The extraction pass found nothing to move.** None of this domain's four `.kh` files carries a Go comment with explanatory text — `dt-uuid.kh`, `model.kh` and `dt-authorized-by.kh` are bare declarations, and `rule-status.kh` is bare constants. [rule.md](./rule.md) is therefore unchanged by the conversion, which is the correct outcome and not an omission.

### Open Questions added by the conversion
1. **What does a Rule's status classify?** `Status_PartlyUsed` and `Status_FullyUsed` read as usage of a rule in the graph; `Status_AutoGenerated` reads as provenance. If one list holds both a lifecycle and a provenance, it is two classifications and the vocabulary should split. Nobody has said which.
2. **Whether a software carries its modules.** The Go's `software_p.Model` has `Modules() []module_p.UUID` commented out. `RuleModel` is where that would surface once `computer/software` converts — a rule governs software, and "which software a rule governs" is the same question [rule.md](./rule.md) answers by traversal.
3. **Whether `Field_AuthorizedBy` is a field at all.** [authorization.md](edges/authorization/authorization.md) gives the edge a `## Fields` heading and leaves it empty, and models the relation as `(thing)-[:authorization_by]->(rule)`. A field accessor returning the rule's identifier and an edge are two ways to say one thing; which one this repository wants is not written down.
