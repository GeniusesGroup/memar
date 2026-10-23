# Transaction Research 001 — What the transaction domain is for, and what is kernel and what is pluggable

## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Starting Evidence](#starting-evidence)
- [Methodology](#methodology)
- [Findings](#findings)
  - [1. What the domain is for](#1-what-the-domain-is-for)
  - [2. Minimal kernel and what must be pluggable](#2-minimal-kernel-and-what-must-be-pluggable)
  - [3. Rival models](#3-rival-models)
  - [4. What the domain must own, as requirements questions](#4-what-the-domain-must-own-as-requirements-questions)
  - [5. How the existing edge folders map](#5-how-the-existing-edge-folders-map)
  - [6. Missing edges and modules](#6-missing-edges-and-modules)
  - [7. Test scenarios](#7-test-scenarios)
  - [Contradictions found](#contradictions-found)
  - [Reconciliation with the sibling researches](#reconciliation-with-the-sibling-researches)
- [Recommendation (unratified)](#recommendation-unratified)
- [Open Questions](#open-questions)
- [Related Artifacts](#related-artifacts)

## Status
Active

Nothing here is ratified. Every proposal carries a confidence mark in the sense of [Handoff Practice](../../knowledge/documentation/handoff/handoff.practice.md): Decided, Tentative, Explored (explored but unresolved), or Deferred. **No item below is Decided by this research.** Items already Decided in the domain documents are cited as such and are not re-argued: a transaction is a request, not an operation; at most one source and one destination (Decided as the kernel's choice, under test in [open 1](transaction.handoff.md#open-questions)); withdrawal precedes deposit and delay is allowed; no rollback, a correction is a new transaction; every transaction has a cause by reference; booked quantity equals requested quantity; the unit belongs to the account; cross-unit intent is two same-unit transactions ([transaction.handoff.md](transaction.handoff.md#decisions), [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md#policies-rules), [account.handoff.md](../account/account.handoff.md#decisions), [matching_system.md](../../../modules-plugable/economics/matching_system/matching_system.md#cross-unit-exchange-formerly-accounting-invariants-5)).

## Question and Goals
- **Questions:**
  - What is the transaction domain for, once tested against cases that are not a plain bank transfer? — finding 1 (Tentative).
  - Which part is kernel and which pluggable under the placement tests of [Modules → Placement](../../modules.md#placement)? — finding 2 (Tentative).
  - Which rival model survives the cases? — finding 3; the choice is the owner's.
  - What must the domain own, and what is unsettled? — finding 4, as requirement questions.
- **Goals:** a sharper reading of what a transaction is responsible for; a kernel small enough to defend; a placement for each existing folder; the missing pieces named; a short owner list with defaults and what each blocks; the meeting points with [account](../account/account.md) and [invoice](../invoice/invoice.md) reported, not edited.
- **Scope:** `modules/economics/transaction` and its four edge folders, plus the transaction-touching folders in `modules-plugable/economics` and `modules/knowledge/status` (read, not changed). Out of scope: the domain Model and Policies, any `.kh` file, moving or deleting any folder, and re-arguing what the domain documents mark Decided.

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — Questioner, Goal-setter, Reviewer (Not yet reviewed). He asked for conceptual development of the base domains while away and unavailable for questions (survey session `20261014T071207Z-28148-0`).
- An AI agent (Claude, model `claude-sonnet-5-5` as reported by the runtime; [CONTRIBUTORS.md](../../../CONTRIBUTORS.md) has no entry for it) — Researcher, session `20261018-T184247Z-6508`.

## Starting Evidence
Read in full in this session: [transaction.md](transaction.md), [transaction.handoff.md](transaction.handoff.md), the four edge documents ([account-from](edges/account-from/account-from.md), [account-to](edges/account-to/account-to.md), [conditional](edges/conditional/conditional.md), [reference](edges/reference/reference.md)), and the converted protocol files (`protocol/dt-uuid.kh`, `data_model.kh`, `model.kh`, `storage.kh`, `edges/account-from/protocol/data_model.kh`, `edges/reference/protocol/data_model.kh`). The domain has no changelog; this research creates it. `README.md` holds only the text `transaction.md`. The legacy `services/`, `internal/` folders were listed, not read (the handoff classes them as old non-architectural code).

Neighbours read at the cited file: [account.research.001.md](../account/account.research.001.md) in full; [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md); [invoice.md](../invoice/invoice.md); the pluggables [matching_system](../../../modules-plugable/economics/matching_system/matching_system.md) with its `deal`, `trade`, `exchange`, `instant_withdrawal` and `account-by` documents, [settlement](../../../modules-plugable/economics/settlement/settlement.md) with `endorsement` and `guarantor`, [restriction](../../../modules-plugable/economics/restriction/restriction.md), [credit](../../../modules-plugable/economics/credit/credit.md), [cash_transaction](../../../modules-plugable/economics/cash/edges-shortcut/cash_transaction/cash_transaction.md), [authorize_by_card](../../../modules-plugable/economics/card/edges/authorize_by_card/authorize_by_card.md), [fraud](../../../modules-plugable/economics/fraud_detection/edges/fraud/fraud.md), [refund](../../../modules-plugable/economics/refund/refund.md), [voucher](../../../modules-plugable/economics/voucher/voucher.md), the [price-index](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales) deferred-payment section; the status domain ([status.md](../../knowledge/status/status.md), `failed`, `read-only`, `block`, `request`, `approval_needed`, [request-status](../../knowledge/status/edges/request-status/request-status.md)).

**Not read, so unverified:** the bodies of `securities`, `pos`, `payroll`, `wage`, `distribution`, `subsidy`; `rights/delegate`, `management/authorization`; the `rule` domain beyond its location; `rights/case` beyond what the transaction handoff quotes; the Go legacy behind the `.kh` residue blocks; the sibling researches for product, task, content and text beyond the lines found by searching them for transaction-relevant words (stated at each use in the reconciliation); the group, thing and user researches only at their open-question lists. The owner-question catalogue ([E6](../../../temp/sessions/20261014T071404Z-26308-0/report.md)) and survey reports were read by search for "transaction", as claims.

## Methodology
One reasoning pass by one agent. No second cognitive system was consulted and no organization was asked. The scenarios are reasoning from general knowledge of practice in several countries and industries, not retrieval and not observation; a custom, a figure or a named system is illustrative and nothing in the findings rests on its exact value.

1. **Memar's criteria,** read from the documents: [Modularity → Core Structure and Optional Modules](../../knowledge/modularity/modularity.md#core-structure-and-optional-modules), [Pluggable Behavior](../../knowledge/modularity/modularity.md#pluggable-behavior), [Foundational Concepts Should Remain Few](../../knowledge/modularity/modularity.md#foundational-concepts-should-remain-few), [What Earns Foundational Status](../../knowledge/modularity/modularity.md#what-earns-foundational-status), [Capability Completeness](../../knowledge/modularity/modularity.md#capability-completeness), [Event as a Module Capability](../../knowledge/modularity/modularity.md#event-as-a-module-capability); [Modeling → Concept Existence vs. Model Existence](../../../docs/modeling.md#concept-existence-vs-model-existence), [Modeling State Change as Events](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates), [Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels), [A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once); [Modeling Practice → The Modeling Workflow](../../../docs/modeling.practice.md#the-modeling-workflow). The placement tests are those of [Modules → Placement](../../modules.md#placement).
2. **Terms, defined before use.** Where Memar defines no term, its ordinary meaning applies.

| Term | Meaning used here | Governing source |
|---|---|---|
| **Transaction** | A request by one or more users for a bookkeeping change; a request, not an operation; a `thing`. | [transaction.md](transaction.md) |
| **Booking / bookkeeping record** | The realized effect of a transaction on one account; at most one per affected account; never edited. | [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md#policies-rules) |
| **Kernel** | A concept whose removal would force a foundational type to be fabricated or distorted; not importance. | [What Earns Foundational Status](../../knowledge/modularity/modularity.md#what-earns-foundational-status) |
| **Pluggable, capability** | An optional module attached through an explicit relationship, owning relation, rules and processing together. | [Capability Completeness](../../knowledge/modularity/modularity.md#capability-completeness) |
| **Status** | A loop-edge on the record, defined once in the status domain; a move between statuses is an event a rule may allow or block. | [status.md](../../knowledge/status/status.md#what-a-status-is) |
| **Acquired / discovered** | Stated by an external source and not recomputable, versus derived from acquired data. | [Acquired Data vs. Discovered Data](../../../docs/modeling.md#acquired-data-vs-discovered-data) |
| **Intent / attempt / effect** (agent terms) | Intent: what was asked (the transaction). Attempt: one occurrence of trying to carry it out (a service request, carried on a bookkeeping record as `Field_RequestID`). Effect: the booking. The three are the handoff's "a retry ... is a new occurrence" made explicit. | [transaction.handoff.md](transaction.handoff.md#decisions) (retry bullet); [bookkeeping.md → Fields](../account/edges/bookkeeping/bookkeeping.md#fields) |
| **In-flight quantity** (agent term) | Quantity booked out of a source whose destination effect has not yet been booked. | agent proposal, from decision 3 |
| **Requester / authorizer** (agent terms) | Who asks for a movement versus who holds authority over its source. The documents say only "one or more users". | agent proposal |
| **Counterpart account** | An account that is the other side of creation or destruction. | [account.research.001.md](../account/account.research.001.md#2-minimal-kernel-and-what-must-be-pluggable) (proposal, unratified) |

**Limits.** One agent, one pass. What a bank, regulator or court does in a scenario is the researcher's judgment.

## Findings
### 1. What the domain is for

**Statement (agent, Tentative).** The transaction domain answers one question for the rest of economics: *what movement of one quantity between at most two accounts has been asked for, by whom, why, under which conditions, and how far has it got?* It owns the **memory of requested quantity movement and its path to realization**: the intent, its cause, its conditions, its status events, and its links to other intents. It deliberately decides nothing about what has actually happened (that is the account's bookkeeping record), who may instruct a debit (authority), what may leave now (restriction), what is owed (invoice, contract), or what the quantity means to a business.

**What the documents already say (source).** A transaction is a `thing` with `Quantity`, optionally one source and one destination, a realized-effect edge owned by the account domain, a mandatory-by-convention reference to its cause, and a `condition_is` edge to a rule ([transaction.md → Model](transaction.md#model)). Execution lives in processors reacting to status and rules, never in the node. History is append-only ([transaction.handoff.md](transaction.handoff.md#decisions), decisions 1, 6, 10).

**The finding that moves the domain (agent, Tentative).** The documents defend the request/effect split with care and say little about the request itself, so the following are in no document:
- **Who asked, and who may authorize the debit.** The model says "one or more users"; a direct debit, a court levy and a cheque all separate the asker from the holder of authority over the source (S5, S8, S1).
- **What is true while the quantity is between its two effects.** Decision 3 allows withdrawal now and deposit days later and also requires conservation. Between the two the quantity is in no account (S2).
- **What freezes when.** The reference is immutable after registration and `account__to` may not change once a record exists, but the quantity, the source, the conditions and the statuses have no stated freeze point, and a draft may be "deleted" while no booking is ever deleted (Contradictions 1, 9).
- **How intents link.** The chain relations (`followed_by`, a compensation link) are relied on by decisions 2 and 6 and defined nowhere (Contradiction 5).

**The completable classification sentence** ([Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels)): *a thing may be classified as a transaction because a requester asked, at a time, for a quantity to move from at most one account to at most one account, for a cause; and therefore it can be conditioned, approved or refused, linked to other transactions, and realized by bookkeeping at most once on each side.* A relation that cannot complete the sentence is not a transaction relation (finding 5).

**What the domain is not for (agent, with sources).** Not the payment (a payment is one cause, [reference](edges/reference/reference.md)); not the operation ([decision 1](transaction.handoff.md#decisions)); not the claim (invoice: "a statement of what is claimable", [invoice.md](../invoice/invoice.md#definition-in-memar)); not the commitment schedule of an instalment plan (see model R5); not the instrument (a cheque is composition, [Future possibilities](transaction.handoff.md#discussion-drawbacks-prior-art-future-carried-from-the-former-invariants-file)); not the order book (matching_system).

#### Scenarios
Eleven cases; the first nine are load-bearing. Names and figures are illustrative.

**S1. A post-dated cheque (Iran's sayyad-registered cheque, a German Scheck, a Pakistani post-dated cheque).** A buyer hands a cheque dated three months on; the seller endorses it to a supplier; at maturity it clears or bounces.
- *Obvious model:* a payment in `pending`.
- *What breaks:* the request is signed now but must not be processed before a date; the right to be paid moves by endorsement without any money moving; a bounce has consequences (credit score) and the cheque is a numbered instrument. The endorsement document says one transaction may have several endorsements that "split first transaction quantity" while the original is suspended ([endorsement](../../../modules-plugable/economics/settlement/edges/endorsement/endorsement.md#policies-rules)), yet booked quantity equals requested quantity ([bookkeeping.md §7](../account/edges/bookkeeping/bookkeeping.md#7-booked-quantity-equals-requested-quantity)): what is the original's quantity after a split?
- *Asks of the domain:* a not-before condition that is a rule, not a field; requester equal to payer; a cause and an instrument number as `uri`; the endorsement chain owned by its pluggable. The handoff already predicts "no new primitives expected".

**S2. A letter of credit and an escrow (international trade; an online-marketplace escrow such as Alipay's; an Iranian escrow deposit).** The buyer's funds are committed at issuance; the seller is paid when documents or delivery are confirmed; failure returns the funds.
- *Obvious model:* one transaction, withdrawal now, deposit later (decision 3).
- *What breaks:* during the wait the quantity is in no account, yet in every real case some party holds it and can be frozen, sued or insolvent. A freeze (restriction) needs an account to act on. "Return the funds" is a new transaction from where?
- *Asks of the domain:* an answer to what the in-flight quantity is (finding 3, smaller choice 1; owner question 4). The tree has a hint in [account-from.md](edges/account-from/account-from.md#policies-rules): "move inventory to middle temp accounts".

**S3. A cross-border transfer through correspondents, and a hawala chain.** Sender pays 1,000; two intermediaries each deduct a fee; the beneficiary receives 985; one hop fails after two days and the amount returns.
- *Obvious model:* one transfer of 1,000.
- *What breaks:* decision 2 and bookkeeping §7 force each hop and each fee to be its own transaction. The sender's one intent has no node; "did my payment arrive?" is a traversal over a chain; a failed hop must return the earlier hops' effects by new transactions, never by rollback (decision 6). Who is the requester of hop 2: the sender, or the bank acting for the sender?
- *Asks of the domain:* a way to say "these are one intent" without a container concept unless one is needed; a chain relation defined once; hop requesters as acting-for (delegation).

**S4. A split payout (a marketplace pays a seller 90, the platform 7, tax 3; a payroll run of 500 salaries; a restaurant bill split by five diners).** One payer intent, several destinations, sometimes all-or-nothing.
- *Obvious model:* one transaction with three destinations (the journal shape).
- *What breaks:* decision 2 forbids it ("A→B 500 + A→C 500 and A→B 700 + A→C 300 produce the same change set"); but the all-or-nothing wish is then a property of a set of transactions that no node owns. Payroll is already read as invoices ([invoice.md](../invoice/invoice.md#definition-in-memar)), so for payroll the higher concept exists; for a marketplace payout it may not.
- *Asks of the domain:* whether the "higher concept" in [open 1](transaction.handoff.md#open-questions) is something that already exists (invoice, task, contract, case) or something new (model R3).

**S5. A direct debit, a standing order and a subscription (SEPA mandates, India's e-mandates, a Japanese convenience-store bill).** The payer authorizes once; the payee pulls varying amounts monthly; the payer may revoke.
- *Obvious model:* a recurring transaction.
- *What breaks:* each pull is a fresh request by the payee against an account whose holder gave a standing authority; the amount is not known at authorization; revocation applies to future pulls only. The requester is not the authorizer. Recurrence is time-driven creation, not an attribute of one transaction.
- *Asks of the domain:* the requester/authorizer split; the standing authority is delegation (not the transaction's); creation on a clock is a rule or a task recurrence ([task research](../../management/task/task.research.001.md) places recurrence in a pluggable of its own; read by search only).

**S6. Barter and a currency swap (goods for services; "give 50 dollars to get 40 euros").** Two parties each want the other's unit, with a deal possibly filled in parts.
- *Obvious model:* one transaction with two units.
- *What breaks:* unit is on the account, so the swap is two same-unit transactions linked by `exchange`/`deal` ([matching_system.md](../../../modules-plugable/economics/matching_system/matching_system.md)); with no atomicity, one leg may complete and the other fail. [instant_withdrawal](../../../modules-plugable/economics/matching_system/edges-loop/instant_withdrawal/instant_withdrawal.md) books the source side at once so the second leg cannot later be impossible.
- *Asks of the domain:* nothing new for the kernel if both legs withdraw first (each side's source is booked at registration), which turns a swap into two escrows; this again raises S2's question.

**S7. A card payment: hold, capture, chargeback (hotel pre-authorization of 200, capture of 180, a chargeback ninety days later).** 
- *Obvious model:* one transaction whose amount is edited.
- *What breaks:* the hold is a reservation, not a movement; the capture is a smaller movement, so by §7 a new transaction (not an edit of the hold); the chargeback is a reversal by an authority's ruling long after the money was spent, which may find the merchant's account unable to fund it. [authorize_by_card](../../../modules-plugable/economics/card/edges/authorize_by_card/authorize_by_card.md) is a bare edge.
- *Asks of the domain:* the hold belongs to [restriction](../../../modules-plugable/economics/restriction/restriction.md) (its stated use case "pending-transfer reservations"); the capture is a transaction referring to the hold's cause; the chargeback is a compensating transaction with the dispute (a case) as reference and a defined outcome when it cannot execute (failed, with consequences).

**S8. A movement nobody consented to (a tax levy, a court-ordered transfer, an inheritance distribution, a seizure).** An authority orders 1,000 from a debtor's account to a creditor's.
- *Obvious model:* a transfer the debtor requested.
- *What breaks:* the requester is an authority acting under a law; the source holder's consent is irrelevant; the draft-then-accept shape of the justice pilot ([open 6](transaction.handoff.md#open-questions)) puts the transaction in draft until the case rules; "block a balance and transfer it" is restriction plus a transaction.
- *Asks of the domain:* authorization is by the requester's authority over the source, whatever its origin; the cause is mandatory and the reference is the order; refusal by rules (a blocked account) must not be bypassed by authority unless a rule says so.

**S9. Conditional pledges (an all-or-nothing crowdfunding campaign, a group purchase, a donation matched by a sponsor).** 5,000 backers pledge; nothing moves unless the total reaches the goal by the deadline.
- *Obvious model:* each pledge is a transaction with a condition.
- *What breaks:* the condition concerns the aggregate of other transactions and a time; decision 3 books the source first, so either every backer's money is withdrawn up front (and returned on failure) or the withdrawal is itself conditional, which decision 3 allows only as "before or at the same time".
- *Asks of the domain:* `condition_is` to a rule that watches other transactions (the rule domain's job, [conditional.md](edges/conditional/conditional.md#policies-rules)); an expiry outcome that creates the returns as new transactions; at the same time a source-conditional withdrawal is an edge case of decision 3 (owner question 5).

**S10. Cash at the till and cash through an agent (a shop's counter, a market stall, a mobile-money agent who takes notes and sends electronic value).** The movement happened physically; the system learns afterwards.
- *Obvious model:* a draft, approved, then processed.
- *What breaks:* "a request" is false here: it is a report of a fact already done. The system cannot refuse it by rule; it can only flag it. [cash_transaction](../../../modules-plugable/economics/cash/edges-shortcut/cash_transaction/cash_transaction.md) marks cash movements but the documents do not say whether such a transaction goes through approval at all.
- *Asks of the domain:* whether the kernel distinguishes an *observation* (acquired fact reported after the event) from a *request* (an intent not yet done). The classification sentence above covers the second; for the first, owner question 6.

**S11. An instalment sale in a falling currency (the owner's pre-sold apartments, recorded in [price-index](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales)).** Sixty fixed instalments; the currency loses most of its value.
- *Obvious model:* sixty scheduled transactions.
- *What breaks:* the amounts are decided at issue, so a transaction's quantity is fixed in a unit that drifts; an indexed instalment would compute its amount at its due date, so the quantity is not known when the intent is registered.
- *Asks of the domain:* the claim and its schedule live in invoice or a deferred-payment capability, not in the transaction; the transaction is created at due time with the amount computed then, or the quantity may be a rule's result at approval. Question 7 asks which.

### 2. Minimal kernel and what must be pluggable

**Tests applied (source).** [Modules → Placement](../../modules.md#placement): kernel only if removal forces a foundational type to be fabricated or distorted; a pluggable owns its relation and processing together; an edge becomes its own module only with independent identity, lifecycle, authorization, rules or processing; no bare edges (who creates or removes it, what it triggers); the kernel never references the rule domain directly; analytics is never kernel.

#### The removal test run on the transaction (agent, Tentative)
Remove the transaction domain. The `bookkeeping` edge then has no start node: a realized effect would have no cause, no requester and no condition, and the account research's append-only ledger would hold facts with no stated origin. Could another foundation carry the request? A `task` could carry "someone asked for something" ([task research](../../management/task/task.research.001.md) makes intent content and completion a pluggable), but then the kernel would give a task a quantity, two accounts and a realization edge, which bends task into a money concept. An `invoice` is a claim by a seller and cannot be the source of a levy (S8) or a cash report (S10). So the transaction earns a place as the **request-with-quantity**, and its independent responsibility is: *the intent's quantity and ends, its cause, its status path, and its immutability once relied upon.* It is thin by design: execution is elsewhere (decision 1).

#### Proposed kernel (agent, Tentative)
| Kernel element | Why kernel | Note |
|---|---|---|
| Identity: a `ThingUUID` | a transaction is a `thing` | `Field_TransactionID` exists ([dt-uuid.kh](protocol/dt-uuid.kh)) |
| `Quantity` as the single source of truth | booked quantity always equals it (§7) | a decimal; the unit comes from the account; see question 3 for a draft with no account |
| `account__from` and `account__to`, each at most one, each optional at registration | the two ends of the movement; the bookkeeping edge is derived from which side the account sits on | `account__by` stays in matching_system |
| `transaction_reference_is` to the cause | decision 10 | mandatory or convention is open 2; label vocabulary is not kernel (finding 6.4) |
| Registration fact: requester, time, request id | an acquired fact whose loss destroys audit ([State Change as Events](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates)); the account's records already carry the request id | today implicit in thing's registration; the thing research proposes a registration event (read at its question list only) |
| Status as events on the shared vocabulary | no private lifecycle (decision in [transaction.md](transaction.md#policies-rules)) | vocabulary is survey question R4; which are kernel defaults is [open 4](transaction.handoff.md#open-questions) |
| An event target for status and for registration | processors, restriction, fraud and notification must not poll | `TransactionModel` composes `EventTarget` already ([model.kh](protocol/model.kh)); the loss of per-type constraint is in the handoff |
| The generic `condition_is` attachment | rules attach, the kernel never says what they say | exists ([conditional](edges/conditional/conditional.md)) |
| Freeze point | the point after which quantity, ends and cause cannot change | proposal only; where it falls is question 2 |

Not transaction's: the unit (account), the booked effect (bookkeeping), availability (restriction), claims (invoice, contract), instruments (uri plus pluggables), prices and indexation, schedules, orders and matching.

#### Pluggable: the capability each would own
"Created / removed by" and "Triggers" are read from the cited document where it states them; otherwise "not stated" is a no-bare-edges gap, reported, not filled in.

| Capability (home) | Relation and processing it owns | Created / removed by | Triggers |
|---|---|---|---|
| **matching_system** (exists): `trade`, `deal`, `exchange`, `account-by`, `all_or_none`, `instant_withdrawal`, `fill_or_kill` | pairing opposite requests; partial/full deal; order types; the account to receive into | not stated for `deal`, `exchange`; `trade` registers an order (the user) | an engine matches and creates deals; `instant_withdrawal` books the source at registration |
| **settlement** (exists): `settles`, `endorsement`, `guarantor` | tiered representation; transfer of a commitment-bearing instrument; a guarantee as a linked transaction | endorsement: "only the owner of the receiving account may invoke"; guarantor: not stated (a claim or legal process fires it) | endorsement suspends the original and creates a new one; settlement transaction created immediately |
| **restriction** (exists) | reservations and blocks; release as a compensating transaction | judge, or pending-transfer rule; remover not stated | blocking transactions until satisfied; `released_by` |
| **cash** (exists): `cash_transaction` | marks a movement as cash via the account's cash role | not stated | the cash flow lists withdraw and deposit accounts |
| **card** (exists): `authorize_by_card` | a transaction authorized by a card | bare edge: not stated | not stated |
| **fraud_detection** (exists): `fraud`, `suspicious` | a rule's finding about a user, account, transaction | not stated | not stated; block by "fraud detection mechanism" appears in [block](../../knowledge/status/edges-loop/block/block.md) |
| **refund / voucher / credit** (exist) | refund rule on an invoice; a voucher is "a bond of the redeemable transaction type"; credit state of an account | not stated | not stated |
| **budget** (exists) | spending booked against allocations | not stated | not stated |
| **analytics** (exists) | transaction queries and totals (discovered) | not applicable | not applicable |
| **chain** (proposed, new, or generic) | one relation family: follows, part of, reverses | agent proposal: the requester of the later transaction; never removed | the processor reads order; a reversal links back |
| **acting-for** (proposed; likely `rights/delegate`, not new) | who may request, or approve, a debit from an account; standing mandates | agent proposal: the owner of the account or an authority; revocable | a request from the account is accepted only for an authorized requester |
| **recurrence / mandate** (proposed; likely task recurrence plus delegate) | creation of transactions on a clock under a standing authority | agent proposal: payer grants, either may revoke | creates a transaction per period |
| **reference vocabulary** (proposed home: label registry, see 6.4) | the reason words (Donate, Tip, Installment, ...) | the originating domains | none |
| **deferred payment / instalment** (proposed, new, to be checked with price-index and invoice `conditional`) | schedule and indexation of due amounts | agent proposal: the seller or lender | creates a transaction per due date with the amount computed then |

The pattern repeats the account research's: where a capability exists, who creates it, who removes it and what it triggers are usually not stated (rows "not stated").

### 3. Rival models

Seven rival models, then three smaller choices. Each is marked.

- **R1. Status quo: a request thing with Quantity, optional from/to, reference, condition, bookkeeping effect (Explored; the current state).** Fits the common case. Trade-offs: the freeze point is unstated; the asker and the authorizer are not separated; the in-flight quantity is in no account; the chain relations are named but undefined; a draft may have a quantity without a unit.
- **R2. Hardened request kernel: R1 plus a registration fact, a freeze point at approval, status events, an event target, a stated chain family, and one rule for the unit of a draft (Tentative; recommended).** Adds no account edge and no container. Migration cost is low because every item is a statement about what already exists. Keeps every Decided statement true.
- **R3. Two-level: a *transfer* (one pair, own status) inside a container that groups transfers with sequencing and all-or-nothing semantics (Explored).** Directly answers S3, S4 and S9, and the handoff's lean that "multi-party operations [are] lifted to a higher concept" ([open 1](transaction.handoff.md#open-questions)). Costs a new foundation that must pass [What Earns Foundational Status](../../knowledge/modularity/modularity.md#what-earns-foundational-status): for payroll the invoice already is the container, for a task-driven operation the task is. It earns a place only if a scenario has no existing container and demands atomic grouping (S9 is the candidate).
- **R4. Entry set (journal) model: a transaction is a set of entries, no source-to-destination pairing (Explored; contrary to Decided item 2).** Natural for S4. Rejected for the transaction by decision 2 because pairing is lost for fee-like cases. Noted because the account is indifferent to it ([account research, model D](../account/account.research.001.md#3-rival-models)).
- **R5. Obligation-first: a claim (debtor, creditor, quantity, due) is the foundation, and a transaction is one performance of it (Explored).** Fits S5, S11 and guarantees (contingent liabilities). Rejected as a kernel replacement because claims already have homes (invoice, contract) and S8 and S10 show requests with no prior claim. Kept as the reading that decides where schedules live: the claim owns the schedule, the transaction is created when asked.
- **R6. Operation model: the transaction is the execution (Rejected, Decided by [decision 1](transaction.handoff.md#ambiguities-resolved)).** Listed for completeness.
- **R7. Intent-and-route: the transaction declares an outcome (give up to 1,000, deliver at least 985) and a route finder chooses the hops (Explored).** The DeFi prior art in [transaction.md](transaction.md#prior-art). Fits S3 and S6; belongs, if adopted, in a routing capability beside matching_system, not in the kernel.

**How each model meets the cases (agent judgment).** "Fits" means no distortion; "strained" a workaround; "fails" a wrong statement.

| Case | R1 | R2 | R3 | R4 | R5 | R7 |
|---|---|---|---|---|---|---|
| S1 cheque | fits | fits | fits | strained | fits | fits |
| S2 escrow | strained (limbo) | strained, fits with choice 1 | strained | strained | strained | fits |
| S3 correspondents | strained (no one-intent node) | strained, fits with chain | fits | strained | strained | fits |
| S4 split payout | strained | strained, fits with an existing container | fits | fits | fits | strained |
| S5 mandate | strained (requester) | fits | strained | fits | fits | strained |
| S6 swap | fits | fits | fits | strained | strained | fits |
| S7 hold/capture | fits (hold elsewhere) | fits | fits | fits | strained | fits |
| S8 compelled | strained | fits | fits | fits | fails | strained |
| S9 pledges | strained | strained | fits | strained | strained | strained |
| S10 cash fact | fails ("request") | strained, fits with an observation status | fails | fits | fails | fails |
| S11 indexed instalments | fails | strained, fits with claim-owned schedule | strained | strained | fits | strained |

R2 has no "fails" row except where the case needs a new concept (S10 is strained, not failed); R3 beats it on S3, S4, S9 only if no existing container is available; R5 is the better reading of where schedules live, not a replacement.

#### Smaller choice 1: what is the in-flight quantity (Explored)
- **(i) Implicit in the transaction (the current Decided reading).** In-flight = sum over transactions with exactly one record. Simple; the quantity belongs to no one, so freezing, dispute and insolvency have no account to act on (S2).
- **(ii) Always an account (transit or escrow).** Deferral is two transactions through an account that someone holds, which is what real escrows, correspondents and clearing houses are. Makes the single-sided transaction unnecessary and contradicts decision 3's wording "A transaction MAY book the withdrawal now and the deposit days later".
- **(iii) Both: implicit for short engine-internal deferral, explicit account where holding has legal meaning.** Two mechanisms for one fact; the test for which applies would be a rule.
Recommendation: none; report it. If the account research's counterpart accounts are accepted, (ii) is the same pattern one step over.

#### Smaller choice 2: the unit of a draft (Tentative: determined at approval)
A draft with no account has a number with no unit ([account.handoff.md](../account/account.handoff.md#decisions) item 4 versus [transaction.md](transaction.md#model)). Options: (a) the transaction carries its own `count_unit` (a second location for a rule the account owns); (b) at least one account at registration (breaks the justice pilot, [open 6](transaction.handoff.md#open-questions)); (c) a draft may carry a bare quantity, and approval requires the unit to be determinable from the named accounts. Recommended: (c).

#### Smaller choice 3: what freezes when (Tentative: at approval, and at the first record for the ends)
Draft: quantity, ends, cause and conditions may change, each change an event that keeps the earlier value. Approved: all frozen; a change is a new transaction that supersedes. After the first booking: nothing changes, including statuses except by new events. The reference is already immutable from registration ([reference](edges/reference/reference.md#policies-rules)), which is stricter than this and stays.

### 4. What the domain must own, as requirements questions

Written to favour no answer where unsettled. A citation means a document already constrains the question; "open" means nothing in the tree decides it.

#### Identity
- What makes two transactions the same? The `ThingUUID` alone; but a retry is "a new occurrence" of the same intent ([handoff](transaction.handoff.md#decisions)): is the intent the transaction and the occurrence a request, so the booking is idempotent per (transaction, side)? Open.
- Is a transaction scoped to one organization, or may it name accounts of two? Open (account research question 13).
- May the same account be both source and destination? "One record per affected account" ([bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md#policies-rules)) is silent. Open.
- Is a numbered instrument (cheque, receipt number) a `uri` of the transaction? Cited as the pattern in [account.handoff.md](../account/account.handoff.md); not stated here.

#### Lifecycle
- Which statuses are kernel defaults? Three candidate sets exist: draft, authorization; issued, blocked, bounced ([transaction.md](transaction.md#policies-rules)); Pending, Expired, Cancelled, Voided ([Idea backlog](transaction.md#idea-backlog)); Approving, Processing, Processed, Rejected, Failed, Canceled, Compensated ([request-status](../../knowledge/status/edges/request-status/request-status.md)). Open ([open 4](transaction.handoff.md#open-questions)).
- Is "cancelled" (before any booking) different from "compensated" (after one)? Open.
- May a transaction be deleted? transaction.md says "deleted"; no booking is ever deleted. Open.
- What ends a transaction that is never processed: an expiry rule, a deadline field, nothing? Open.
- What is a partially processed transaction: source booked and destination not (a status), or two statuses? Open.
- May a draft be an observation of a fact already done (S10)? Open.

#### Authorization
- Who may register, approve, cancel and retry? "One or more users" ([transaction.md](transaction.md)); `approval_needed` exists ([approval_needed](../../knowledge/status/edges-loop/approval_needed/approval_needed.md)). Open.
- Must the requester be the authorizer of the source, or may a payee pull (S5) and an authority compel (S8)? Open.
- May a transaction be approved by several users jointly (a company with two signatories)? Open.
- Who may read a transaction, whose reference may name a private cause? Open.
- Who may attach each pluggable edge to a transaction (a guarantor, an endorsement, a card, a trade)? Mostly not stated (finding 2).

#### Rules
- Which rules does the kernel itself require? Candidates (own proposal): at most one source and one destination (cited); a transaction names at least one account at approval; both accounts share one unit (cited, but where it is enforced is open, account research question 15); reference immutable (cited); source realized before or with destination (cited); quantity positive (the sign comes from the side, [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md#policies-rules)) — zero and negative quantities ([negative pricing](edges/account-from/account-from.md#policies-rules)) open.
- Is the effective time (value date) a field of the transaction, as the account research's default assumes? Open (account research question 6).
- May a quantity be a rule's result at approval (S11)? Open.
- Is `from` equal to `to` valid? Open.

#### Events
- Which facts must the domain emit: registered, approved, source realized, destination realized, completed, failed, cancelled, expired? The kernel exposes an event target, not an event model ([Event as a Module Capability](../../knowledge/modularity/modularity.md#event-as-a-module-capability)). Open.
- Who listens, and is each reaction the listener's own rule, never a cascade the transaction performs? (restriction creates its own transactions, [restriction.md](../../../modules-plugable/economics/restriction/restriction.md#policies-rules)). Open for the rest.
- A failed listener may not change the transaction. Proposed, open.
- Is a failure a status of the transaction or an event of an attempt? [failed](../../knowledge/status/edges-loop/failed/failed.md) says "Refund for any reason". Open.

### 5. How the existing edge folders map

Without moving anything. Verbs: **keep**, **reclassify**, **retire**, **missing**.

| Folder | Verb | Proposed disposition | Basis |
|---|---|---|---|
| [edges/account-from](edges/account-from/account-from.md) | keep, correct | Kernel edge. Its text still speaks of `takes`, `sell` and "financial account"; it states no rule that the source may not change after a record exists (the destination does, [account-to](edges/account-to/account-to.md#policies-rules)). Its record declares only `Observer_Quantity` (handoff) | own Policies; [handoff](transaction.handoff.md#khayyam-conversion-2026-10-03) |
| [edges/account-to](edges/account-to/account-to.md) | keep, correct | Kernel edge. "If this edge exist, `takes` edges MUST not exist" names a vocabulary the tree replaced by `account__by` in matching_system; reconcile (open 3) | same |
| [edges/conditional](edges/conditional/conditional.md) | keep | The generic attachment point. Its second line `(rule)-[:is_condition_for]->(transaction)` is a reverse traversal, not a second edge | own Policies |
| [edges/reference](edges/reference/reference.md) | keep, split | The edge is kernel. The "Reference types" vocabulary is not kernel and has no owner in code; it moves to a label registry (finding 6.4). The thing-side name `financial_transaction_is` carries the legacy "financial" framing the handoff closed for the field name | own Open questions |
| `protocol/*.kh` (five files) | keep | Converted, accepted. Import paths were corrected in the working tree during this session (Contradictions, item 11); the handoff prose still shows the old path | [handoff](transaction.handoff.md#khayyam-conversion-2026-10-03) |
| `services/*.kh`, `internal/storage/ganjine.kh` | retire | Old per-user `FinancialTransaction` record, as the handoff already says: delete or re-model | handoff |
| [matching_system](../../../modules-plugable/economics/matching_system/matching_system.md) edges | keep | `deal`, `trade`, `exchange` stay. `account-by` is user-set and is an edge, not a shortcut (survey D5); `exchange` is an alias of `deal` in the survey's reading | survey reports |
| [settlement](../../../modules-plugable/economics/settlement/settlement.md): `settles` | keep | Transaction-level tier link | settlement Model |
| settlement: [endorsement](../../../modules-plugable/economics/settlement/edges/endorsement/endorsement.md), [guarantor](../../../modules-plugable/economics/settlement/edges/guarantor/guarantor.md) | reclassify | Their home is "undecided" in their own documents; they are conditional-fulfilment capabilities (finding 6.5). The `(User)-[:GUARANTEES]->(...)` line is query-flavoured | their Open questions |
| [restriction](../../../modules-plugable/economics/restriction/restriction.md) `released_by` | keep | The pair `released_by` / `released_to` has no policy text | document |
| [cash_transaction](../../../modules-plugable/economics/cash/edges-shortcut/cash_transaction/cash_transaction.md) | reclassify | A shortcut over account role and transaction; the Model has a typo; whether it is acquired (S10) is open | survey D11 |
| [authorize_by_card](../../../modules-plugable/economics/card/edges/authorize_by_card/authorize_by_card.md) | reclassify | Bare edge: no creator, remover or trigger | placement rule |
| [fraud](../../../modules-plugable/economics/fraud_detection/edges/fraud/fraud.md), `suspicious` | keep, document | A rule's finding about a transaction; discovered data | survey |
| [status](../../knowledge/status/status.md) loops: `failed`, `read-only`, `block`, `approval_needed`, `request` | keep | The shared vocabulary; the transaction-specific candidates in `request-status` stay unconfirmed until open 4 | status documents |
| **missing** | | `followed_by` / part-of, `reverses`, registration fact, observation status, freeze point | findings 2 and 6 |
| **Not this domain's, reported:** [invoice](../invoice/invoice.md) | — | Settles by transactions; invoice currency must equal the paying account's unit, a rule for whoever creates the transaction | [invoice.md](../invoice/invoice.md#definition-in-memar) |

### 6. Missing edges and modules

Each is a proposal; none is created here. Each names what, who creates and removes, and what it triggers.

**6.1 Chain family — one relation defined once (Explored).** `followed_by` (order), `part_of` (one intent's legs) and `reverses` (compensation) among transactions. Today decisions 2 and 6 rely on them and no folder exists. By [A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once), task already has `part_of` and `blocks` and thing proposes `derived_from` (read at the thing research's question 18 only), so the generic ordering and part-of relations may be defined once and transaction only adds `reverses`, which has transaction-specific rules: it needs an original with at least one record, and it books the opposite sides. Created by the requester of the later transaction; never removed. Triggers: the processor honours order; a reversal's registration is an event to the original's listeners.

**6.2 Registration fact (Tentative).** Requester, time and request id as an acquired fact, not edited. Created by the system on registration; no remover. Triggers the registered event. Likely covered by thing's registration event if the thing research is accepted.

**6.3 Freeze (Tentative).** A status `approved` (or the existing `read-only` loop) that stops edits of quantity, ends and conditions, with the first record freezing the rest. Created by the approver; removed by nobody (a change is a new transaction). Triggers the approved event; processors act on it.

**6.4 Reference vocabulary in the label registry (Tentative).** The accepted list in [reference](edges/reference/reference.md#reference-types) becomes registered words; the budget words move to the budget module ([reference](edges/reference/reference.md#open-questions) asks the same). Created by the originating domain; no remover. Triggers nothing.

**6.5 `conditional-fulfilment` — a home for endorsement, guarantor, escrow (Explored).** Both documents say their home under `settlement` is a placeholder for "the processing machine behind conditional fulfilment". One capability owning commitments carried by transactions: endorsement, guarantee, escrow and the cheque composition. Created by the parties; removal ends future effect only. Triggers: suspension and new transactions; a claim or maturity fires a guarantee.

**6.6 Observation status (Explored).** A transaction registered after the fact (S10), accepted as acquired data, flagged but not refused by rules. Created by the reporter (till, agent); not removed. Triggers a flagging rule, not a refusal.

**6.7 Standing authority / mandate (Explored; likely `rights/delegate` plus task recurrence).** A payer's revocable standing authority for a payee to request debits, bounded by amount and period, and a clock that creates the requests. Created by the account's owner; removed by the owner. Triggers: each period creates a transaction (S5). Whether delegate's lifecycle covers it is the open question the account and task researches also ask.

**6.8 Deferred payment (Explored; check price-index and invoice conditional).** Schedule and indexation of due amounts, creating a transaction per due date with the amount computed then (S11). Created by the seller; removal ends future instalments. Triggers the transaction creation.

**6.9 Dispute and reversal by authority (Explored; likely `rights/case`).** A chargeback or a break of a final ruling as a compensating transaction with the case as reference and a defined outcome when the account cannot fund it (S7, [open 6](transaction.handoff.md#open-questions)). Created by the authority. Triggers a failed status with consequences by rule.

**6.10 Atomic group (Deferred).** Only if the owner wants all-or-nothing multi-leg semantics where no existing container applies (S9, S4 marketplace): model R3. Deferred until a case shows it.

### 7. Test scenarios

Given/when/then in prose. Each is marked **kept** (follows from settled text), **R2** (assumes the recommended model), or **Q n** (assumes the default of owner question n).

1. **One pair at most (kept).** Given a request naming two sources. When registered. Then it is refused; two sources are two transactions linked.
2. **Request is not effect (kept).** Given a draft transaction. When the accounts are read. Then no bookkeeping record exists and no balance changed.
3. **Withdrawal before deposit (kept).** Given an approved transaction. When processing starts. Then the source record is booked first or together with the destination record; never after.
4. **Delay allowed (kept).** Given a source record booked and a not-yet-met condition. When the destination is read. Then it has no record; the transaction reads partially processed (Q 4).
5. **Booked equals requested (kept).** Given a quantity of 100. When booked. Then both records carry the effect of 100; a fee is a separate transaction.
6. **No rollback (kept).** Given a booked source effect and a failed destination. When the sender cancels. Then a new transaction books the reverse and `reverses` the original; record 1 is unchanged.
7. **Cause by reference, immutable (kept).** Given a registered transaction referencing an invoice. When someone tries to change the reference. Then it is refused and the transaction carries the read-only mark.
8. **Reference is mandatory (Q 8).** Given a request with no reference. When registered. Then it is refused (default) or accepted with a warning (convention).
9. **Destination fixed after a record (kept).** Given a destination record exists. When the destination is changed. Then refused ([account-to](edges/account-to/account-to.md#policies-rules)).
10. **Source fixed after a record (R2).** Same for the source.
11. **Draft is editable with history (R2, Q 2).** Given a draft with quantity 100. When changed to 120. Then the draft shows 120 and the change is a kept event with 100.
12. **Approved is frozen (R2, Q 2).** Given an approved transaction. When the quantity is edited. Then refused; a new transaction supersedes.
13. **A draft with no unit (Q 3).** Given a draft with quantity 50 and no account. When approval is requested. Then it is refused until an account fixes the unit.
14. **Cross-unit pair refused (kept).** Given source in kilograms and destination in grams. When approved. Then it is refused as a movement; the intent is two transactions linked by `exchange`.
15. **A cheque matures (S1).** Given an approved transaction with a not-before condition three months out. When the date passes. Then the rule releases it; before that nothing is booked, and a bounce is a failed status plus an event for reputation listeners.
16. **An escrow is held (S2, Q 4).** Given the source booked and the destination awaiting confirmation. When a court freezes the funds. Then the freeze acts on an account that holds them (under choice 1 option ii) or on the in-flight quantity (option i, which the freeze cannot reach: the case that decides between them).
17. **A chain of hops (S3, R2).** Given three transactions linked `followed_by`, the second failing. When the failure is recorded. Then the first is reversed by a new transaction, the third is cancelled before any booking, and the sender's one intent is readable by traversing the chain from the first.
18. **A split payout (S4).** Given a payer intent with three destinations. When registered. Then it is three transactions with one shared cause; whether they succeed together is not a kernel guarantee (Q 10).
19. **A direct debit (S5, Q 6).** Given a payee holding a mandate. When it requests 40. Then the request is accepted because the authority is the payer's delegation; with the mandate revoked it is refused.
20. **A swap withdraws first (S6, kept).** Given an exchange with `instant_withdrawal` on both legs. When registered. Then both sources are booked immediately; if the match never comes, two reversals return them.
21. **A hold and a capture (S7).** Given a reservation of 200 and a capture of 180. When the capture is registered. Then it is a new transaction of 180 referring to the cause; the reservation is released as its own compensating transaction of 200.
22. **A compelled transfer (S8).** Given a court order. When registered by the authority. Then the cause is the order; a rule blocking the account is not bypassed unless the order's rule says so.
23. **Pledges that fail (S9).** Given conditional pledges with a goal and a deadline. When the deadline passes below the goal. Then every pledge is cancelled or returned by new transactions; none is edited.
24. **A cash report (S10, Q 9).** Given a till reports a sale already done. When registered. Then it is accepted as an observation and flagged by rule, not refused.
25. **An indexed instalment (S11, Q 7).** Given a schedule owned by the invoice. When a due date arrives. Then a transaction is created with the amount computed at that date, and it freezes at approval.
26. **Same account both ends (Q 11).** Given from equal to to. When approved. Then refused (default).
27. **An event per status change (R2).** Given a status change. When committed. Then one event is emitted; a failing listener does not alter the transaction.

### Contradictions found

Reported, not resolved. Each cites both sides, read at the file.

1. **Deleted versus never deleted.** [transaction.md](transaction.md) says a request "may be drafted, approved, partially processed, deferred, cancelled, or deleted"; [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md#policies-rules) and [handoff decision 6](transaction.handoff.md#decisions) say booked effects are never undone or edited. Whether deletion applies only to a transaction with no record is not stated; the shared [deleted](../../knowledge/status/edges-loop/deleted/deleted.md) loop exists.
2. **Conservation versus delay.** [Decision 3](transaction.handoff.md#decisions) requires that "what leaves the source equals what enters the destination" and allows the deposit days later; between the two effects the quantity is in no account. Reported also as the first-leg problem in the [account research](../account/account.research.001.md#contradictions-found), item 2.
3. **Optional source versus no unbacked quantity.** [transaction.md](transaction.md#model) makes the source optional at registration, [account-from.md](edges/account-from/account-from.md#policies-rules) says "a `user` want to `takes` something without `gives` anything", decision 3 forbids crediting before debiting. Same item as the account research's item 2.
4. **A draft with a number and no unit.** [account.handoff.md](../account/account.handoff.md#decisions) item 4 puts the unit on the account; the justice-pilot note ([open 6](transaction.handoff.md#open-questions)) and [transaction.md](transaction.md#model) allow a draft with only the amount asked. Account research item 5.
5. **Named, not defined.** [transaction.md](transaction.md#policies-rules) lists `followed_by` among the linking edges; a search of `modules` and `modules-plugable` finds the word only in the transaction documents. The compensation link of decision 6 has no folder either. `settles`, `exchange`, `deal`, `endorsement_in_favor_of`, `guarantor_is` have documents.
6. **`takes` versus `account__by`.** [account-to.md](edges/account-to/account-to.md#policies-rules) says "If this edge exist, `takes` edges MUST not exist"; [account-by.md](../../../modules-plugable/economics/matching_system/edges-shortcut/account-by/account-by.md) describes the receiving-account semantics under the new name and calls itself a shortcut though a user sets it; [account-from.md](edges/account-from/account-from.md) still describes optional `takes`. Handoff open 3 already asks.
7. **Split by endorsement versus booked equals requested.** [endorsement.md](../../../modules-plugable/economics/settlement/edges/endorsement/endorsement.md#policies-rules) says several endorsements split "first transaction quantity", the original is suspended; [bookkeeping.md §7](../account/edges/bookkeeping/bookkeeping.md#7-booked-quantity-equals-requested-quantity) says the requested quantity is the single truth. After a split what is the original's quantity?
8. **Reference: mandatory, automatic, or convention.** [reference.md](edges/reference/reference.md#policies-rules) says "Referencing MUST be automatic process" and the transaction "MUST get `ReadOnly` label"; handoff decision 10 says no transaction exists without a cause; [open 2](transaction.handoff.md#open-questions) asks whether it is mandatory or convention. The thing-side edge is still named `financial_transaction_is`.
9. **A marker without a freeze point.** [account-to.md](edges/account-to/account-to.md#policies-rules) fixes the destination once a record exists; [account-from.md](edges/account-from/account-from.md#policies-rules) states no equivalent; [transaction.md](transaction.md) has none for quantity or conditions; the idea backlog says "User can't redo||change|| ... to transaction" and "Currency change can't be in transaction request" without owner.
10. **Three status vocabularies.** `issued`, `blocked`, `bounced` ([transaction.md](transaction.md#policies-rules)); Pending, Expired, Cancelled, Voided ([Idea backlog](transaction.md#idea-backlog)); Approving, Processing, Processed, Rejected, Failed, Canceled, Compensated ([request-status](../../knowledge/status/edges/request-status/request-status.md)). Also spelling: Cancelled and Canceled.
11. **Import paths, resolved in the working tree during this session.** The coordinator states that Khayyam imports inside this repository carry no `org/` prefix. When first read, the `.kh` files of this domain imported with `org/modules/...`; at the end of the session they import with `modules/...` (uncommitted edits by another party, not by this session). The handoff's Khayyam section still quotes the old `org/modules/identity/thing/protocol/dt-uuid.kh` path in prose.
12. **Kernel names pluggables.** [transaction.md](transaction.md#policies-rules) names `matching_system` and lists pluggable edges; [account-from.md](edges/account-from/account-from.md#policies-rules) discusses `money` and `sell`. Against [Modules → Placement](../../modules.md#placement) (core never knows pluggables); the same finding as in the [account research](../account/account.research.001.md#contradictions-found), item 8.
13. **Handoff status wording.** [transaction.handoff.md](transaction.handoff.md#status) says invariants are "practiced in README/edges", but `README.md` holds only the text `transaction.md`.

### Reconciliation with the sibling researches

Read as claims; only what was read at the file is relied on. The [account research](../account/account.research.001.md) was read in full; the product and task researches by searching for transaction-relevant words and reading the hits; content, text, group, thing and user only at their open-question lists and the synthesis (see Starting Evidence).

**Agreements.**
1. **Same kernel shape.** Identity, one or two structural relations, status as events, an event target, a generic `condition_is`, and pluggables owning relation and processing together ([concept-synthesis.md](../../../temp/sessions/20261014T071207Z-28148-0/concept-synthesis.md)). Here: identity, quantity, two ends, cause, status, event target, condition.
2. **A correction is a new fact.** The account research states it for bookkeeping; the synthesis lists it for tombstones, immutable text values and task supersession. The transaction's `reverses` is the same move.
3. **Status as events on the shared vocabulary, waiting on ruling R4.** Account, product and task all wait on it (account research, reconciliation agreement 3); so does this one.
4. **Reference, not embed.** [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md) states the rule; the cause by reference and the body by reference in content are the same rule.
5. **Account counterparts and conservation.** This research depends on the account research's default (counterpart accounts, [question 2](../account/account.research.001.md#open-questions)): if accepted, an absent source becomes an explicit counterpart and S10's destination-only deposit is an issuance; if rejected, the optional source stays unbacked.
6. **Effective time on the transaction.** The account research's default (question 6) puts the effective time on the transaction; this research asks the transaction domain whether it accepts that field.
7. **Budget has one home.** The task research's default (question 12, read in its list) has budget hold the one budget relation; the transaction reference vocabulary's budget words (Materials, Labor, Markup...) belong with budget for the same reason.

**Contradictions and tensions across the researches.**
1. **Counterparts versus an optional source.** Account question 2 proposes a counterpart per unit so that every transaction conserves; [transaction.md](transaction.md#model) keeps the source optional and S9/S10 here make observation and pledge cases that look like sourceless requests. The two researches propose compatible fixes but neither adopts the other's.
2. **Three creators of "the other side".** The account research notes product's `pack`, production and the bakery all reinvent "the other side"; here the transaction chain adds a fourth place (an escrow or transit account). One decision (account question 2) settles all four.
3. **Where authority lives.** Account question 3 puts instruction authority in delegation and authorization; this research needs the same for requester versus authorizer (S5, S8). Group research question 17 and task question 6 ask related things (read in their lists only). One home is needed for "who may cause an effect on a thing they do not own".
4. **Never erased versus erased.** The account research already reports that the ledger is never erased while text, content and user default to authority-gated erasure; a transaction's reference and requester are personal data in some jurisdictions. The same resolution applies: detach identity, keep effect (account question 14).
5. **Invoice exchange.** The invoice handoff's open question on one invoice or two per organization is the same shape as a transaction naming accounts of two organizations (account question 13). Read at [invoice.md](../invoice/invoice.md#unresolved-questions) and the account research only; [invoice.handoff.md](../invoice/invoice.handoff.md) was not read in full.

## Recommendation (unratified)
The owner has not reviewed this, and nothing in it is decided.

1. **Say what the transaction is for (Tentative, medium confidence).** The memory of requested quantity movement and its path to realization: intent, cause, conditions, status events and links; execution and effect are elsewhere.
2. **Keep a nine-element kernel (Tentative):** identity, quantity, the two ends, the cause, the registration fact, status events, an event target, the `condition_is` attachment, and a stated freeze point. Everything else is a capability, a rule or an existing domain.
3. **Choose R2 over R1; keep R3 deferred until a case has no existing container (Tentative).** R2 adds statements, not folders.
4. **Define the chain family once across domains (Tentative):** order and part-of are generic relations; transaction adds only `reverses`.
5. **Report the in-flight quantity and do not decide it (Explored).** It decides whether single-sided transactions survive.
6. **Keep schedules with claims (Tentative):** invoice and a deferred-payment capability own due dates and indexation; a transaction is created when asked.
7. **Separate requester from authorizer (Tentative)** and put authority in delegation, as the account research does.
8. **Distinguish an observation from a request (Explored)** before the cash and agent cases force it.
9. **Do not move, delete or convert anything on this evidence.** The mapping in finding 5 is a reading list.
10. **Ask the three questions that change what the work is first:** question 1 (what the transaction is responsible for), question 4 (the in-flight quantity), and question 6 (requester versus authorizer).

## Open Questions
Only the owner can decide these. Ordered by what they change, those that change what the domain is first. Each carries a recommended default and what it blocks. They are also entered in the [handoff](transaction.handoff.md#open-questions).

1. **Is the transaction's responsibility the memory of requested quantity movement and its path to realization (intent, cause, conditions, status, links), with execution and effect elsewhere?** Default: yes. Blocks: the opening paragraph of [transaction.md](transaction.md), the choice between R1 and R2, the shape of `TransactionModel` beyond `ThingModel` and `EventTarget`.
2. **When does a transaction freeze: quantity, ends and conditions at approval, the ends and everything else at the first booking?** Default: draft editable with kept history, approval freezes, a change afterwards is a new superseding transaction. Blocks: the immutability statements of `account-from`, `account-to` and `reference`, the idea-backlog items on "can't redo" and "currency change", the read-only mark.
3. **What is the unit of a draft with no account?** Default: a bare quantity is allowed; approval requires the unit to be determinable from the named accounts. Blocks: the justice-pilot draft, the duplicate same-unit rule (account question 15), `TransactionAccountFromDataModel`.
4. **What is the quantity between the source effect and the destination effect: nobody's (implicit), always an account's (transit or escrow), or both by a rule?** Default: none recommended; report. Blocks: decision 3's wording, escrow, LC, correspondents, freezing in flight, conservation as a graph claim (account question 2).
5. **May a withdrawal itself be conditional, or must the source always be booked first (decision 3) so that conditional pledges are held then returned?** Default: source first; a conditional withdrawal is a hold in restriction. Blocks: S9, S6, `instant_withdrawal`, the meaning of "delay is allowed".
6. **Who may request and who must authorize a debit: may a payee pull under a standing authority, and may an authority compel?** Default: the requester may differ from the authorizer; authority over the source is delegation or a law, recorded; the transaction names the requester only. Blocks: direct debits, levies, the justice pilot, payroll collection, account question 3.
7. **May a quantity be a rule's result at approval (an indexed instalment), or is it always a stated number at registration?** Default: stated at registration; indexed schedules create the transaction at due date. Blocks: deferred-payment sales, [price-index](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales), the [unresolved question](transaction.md#unresolved-questions) of instalments.
8. **Is the cause (reference) a mandatory edge or a convention, and is it set automatically?** Default: mandatory at approval, may be absent in draft. Blocks: [open 2](transaction.handoff.md#open-questions), `reference.md` policies, the kernel's refusal rules.
9. **Does the domain distinguish an observation (a movement already done, reported afterwards) from a request?** Default: yes, as a status that rules may flag and not refuse. Blocks: cash at the till, agent networks, offline payment, `cash_transaction`.
10. **Is there a container for several transactions that must succeed together, or does each scenario use an existing one (invoice, task, case) with the chain family?** Default: no container; use existing ones; atomic grouping deferred until a case has none. Blocks: R3, S4 marketplace payouts, S9, [open 1](transaction.handoff.md#open-questions) ("a higher concept").
11. **Are `from` equal to `to`, zero quantity and negative quantity valid?** Default: refused for the first two; negative quantity is not a negative transaction, it is the opposite direction. Blocks: [negative pricing](edges/account-from/account-from.md#policies-rules), test 26.
12. **Which statuses are kernel defaults, and are Cancelled and Compensated different?** Default: kernel defaults draft, approved, partially processed, completed, failed, cancelled; compensated is a link (`reverses`), not a status. Blocks: [open 4](transaction.handoff.md#open-questions), `request-status`, the idea-backlog status labels, ruling R4.
13. **Where do the chain relations live: transaction-specific, or generic relations defined once (with `reverses` the only transaction one)?** Default: generic order and part-of, transaction owns `reverses`. Blocks: `followed_by`, `settles`, `endorsement_in_favor_of`, decisions 2 and 6.
14. **Does the transaction carry the effective time (value date), as the account research's default assumes?** Default: yes, a field of the transaction; recorded time is the registration. Blocks: statements "as of a date", back-dated entries, account question 6.
15. **Do endorsement, guarantor and escrow leave settlement for a conditional-fulfilment capability?** Default: yes. Blocks: both documents' homes, settlement's internal structure, the cheque composition test.
16. **Do the reference words live in the label registry, and do the budget words move to budget?** Default: yes to both. Blocks: the "Reference types" section and its open questions, the thing-side name `financial_transaction_is`.
17. **Is `account__by` an edge owned by matching_system or a use of `account__to`?** Default: `account__by` stays in matching_system as an edge (user-set); `account__to` stays core. Blocks: [open 3](transaction.handoff.md#open-questions), the `takes` wording.
18. **What does a failed leg do to the earlier legs of a chain: nothing, a rule decides, or a reversal is automatic?** Default: a rule decides; nothing is automatic in the kernel; the sender may cancel. Blocks: S3, S6, "never roll back on the user's behalf" ([handoff](transaction.handoff.md#decisions)).

## Related Artifacts
- [transaction.md](transaction.md) — the opening paragraph and the Unresolved questions change if question 1 is accepted (Review; not edited)
- [transaction.handoff.md](transaction.handoff.md) — gains questions 7 and onward and Next Steps (Update, done in this session)
- [transaction.changelog.md](transaction.changelog.md) — created with an entry for this research (Create, done)
- [account.research.001.md](../account/account.research.001.md), [account.handoff.md](../account/account.handoff.md) — the other half; questions 2, 3, 6, 13, 15 (Related)
- [bookkeeping.md](../account/edges/bookkeeping/bookkeeping.md) — §7 and §8 (Review)
- [invoice.md](../invoice/invoice.md) — claims and settlement (Related; not edited)
- [Product Research 001](../product/product.research.001.md), [Task Research 001](../../management/task/task.research.001.md), [Content Research 001](../../knowledge/content/content.research.001.md), [Text Research 001](../../knowledge/text/text.research.001.md) — sibling researches (Related)
- [matching_system](../../../modules-plugable/economics/matching_system/matching_system.md), [settlement](../../../modules-plugable/economics/settlement/settlement.md), [restriction](../../../modules-plugable/economics/restriction/restriction.md), [status](../../knowledge/status/status.md) — the capabilities the mapping keeps or reclassifies (Review)
