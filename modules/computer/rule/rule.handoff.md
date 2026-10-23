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

### From Rule Research 001 (2026-10-18, agent proposals, nothing ratified)
Each entry: the question, the recommended default, what it blocks. Ordered by what they change: those that change what the domain is first. Reasoning, twelve scenarios and seven rival models are in [Rule Research 001](rule.research.001.md#open-questions). The research answers, as its own labelled proposals, the Memar-carried questions above; it does not claim them settled.
1. **Is the rule domain the home of the rule node (identity, statement by reference, interval, attachment, consequence trail) rather than the engine or a classification on content?** Default: the node domain, model M3. Blocks: the rewrite of the opening of [rule.md](rule.md), `RuleModel` beyond `ThingModel` (Khayyam rule 6), every sibling's kernel list.
2. **Who owns `condition_is`: one defining document in this domain, each consumer keeping only an event target naming its points?** Default: one, here; one stored direction (subject to rule). Blocks: the three `conditional` folders, the ten sibling kernel lists, survey Q3, B4 and D14, the `authorization` merge.
3. **What may a rule do at a before-point, and what happens when the engine is unavailable?** Default: three modes (observe, accompany, refuse); only refuse stops the subject, as a response of the subject's own service; fail-open or fail-closed stated per attachment. Blocks: `synchronous`, restriction, authorization, the sentence "never modifies".
4. **Is an amendment a new rule that supersedes the old, and does validity keep both an effective and a recorded time?** Default: yes to both. Blocks: temporal validity (Memar-carried), the law freeze, `time_limit`, the sibling convention on time.
5. **Where is the Code/Rule boundary?** Default: the ontology test (no organization could run the domain with it off means Code). Blocks: cycle guards of task and group, candidate kernel rules of account and product.
6. **Does the node hold only the statement's reference, the normative claim staying in the subject's own module; is field-indexed lookup derived data?** Default: reference only; lookup derived and pluggable. Blocks: the Rule storage idea above, `code`, `uml`, law `computer_code`.
7. **Conflict resolution: precedence stated by an authority over both rules, no silent specificity?** Default: yes. Blocks: price cap versus promotion, discount versus voucher (survey E1).
8. **Idempotency, ordering, cascade: one firing per (rule, trigger); order by precedence then declared time; a consequence never re-enters its own rule; a depth cap?** Default: yes to all. Blocks: double-fire, fees, schedules.
9. **Who may declare, attach and read a rule?** Default: the owner declares (software only under a named principal); attaching needs authority over the subject; the subject's owner can always learn that a rule governs it. Blocks: the authorization merge, listener sprawl, rules about rules.
10. **May a rule attach to a class (label, type, edge kind) and not only an instance?** Default: yes, by label, with authority over its scope. Blocks: initiator-event and initiator-service, "all future accounts".
11. Decided (owner, 2026-10-20): none of the three names is a status; [rule.md → Status](rule.md#status) states it. Whether the rule has a lifecycle vocabulary stays with question 4.
12. **Is a rule's identity the same as its module identity when developed as a module?** Default: one `ThingUUID`; module is a classification. Blocks: `Field_ModuleID` composition.
13. **Does the domain record every evaluation or only outcomes?** Default: outcomes; the rest to the log-listener. Blocks: audit, volume.
14. **Schedules: is a missed run made up once or skipped; whose clock decides?** Default: the rule states it; due and fire time recorded. Blocks: `repeatable`, payroll.
15. **Is where a rule may run an acquired fact of its owner (execution-scope)?** Default: yes. Blocks: the two `execution-limit` folders, data residency.
16. **May a rule's consequence be a task for people?** Default: yes; the check is its own rule. Blocks: human-executed rules, task acceptance check.
17. **Is a set of rules a thing with identity, and may an organization adopt an authority's published rule instead of copying it?** Default: yes to both, adoption through `follow`. Blocks: the law digest, tax libraries.
18. **Must a rule pass its own tests before it is in force?** Default: optional, except the "no input can satisfy it" check for rules a law names. Blocks: rule-test capability.

### Contradictions reported by Rule Research 001 (not resolved)
See [Contradictions found](rule.research.001.md#contradictions-found): direction of the governing relation; `synchronous` against "never modifies or rolls back"; three `conditional` folders and five statements of permission; `uml.md` naming a notation while describing actions; sibling kernels counting the attachment as their own element; kernel documents naming the rule domain; Memar's by-subject home against this domain's storage; overlap with Memar's process rule and engine; status names without a classification; edge folders without Placement and Open questions.

## Proposed Next Steps (from Rule Research 001)
1. Owner answers questions 1 to 4 of the research (what the domain is, who owns `condition_is`, what a rule may do at a before-point, amendment and the two times).
2. If 2 is accepted: write `edges/condition_is` with point, mode, limit, who attaches, what removal does; reduce the transaction, invoice and request `conditional` documents to pointers; each consumer names its event points.
3. Reclassify the edge folders as in the research's mapping (trigger-binding, schedule, manual-call, execution-scope, checking, rationale); give each Placement and Open questions (survey T4).
4. Declare what [rule.md → Status](rule.md#status) makes of the Go source's three status names: `AutoGenerated` a label on the rule, in this module's `labels/`, and the usage a reading derived from firings, each declared where its kind is. The `status/` folder is removed (2026-10-23, task 20261023-T100229Z-17920).
5. Draft `precedence` and `rule-set` once questions 7 and 17 are answered; consider `rule-test` and `adoption`.
6. Do not edit the Model or Policies of rule.md, move folders or write `.kh` on this evidence alone.

## Related Artifacts
- [`rule.research.001.md`](rule.research.001.md)
- [`README.md`](README.md)
- [`../../economics/transaction/transaction.handoff.md`](../../economics/transaction/transaction.handoff.md)
- [`../../../modules-plugable/economics/restriction/README.md`](../../../modules-plugable/economics/restriction/README.md)

## Notes
- Drawback carried from invariants: #7-style quantity purity pushes partial fulfilment and fees into rules/pluggable modules; the kernel cannot express "book half of this transaction" as a mutation of the original.

## Go → Khayyam conversion (protocol layer)

### Status
Three `.kh` files accept under the Khayyam frontend; one composition is blocked on `computer/software`.

### Converted
- `protocol/dt-uuid.kh` — `Field_RuleID` + `RuleID () (t ThingUUID)`
- `protocol/model.kh` — `RuleModel`, composing `ThingModel` and `Field_RuleID`
- `edges/authorization/protocol/dt-authorized-by.kh` — `Field_AuthorizedBy` + `AuthorizedBy () (t ThingUUID)`

### Unblocks

`[rights/delegate](../../../rights/delegate/delegate.handoff.md)`: `DelegateDataModel` composes nothing for the rule it delegates to, because `computer/rule` declared no `Field_RuleID`. That is now declared, and its handoff records the one-line change:

```
tp Field_RuleID in "modules/computer/rule/protocol/dt-uuid.kh"
```

`[rights/contract](../../../rights/contract/contract.handoff.md)`: `ContractTermsModule` returns a bare `ThingUUID` where the Go's `Data` struct had `moduleID module_p.UUID`. `computer/module` now declares `Field_ModuleID`, and that field's accessor is where the bare return becomes a composition. Not this domain's file to change.

### Decisions

1. **`Field_RuleID` returns `ThingUUID` and no `RuleUUID` abstraction was declared.** The Go wrote `type UUID record_p.UUID` — the repository-wide identifier alias, of which about ninety copies exist and which is owned by [identity/thing](../../identity/thing/protocol/dt-uuid.kh) as `ThingUUID`. Adding a rule-domain value abstraction would have been a second owner of one concept.
2. **`RuleModel` composes `Field_RuleID`, which the Go's `Model` did not.** The Go's `Model` was `thing_p.Model` + `software_p.Model` only. This follows the pattern [knowledge/edge/protocol/model.kh](../../knowledge/edge/protocol/model.kh) already set, where `EdgeModel` carries `Field_EdgeID` although the Go's `Model` did not, and it is what [rule.md](./rule.md) needs: "which entities are subject to Rule X" is answerable by traversal only if the rule node knows its own identity. A reviewer who disagrees loses one line.
3. **`Field_AuthorizedBy` returns `ThingUUID` rather than the rule domain's type.** The Go's `AuthorizedBy() rule_p.UUID` reached the rule domain's identifier alias, and [authorization.md](edges/authorization/authorization.md)'s TODO asks whether `label_p.UUID` or `form_p.UUID` should serve as the rule identifier instead. The repository's UUID-ownership decision answers it: those are one concept, not alternatives, so the answer is no and `ThingUUID` is what the field returns. The TODO's own wording (`RuleUUID??`) is a pre-decision spelling of the question.

### Findings

1. **`RuleModel` cannot compose `SoftwareModel`.** The Go's `Model` embedded `software_p.Model`, and [computer/software](../../computer/software/protocol/model.kh) is not converted. That file's Go is `thing_p.Model` with a commented `Modules() []module_p.UUID`, so what converts as `SoftwareModel` is `ThingModel` alone — a composition that would add nothing over `ThingModel` until `computer/module` decides whether a software carries its modules (see `module.handoff.md`). Declaring `SoftwareModel` here would be a second abstraction claiming a concept the software domain owns. **What is needed elsewhere:** `computer/software/protocol/model.kh` declares `tp SoftwareModel ab { ThingModel }`, and `RuleModel` then adds it to its composition block.
2. **The extraction pass found nothing to move.** None of this domain's `.kh` files carries a Go comment with explanatory text — `dt-uuid.kh`, `model.kh` and `dt-authorized-by.kh` are bare declarations. [rule.md](./rule.md) is therefore unchanged by the conversion, which is the correct outcome and not an omission.

### Open Questions added by the conversion
1. Decided (owner, 2026-10-20): a Rule's three names are a label and a derived reading, not statuses ([rule.md → Status](rule.md#status)).
2. **Whether a software carries its modules.** The Go's `software_p.Model` has `Modules() []module_p.UUID` commented out. `RuleModel` is where that would surface once `computer/software` converts — a rule governs software, and "which software a rule governs" is the same question [rule.md](./rule.md) answers by traversal.
3. **Whether `Field_AuthorizedBy` is a field at all.** [authorization.md](edges/authorization/authorization.md) gives the edge a `## Fields` heading and leaves it empty, and models the relation as `(thing)-[:authorization_by]->(rule)`. A field accessor returning the rule's identifier and an edge are two ways to say one thing; which one this repository wants is not written down.
