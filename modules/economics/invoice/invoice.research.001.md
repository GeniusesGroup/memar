# Invoice Research 001 — What the invoice domain is for, and what is kernel and what is pluggable

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

Nothing here is ratified. Every proposal carries a confidence mark in the sense of [Handoff Practice](../../knowledge/documentation/handoff/handoff.practice.md): Decided, Tentative, Explored (explored but unresolved), or Deferred. **No item below is Decided by this research.** Items already Decided in the domain documents are cited as such and are not re-argued: a customer, a buyer and a consumer are three distinct roles joined to the user by distinct edges; core versus optional is relative to purpose; an invoice carries no `discount` field (naming of the aggregation still open); a payslip is not a concept but invoices between an employee-seller and an organization-buyer; tax is not a kernel concept; a paid invoice is never deleted and corrections are compensating records; a purchase invoice's item is history and never the basis of a later sale price ([invoice.md](invoice.md#definition-in-memar), [invoice.handoff.md](invoice.handoff.md#decisions), [item.md](edges/item/item.md#policies-rules), [paid](status/paid/paid.md)).

## Question and Goals
- **Questions:**
  - What is the invoice domain for, once it is tested against cases that are not a shop receipt? — Answered as finding 1 (proposal, Tentative).
  - Which part is kernel and which must be pluggable, under the tests of [Modules → Placement](../../modules.md#placement)? — Finding 2.
  - Which rival model survives the cases and Memar's modeling criteria? — Finding 3; the choice is the owner's.
  - What must the domain own, and what is unsettled? — Finding 4, as requirements questions.
- **Goals:**
  - Give the domain a sharper reading of its responsibility, a kernel small enough to defend, a placement for every existing folder, and the missing pieces named. — Met as proposal
  - Leave the owner a short list of decisions, each with a recommended default and what it blocks. — Met
  - Say where the domain meets [product](../product/product.md), [account](../account/account.md) and [transaction](../transaction/transaction.md) without editing any. — Met, findings 5 and the reconciliation
- **Scope:** the `modules/economics/invoice` domain, its fourteen edge folders, its four status folders and its `pre-order` shortcut; the invoice-touching pluggables in `modules-plugable/economics` are read, not changed. Out of scope: the data-model pass, any `.kh` file, moving or deleting any folder, the domain Model and Policies, and re-arguing what the documents mark Decided.

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — Questioner, Goal-setter, Reviewer (Not yet reviewed). He asked for conceptual development of the base domains while away and unavailable for questions (survey session `20261014T071207Z-28148-0`).
- An AI agent (Claude, model `claude-sonnet-5-5` as reported by the runtime; [CONTRIBUTORS.md](../../../CONTRIBUTORS.md) has no entry for it) — Researcher, session `20261018-T184248Z-15520`.

## Starting Evidence
The domain's documents, read in full: [invoice.md](invoice.md), [invoice.handoff.md](invoice.handoff.md), all fourteen edge documents (`conditional`, `item`, `pay_by`, and the eleven `user-*`), the four `status/<state>` documents and [status.md](status/status.md), [pre-order](edges-shortcut/pre-order/pre-order.md), the two `.kh` files ([dt-uuid.kh](protocol/dt-uuid.kh), [item data_model.kh](edges/item/protocol/data_model.kh), the latter only a `TODO(go-migrate)` block). The domain has no changelog; this research creates it. Questions the documents already hold open and that move this research: zero-product invoices; whether partial payment is invoice-side or analytics-side; reconciliation with the general status domain; the `RulePrice` naming; the invoice's own record having no `## Model` ([handoff, Khayyam conversion](invoice.handoff.md#open-from-this-pass)); and invoice exchange between organizations ([handoff](invoice.handoff.md#open-questions)).

Neighbours read at the passages cited: [transaction.md](../transaction/transaction.md), [transaction reference](../transaction/edges/reference/reference.md), [transaction.handoff.md](../transaction/transaction.handoff.md); [product.md](../product/product.md); the pluggables [discount](../../../modules-plugable/economics/discount/discount.md), [voucher](../../../modules-plugable/economics/voucher/voucher.md), [refund](../../../modules-plugable/economics/refund/refund.md), [pricing](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md), [price-index](../../../modules-plugable/economics/price-index/price-index.md), [payroll](../../../modules-plugable/economics/payroll/payroll.md), [pos](../../../modules-plugable/economics/pos/pos.md), [settlement](../../../modules-plugable/economics/settlement/settlement.md), [credit](../../../modules-plugable/economics/credit/credit.md), [club-coin](../../../modules-plugable/economics/club-coin/club-coin.md), [invoice-totals](../../../modules-plugable/economics/analytics/invoice-totals/invoice-totals.md); [contract](../../rights/contract/contract.md), [ownership](../../rights/ownership/ownership.md), [status](../../knowledge/status/status.md), thing [supersedes](../../identity/thing/edges/supersedes/supersedes.md); and the area surveys and owner-question catalogue ([economics-core report](../../../temp/sessions/20261014T071357Z-29392-0/report.md), [catalogue](../../../temp/sessions/20261014T071404Z-26308-0/report.md)) as claims, not authority.

## Methodology
One reasoning pass by one agent. No second cognitive system was consulted and no organization was asked. The scenarios are reasoning from general knowledge of practice in several countries and industries, not retrieval and not observation; a custom, figure or named system is illustrative and nothing in the findings rests on its exact value.

1. **Reading.** Read in this session: the sources above; [modules.md](../../modules.md); [Khayyam practice](../../../temp/Khayyam.practice.md) (only to know what this session must not write; rules 1, 5 and 6 matter: an empty abstraction is a smell, so an `InvoiceModel` is not proposed until the kernel below says what it adds); [concept-synthesis.md](../../../temp/sessions/20261014T071207Z-28148-0/concept-synthesis.md); the [account research](../account/account.research.001.md) in full; the other siblings ([product](../product/product.research.001.md), [task](../../management/task/task.research.001.md), [content](../../knowledge/content/content.research.001.md), [text](../../knowledge/text/text.research.001.md), [group](../../management/group/group.research.001.md), [thing](../../identity/thing/thing.research.001.md), [user](../../identity/user/user.research.001.md)) only by search for every mention of an invoice, plus the product research's open questions and kernel section.
   **Not read, so any statement about them is unverified:** the siblings beyond those passages; the bodies of `restriction`, `vat`, `batch`, `service`, `good`, `inventory` and the `pos` edges beyond the lines that mention an invoice; the Go legacy behind the `.kh` residue and the `_import/` code; the shared status domain beyond its opening; `rights/delegate`; the full Memar documents (only the passages named below, read through `memar content section`).
2. **Memar's criteria,** read as written: [Modularity → What Earns Foundational Status](../../../docs/modularity.md#what-earns-foundational-status), [Pluggable Behavior](../../../docs/modularity.md#pluggable-behavior), [Capability Completeness](../../../docs/modularity.md#capability-completeness), [Event as a Module Capability](../../../docs/modularity.md#event-as-a-module-capability) (whose worked example is an invoice transition that an optional module may refuse before it is finalized); and, by the sibling researches' reading, [Modeling → Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels), [Acquired vs. Discovered Data](../../../docs/modeling.md#acquired-data-vs-discovered-data), [State Change as Events](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates), [One Authoritative Location per Concern's Data](../../../docs/modeling.md#one-authoritative-location-per-concerns-data), [A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once); and [Modeling Practice → The Modeling Workflow](../../../docs/modeling.practice.md#the-modeling-workflow). Those two Modeling-document sections were taken from the sibling researches' quotation of them and the repository's own handoff, not re-read in full here.
3. **Terms, defined before use.** Memar defines none of "invoice", "claim", "line", "payable" or "party"; a term no Memar document defines carries its ordinary meaning ([Terminology → The Default Meaning of an Unreferenced Term](../../../docs/terminology.md#the-default-meaning-of-an-unreferenced-term)). The repository's own definitions are used where they exist.

| Term | Meaning used here | Governing source |
|---|---|---|
| **Invoice** | A statement of what is claimable between parties: a seller's assertion of what it delivered and at what price. | [invoice.md](invoice.md#definition-in-memar) |
| **Claim** (agent term, ordinary meaning) | An assertion that one party may demand something of another. The invoice states one; whether "claim" is a concept of its own is model C below. | agent proposal |
| **Issue** (agent term) | The act that turns a working draft into an asserted, immutable statement; an acquired fact with a time and a declarer. Not a repository term. | agent proposal |
| **Line / item** | One reference from an invoice to a product with a quantity and the price it was issued at. | [item.md](edges/item/item.md), [data_model.kh](edges/item/protocol/data_model.kh) |
| **Payable** | What the party claimed against is asked to pay: the item's `PayablePrice`, "total price user pay to organization". | [data_model.kh](edges/item/protocol/data_model.kh) |
| **Settlement** | Realized transactions that reference the invoice as their cause. | [invoice.md](invoice.md#definition-in-memar), [transaction reference](../transaction/edges/reference/reference.md) |
| **Transaction** | A request by users for a bookkeeping change; not an operation; one source, one destination. | [transaction.md](../transaction/transaction.md) |
| **Product** | A thing admitted to economic acts (research proposal) or, in the document, anything priceable. | [product.md](../product/product.md#definition-in-memar), [Product Research 001](../product/product.research.001.md) |
| **Status** | A loop-edge on a record; the move between statuses is an event. | [status.md](../../knowledge/status/status.md#what-a-status-is) |
| **Kernel, pluggable, capability, edge buckets** | As in [Modules → Placement](../../modules.md#placement) and [Edge buckets](../../modules.md#edge-buckets). | modules.md |
| **Acquired / discovered** | Acquired data is stated by an external source and cannot be recomputed; discovered data is derived from it. | Memar modeling |
| **Counterparty organization** (agent term) | The organization of the party an invoice is claimed against (or by), when it is not the issuing organization. | agent proposal |

**Limits.** One agent, one pass, no organization consulted. Statements about what a tax authority, an insurer or a marketplace does are the researcher's judgment.

## Findings
### 1. What the domain is for

**Statement (agent, Tentative).** The invoice domain answers one question for the rest of economics: *who asserted, at one moment, that what may be demanded of whom, for what, at which agreed amounts, and what became of that assertion?* It owns the **memory of an agreed claim**: an assertion that is drafted freely, becomes a fact when issued, is answered by the party it is made against, and afterwards is only ever settled, corrected or withdrawn by further facts, never edited. It deliberately decides nothing about what the lines are (product), what the prices were derived from (pricing, replacement cost), how quantity moved (account, transaction), who owns what (ownership), what the parties agreed beforehand (contract), who may adjust (discount, voucher, tax), or how a claim reaches another organization (a capability, below).

**What the documents already say (source).**
- An invoice is a statement of what is claimable between parties; a payslip is invoices between employee and organization; tax is pluggable; transactions settle invoices ([invoice.md](invoice.md#definition-in-memar)).
- Its lines are `(invoice)-[:invoice_item]->(product)`, a candidate edge, and the item holds the price it was issued at as its own fact (answered 2026-10-10, unratified) ([item.md](edges/item/item.md#open-questions)).
- It exposes `condition_is` and nothing rule-specific ([conditional.md](edges/conditional/conditional.md)).
- Roles are edges to the user ([user-seller](edges/user-seller/user-seller.md) and ten siblings); settlement is `(transaction)-[:transaction_reference_is]->(invoice)` ([reference](../transaction/edges/reference/reference.md#model)).

**The finding that moves the domain (agent, Tentative; owner questions 1 to 4).** The documents describe an invoice as a shop sale that has already happened and is paid or not. Four things a claim owner must say are left in no document:
- **When the statement becomes a fact.** There is no draft/issue boundary. The invoice.md Definition says a VAT module "adds a line to an existing invoice", the item says discounts are "directly assigned by users", and the paid state says a paid invoice cannot change: nothing says when the lines stop being editable (scenarios S1, S2).
- **What answers the statement.** Settlement is discoverable from transactions, but acceptance, rejection, clearance by an authority and dispute are acts of the counterparty with no home ([exchange question](invoice.handoff.md#open-questions); S2, S9).
- **How an issued invoice is corrected.** Only an unpaid, issued invoice "can be cancelled" ([voided](status/voided/voided.md)); every other mistake has no stated mechanism except the transaction rule that corrections are compensating records ([transaction.handoff.md](../transaction/transaction.handoff.md#decisions), item 6) (S3).
- **What an invoice is not.** The first line of invoice.md says its main purpose is "to ChangeOwner of products", while the Definition says it is a claim and the account and ownership documents say holding is not title and rights come first. A service invoice changes no owner (S4, S5).

**The completable classification sentence** ([Modeling → Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels)) for the proposal: *a thing may be classified as an invoice because an issuer has asserted a claim (an acquired fact with a time and a declarer) naming a claimant and a party claimed against, and therefore the party claimed against may answer it, transactions may name it as their cause, a correction may point at it, and rules may attach to it.* A label that cannot complete that sentence is not an invoice relation (finding 5).

**What the domain is not for (agent, with sources).**
- Not the order, the delivery note, the receipt, the quote or the pro-forma: these are the same claim at other moments or with other force (a quote "is not an invoice", [quote](../../../modules-plugable/economics/replacement-cost/edges/quote/quote.md)); the ERP chain of five documents is five labels, tested in model D.
- Not payment status: `paid` and `paid-partially` are derived from transactions (finding 3, smaller choice 1).
- Not tax, salary, commission or discount: each is a pluggable producing lines or invoices.
- Not title transfer: "ChangeOwner" is an effect a fulfilled claim may have, caused by whoever fulfils it, in `rights/ownership` ([contradiction 1](#contradictions-found)).

#### Scenarios

Eleven cases from several countries and industries. For each: what happens, what the obvious model says, what breaks, and what it asks of the domain. S1 to S8 are load-bearing; all are used in the model comparison. Names and figures are illustrative.

**S1. A table at a restaurant (Tehran, Istanbul, Tokyo).** The waiter opens a table at 20:00 and adds dishes for two hours; five people eat; four pay their own shares, one pays for two and tips; the kitchen receives each line as it is added, before any payment.
- *Obvious model:* one invoice with a customer who pays.
- *What breaks:* lines are added for hours, so "the invoice" exists and is changing before it is a claim; customer, buyer, consumer and payer are different people (Decided in the handoff, [roles](invoice.handoff.md#decisions)); the payer is plural and each pays a share; a tip is not a product the restaurant claims.
- *Asks of the domain:* a mutable working phase before issue (draft), with lines that other capabilities already act on (kitchen, [pos](../../../modules-plugable/economics/pos/pos.md)); issue freezes; payers are discovered from transactions, or declared as shares by a payer capability, never the claim's own shape.

**S2. A cleared e-invoice (Italy's exchange system, Mexico's stamped invoices, Turkey's e-fatura, Iran's tax-authority registry).** A seller prepares an invoice. It is not valid until a state system accepts it, assigns an identifier, and may reject it with a reason; the buyer's side receives it through the same system; a cancellation is possible only within a window and through the same system.
- *Obvious model:* the seller issues and the buyer gets a copy.
- *What breaks:* validity depends on a third party's answer; the legal number is assigned by someone other than the issuer (identity is not that number); rejection is a normal event; gapless numbering by series is a legal property in some places, not a database property.
- *Asks of the domain:* "issued" must be able to wait on an answer (the [event-target example](../../../docs/modularity.md#event-as-a-module-capability) of an optional module refusing a transition before it is finalized); the legal number is a reference from a numbering capability; the authority is a party to a capability, not to the kernel.

**S3. A return, a price error, a deposit bottle (Germany's returnable-bottle deposit, a retail return in the US, a corrective invoice in Iran).** A paid invoice of ten items: two come back damaged; the price of one was wrong by 3 percent; later a bottle deposit is refunded.
- *Obvious model:* void and reissue, or edit.
- *What breaks:* a paid invoice cannot be voided or edited ([paid](status/paid/paid.md), [voided](status/voided/voided.md)); the refund edge points to a rule and names no coupled claim ([refund](../../../modules-plugable/economics/refund/refund.md)); a refund of what price (issued, or replacement cost today) is open there; the invoice is a tax fact, so erasing is illegal in most places.
- *Asks of the domain:* a correction is a new invoice that points at the one it corrects and carries negative lines, not an edit and not a void; void remains for "never took effect".

**S4. A salary and a property tax (any country).** The employer computes pay from attendance, withholds tax and insurance, and "issues" the payslip; the employee never asserted anything. A municipality assesses a property tax: the payer neither ordered nor chose, and the amount is the result of a rule over facts.
- *Obvious model:* the seller issues to the buyer.
- *What breaks:* the claimant is not the issuer in the payslip (self-billing, a buyer-issued invoice is a known practice); the tax has no choosing buyer, which the repository already models as a "forced purchase of a government-offered product" ([invoice.md](invoice.md#prior-art)) and the product research defaults to "a rule on issue" ([Product Research 001, question 13](../product/product.research.001.md#open-questions)); both are claims whose issuer is a rule.
- *Asks of the domain:* issuer (the declarer of the issue event) is not the same relation as claimant (seller); the issue is declared by a person, a rule or an authority; roles come from the capability that creates the invoice.

**S5. A recurring and a measured bill (a SaaS subscription, an electricity bill read monthly from a meter in Japan, a mobile-data plan with overage).** A period ends, usage is measured, an invoice is produced without anyone ordering it that month; some are issued in advance, some in arrears; a missed meter reading is estimated and corrected next month.
- *Obvious model:* a scheduled job creates invoices.
- *What breaks:* the price is a function of discovered data (usage) rather than a stated price version; an estimate is a claim that is knowingly provisional; the correction is S3 again.
- *Asks of the domain:* a billing-cycle capability that produces invoices by rule (the same way payroll and tax modules already "listen to events and produce invoices"); the kernel needs no recurrence.

**S6. A pre-sale paid over years, in an inflating currency (the owner's apartments; a Turkish or Iranian forward contract).** An apartment that does not exist yet is sold now; the buyer pays 24 instalments; the seller's cost of building rises; a fixed amount paid in two years is worth a fraction.
- *Obvious model:* an invoice for the full price plus a payment plan.
- *What breaks:* the claim is a schedule of dated amounts, each possibly indexed to a basket ([price-index → Deferred-payment sales](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales)); the item's product does not exist ([pre-order](edges-shortcut/pre-order/pre-order.md)); the "payable" is a rule's result at each due date, not a number at issue.
- *Asks of the domain:* the issued claim states the amount agreed and the rule that fixes later amounts; each due entry is a deferred transaction referencing the invoice (a transaction "may be deferred", [transaction.md](../transaction/transaction.md)); the schedule capability is not credit and not settlement (both say so in their own open questions, [credit](../../../modules-plugable/economics/credit/credit.md), [settlement](../../../modules-plugable/economics/settlement/settlement.md)).

**S7. A marketplace and a broker (a Chinese or Iranian online marketplace, a travel agent, a franchise).** The buyer pays the marketplace; the marketplace keeps a commission and pays the seller later; the seller's invoice is to the buyer, the commission invoice is from the marketplace to the seller; the delivery is by a courier who issues nothing.
- *Obvious model:* one invoice with seller and buyer.
- *What breaks:* the money path and the claim path differ; one purchase yields several invoices between different pairs, each caused by the first; `broker`, `agent`, `franchise` and `provider` roles of the existing edges are each a relation with processing (commission, royalty, staff pay) but no document states it.
- *Asks of the domain:* a claim may cause other claims ("listens to events and produces invoices", the tax and payslip pattern), so a caused-by relation between invoices is needed, and roles other than seller and buyer belong to the capabilities that process them.

**S8. A grocer's credit notebook and a fine (the Indian khata, the Iranian shop's credit ledger, a traffic fine, a court-ordered compensation).** The grocer writes "Ahmad owes 120" without lines; a fine is owed to the state with no product at all.
- *Obvious model:* an invoice needs products.
- *What breaks:* the question [invoice.md already asks](invoice.md#unresolved-questions): "Can an invoice exist with zero products (a pure claim)?" Here yes, in two forms: a claim with no lines (the fine), and a claim whose lines are summarized (the notebook).
- *Asks of the domain:* zero lines are permitted; what the claim is for may be a reference to a cause (a case, a law) rather than lines, which is the fine's case and the product research's [authority-declared product](../product/product.research.001.md#6-missing-edges-and-modules) in other words. The kernel is the claim; lines are a capability of it that most claims use.

**S9. A health-insurance claim (Japanese reviewed receipts, Iranian prescription billing, US third-party payment).** A clinic bills the insurer for 10 lines; the patient pays a co-payment; the reviewer accepts 8 lines at a reduced tariff and rejects 2.
- *Obvious model:* one payer.
- *What breaks:* two parties owe parts of one set of lines; acceptance is per line and may change the amount; the tariff is not the price the clinic stated.
- *Asks of the domain:* an answer by the party claimed against can be per line and carry an amount (a partial acceptance, handoff question), and the portion owed by each payer is a payer-share capability; one rejected line does not void the invoice.

**S10. Progress billing on a construction contract (an Iranian "status statement", an AIA-style pay application).** Each month the contractor bills the cumulative work done minus earlier statements; an engineer certifies it before it is payable; 10 percent is held back and released after completion.
- *Obvious model:* a monthly invoice.
- *What breaks:* each invoice is a delta against earlier invoices of the same contract; certification is a third party's act; the retained part is a claim that exists but is not yet demandable.
- *Asks of the domain:* invoices relate to a contract and to earlier invoices; "claimable now" is not the same as "claimed" (a due date or a release condition, evaluated by a rule); certification is the same capability shape as S2.

**S11. A cross-border sale (a Turkish seller to a German buyer in euros, paid in lira through a third bank).** The invoice is in euros; the buyer's bank sends dollars; a reverse-charge VAT note replaces German VAT.
- *Obvious model:* currency on the invoice, one payment.
- *What breaks:* the unit of the claim is not the unit of the settling transaction; [account research](../account/account.research.001.md#5-how-the-existing-edge-folders-map) says "the unit of a payment is the unit of the paying account and must equal the invoice's currency", while a cross-unit movement is two transactions linked by an exchange ([transaction.md](../transaction/transaction.md#policies-rules)).
- *Asks of the domain:* the claim states its unit; settlement of a claim in another unit goes through the exchange pair, and "settled" is evaluated in the claim's unit; the invoice has no account.

### 2. Minimal kernel and what must be pluggable

**Tests applied (source).** [Modules → Placement](../../modules.md#placement): kernel only if its removal forces a foundational type to be fabricated or distorted; pluggable if an optional capability attaches through an explicit relationship and owns relation and processing together; an edge becomes its own module only with independent identity, lifecycle, authorization, rules or processing; no bare edges (who may create or remove it, and what it triggers); the kernel never references the rule domain directly; analytics is never kernel; behaviour binds to a UUID.

#### The removal test run on the invoice itself (agent, Tentative)
Remove the invoice domain. What is forced?
- A seller's assertion of an agreed price at one moment needs a node. A transaction cannot carry it (the transaction records a request for a quantity change; it holds no items, no agreed price, and the payer's account may be unknown when the price is agreed, S1). A product cannot carry it (it is the same across all sales). A contract cannot (it comes earlier and is not repeated per sale). So the assertion has no home but a thing marked as a claim; the marker with its rules is the invoice.
- The independent-lifecycle test ([Concept Existence vs. Model Existence](../../../docs/modeling.md#concept-existence-vs-model-existence)) is met by what no neighbour owns: the draft-to-issue boundary, the answer by the other party, the correction rule, immutability after issue. These are the rules the documents lack (finding 1) and so owner question 1 decides between model B and C.

#### Proposed kernel (agent, Tentative)

| Kernel element | Why kernel | Note |
|---|---|---|
| Invoice identity: a `ThingUUID` (`InvoiceID`, exists) | the thing marked as a claim; the legal number is not identity | [dt-uuid.kh](protocol/dt-uuid.kh) already values it as `ThingUUID`; an `InvoiceModel` is unwritten and Khayyam rule 6 forbids an empty one, so this research is the missing "what is added" |
| Two party relations: the claimant and the party claimed against (today `seller_is`, `buyer_is`) | a claim names who may demand of whom; remove them and the assertion has no subject | the other nine roles are capabilities (below) |
| The line: `(invoice)-[:invoice_item]->(product)` with quantity, the price as issued as its own fact (amount, unit, reference to the price version) | the agreed price at one moment | exists as candidate; zero lines allowed (S8) |
| Lifecycle events with declarer and time: issued, answered (accepted or rejected, per line or whole), voided | the acquired facts; overwriting them discards who and when ([State Change as Events](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates)) | statuses as loop-edges on the shared vocabulary ([status](../../knowledge/status/status.md#what-a-status-is)); where they live is survey question R4 |
| `corrects`: `(invoice)-[:corrects]->(invoice)` | an issued claim cannot be edited, so a way to offset it is forced | not `supersedes` (that replaces and leaves one record standing; a credit note offsets and both stand); the place for the relation is open (question 6) |
| An event target for the transitions (issue, answer, void) | optional modules must be able to refuse a transition before it is final | the [event-target example](../../../docs/modularity.md#event-as-a-module-capability); whether a domain target constrains its events is the open memar question A7 ([synthesis](../../../temp/sessions/20261014T071207Z-28148-0/concept-synthesis.md)) |
| The `condition_is` attachment | the kernel exposes where rules attach and never what they say | already [conditional](edges/conditional/conditional.md) |

Not the invoice's, though invoices have them: payment status (discovered from transactions), the settling reference (transaction's), the amounts' derivation (pricing), title (ownership), tax (a product), the eleven party roles beyond two, numbering, clearance, exchange, schedules, templates.

#### Pluggable: the capability each would own

"Created/removed by" and "Triggers" are read from the cited document where it states them, otherwise marked as gaps ([Modules → Placement](../../modules.md#placement): no bare edges).

| Capability (home) | Relationship and processing it owns | Created / removed by | Triggers |
|---|---|---|---|
| **adjustment** (proposed, new; absorbs the effect of [discount](../../../modules-plugable/economics/discount/discount.md), [voucher](../../../modules-plugable/economics/voucher/voucher.md), [club-coin](../../../modules-plugable/economics/club-coin/club-coin.md), manual staff change) | a signed amount on a line or an invoice, with a reference to its cause (a rule, a staff authorization, a tax); the item's `PayablePrice` is suggested plus the adjustments | before issue: rules by the issuer's configuration, or authorized staff; none after issue (a correction instead) | recomputes the payable; emits an event for the issuer's listeners. Naming open ([RulePrice](invoice.handoff.md#decisions)) |
| **tax** (`vat` exists; reclassify in place) | an item whose product is a tax product declared by an authority (Decided as a product in 2026-09-16, per [Product Research 001, S4](../product/product.research.001.md#scenarios)); jurisdiction rules produce it | the jurisdiction's module, before issue | adds a line, or issues a separate invoice; its basis rule is [VAT's own open question](../../../modules-plugable/economics/vat/vat.md) |
| **numbering** (proposed, new) | a legal number and series, gapless where the jurisdiction says so, as a reference to the invoice | the issuer's organization; assigned at issue; never removed | the number on issue; a gap detector reports a hole |
| **clearance** (proposed, new) | an authority's registration and answer; its identifier | the issuer, where the jurisdiction requires | issue waits for the answer; a rejection is an event with reasons |
| **exchange** (proposed, new) | delivery of an invoice to the counterparty organization, the receipt, the answer, the timeout; the product-identifier mapping | the sender (by rule on issue); the receiver answers; no one removes a delivery | the receiver's `condition_is` rules decide acceptance; replacement cost re-evaluates on an accepted purchase ([handoff](invoice.handoff.md#open-questions)) |
| **payer** (proposed; the `payer`, `sponsor` of [pay_by](edges/pay_by/pay_by.md) become its roles) | who is expected to pay, with shares (S1, S9); the actual payer is discovered from the settling transactions | the issuer at draft, or the party claimed against by agreement | a share unmet raises an event; the shares sum to the payable |
| **intermediary** (proposed; `agent`, `broker`, `franchise`) | the relation and the commission or royalty invoice it causes (S7) | the issuer, by rule from a standing agreement | a caused-by invoice to the intermediary |
| **fulfilment** (proposed; `consumer`, `provider`) | who receives or performs; links to [staff](../../management/staff/staff.md) and to [payroll](../../../modules-plugable/economics/payroll/payroll.md) | by rule at the order (the provider-edge document already says "a rule set this relation" and calls a staff) | work credit for the performer; delivery |
| **origin** (proposed; `orderer`, `applicant`) | who started the draft (a waiter, a doctor, a sales agent, an applicant for a permit) | the actor at draft | the creator's attribution; authorization checks at draft |
| **payment-schedule** (proposed, new) | dated due entries, each a deferred transaction referencing the invoice; indexed amounts via [price-index](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales) | the issuer, from the agreed terms; amendable only by a correction | the transaction at each due date; the warning at approval |
| **billing-cycle** (proposed; may be a rule on [task](../../management/task/task.md) recurrence, Explored) | produces invoices per period from discovered usage (S5) | the issuer | an invoice per period; estimates flagged |
| **contract-billing** (proposed, Explored) | the relation to a contract, cumulative billing, retention and certification (S10) | the contract's parties | claimable-now evaluated by a rule |
| **refund** (exists: `(invoice)-[:refund]->(rule)`) | repay rule for a correction | not stated: gap | repayment transaction |
| **pos issuer / editor** (exist in [pos](../../../modules-plugable/economics/pos/pos.md)) | the register that issued or edited the invoice | the register's rule | print, kitchen |
| **invoice-totals** (exists, analytics, `invoice_summary`) | discovered totals; never acquired | not applicable | not applicable |
| **negotiation** (a task kind; [task research](../../management/task/task.research.001.md)) | counter-offers on an invoice or offer | the parties | an accepted result changes the draft |
| **print / template** (exist in pos) | the layout of an invoice for a customer or kitchen | the register's owner | rendering only |

The pattern across the table: where a capability exists, the tree rarely states in full who creates it, who removes it and what it triggers; where it is proposed, all three are given. The eleven `user-*` edge documents state none of the three except `orderer` (creator) and `provider` (rule-set). They are listed as work in finding 5, not repaired here.

### 3. Rival models

#### The models
- **A. Status quo: invoice = a record + `invoice_item` + eleven user edges + stored status folders (Explored; the current state).** Minimal in documents and right for the common shop sale. Trade-offs: no draft/issue boundary; payment states stored where they can be computed; no answer, correction or exchange; eleven bare-looking edges; the invoice's own record has no Model.
- **B. Claim kernel: the seven-element kernel of finding 2, with the answer and correction as events and relations, and everything else pluggable (Tentative; recommended).** Keeps every Decided statement true: roles stay distinct edges, tax and payslips stay compositions, the item price stays its own fact. **Migration cost is low by construction:** an existing invoice is simply "issued" at its creation; nothing visible changes until the first draft, correction or exchange.
- **C. Claim (obligation) as the concept; invoice is its document form (Explored; the strongest rival).** Following the [Premature Classification Check](../../../docs/modeling.practice.md#premature-classification-check): S8 shows claims with no lines, S10 a claim not yet demandable, S4 a claim issued by a rule; [contract](../../rights/contract/contract.md) already says rights and obligations arise from contracts and the rights domain puts rights first ([ownership](../../rights/ownership/ownership.md)). Then an invoice is a labelled document over a right-and-obligation pair, e-invoice formats and numbering are its pluggables, and the kernel is smaller. It becomes the better model if a rights/obligation domain is ratified and the independent-lifecycle test fails (question 1). The synthesis's own idea was "an Obligation module only if a case breaks Right + correlation edge" ([concept-synthesis](../../../temp/sessions/20261014T071207Z-28148-0/concept-synthesis.md#next-domains-worth-the-same-treatment)); S6 and S10 are candidates for that break.
- **D. Order-first chain: quote, order, delivery note, invoice, receipt as separate domains (Explored; rejected for the kernel).** The ERP shape. The repository already puts the agreed price at the invoice (the invoice at the "previous price" is the exchange problem, [handoff](invoice.handoff.md#open-questions)) and has a pre-order invoice; five documents for one claim at five moments is the false taxonomy [Modeling](../../../docs/modeling.md#false-taxonomies-hide-shared-structure) warns of. The status.md proposals (UserCheckout, Packaging, Shipping, Done) belong to a retail pluggable ([status.md](status/status.md#open-questions-cross-state)).
- **E. Invoice as a view over transactions: a deferred transaction with items (Explored; the cases refuse it).** A claim of 120 from A to B is a pending transaction from B's account to A's account. Simple where accounts are known at issue. Fails S1 (the paying account is chosen later, by several payers), S2 (the claim exists and is cleared before any account), S8 (a claim with no accounts), and gives no home to lines and agreed prices. It survives in B as the schedule: each due entry is a deferred transaction.
- **F. Two invoices, one per organization, as counterparts (Explored; exchange model).** See the exchange choice below; it is a sub-choice of B or A, not a rival to them.

**Not re-argued (Decided or confirmed, source):** the three party-role distinctions; no `discount` field on the invoice; a payslip as invoices; tax pluggable; transaction is a request and corrections are compensating records; a purchase invoice item is history; one authoritative location per concern's data ([invoice.handoff.md](invoice.handoff.md#decisions), [transaction.handoff.md](../transaction/transaction.handoff.md#decisions)).

#### How each model meets the cases (agent judgment)
"Fits" means no distortion; "strained" means it works only with a workaround; "fails" means it forces a wrong statement.

| Case | A status quo | B claim kernel | C claim as concept | D order chain | E transaction view |
|---|---|---|---|---|---|
| S1 table | strained (no draft) | fits | fits | strained | fails |
| S2 cleared e-invoice | fails (no answer) | fits (event target) | fits | strained | fails |
| S3 return, correction | strained (void only) | fits | fits | strained | strained |
| S4 payslip, tax | strained (seller must issue) | fits (issuer separate) | fits | fails | strained |
| S5 recurring bill | fits | fits | fits | strained | strained |
| S6 pre-sale, indexed | strained | fits with schedule | fits | strained | fits |
| S7 marketplace | strained (roles bare) | fits (caused-by) | fits | strained | fails |
| S8 notebook, fine | fails (needs products) | fits | fits | fails | fails |
| S9 insurer, partial | fails (one payer) | fits with payer | fits | strained | fails |
| S10 progress, retention | fails | strained, fits with contract-billing | fits | strained | strained |
| S11 cross-border | strained | fits (exchange pair) | fits | strained | strained |

B has no "fails". C ties with B on every case, which is why the difference is not in the cases but in whether a rights/obligation domain exists (question 1).

#### Smaller choice 1: are `paid`, `paid-partially` and `expired` stored statuses (Tentative: discovered, except what a rule or person acts)
`paid` and `paid-partially` are a comparison between the payable and the sum of the realized transactions that reference the invoice: discovered from acquired facts ([Acquired vs. Discovered](../../../docs/modeling.md#acquired-data-vs-discovered-data)), the question the [paid-partially](status/paid-partially/paid-partially.md) and [paid](status/paid/paid.md) documents themselves ask ("one state or multiple part-payments over time (a ledger on the invoice)?"). Storing them copies the ledger onto the invoice (two locations for one fact). What stays acquired: voided, and `expired` only as an event a rule raises at a validity time (the [expired](status/expired/expired.md) question: a rule or an explicit action). The policies "cannot be deleted or cancelled after any payment" become the voiding rule's precondition: it reads the discovered settlement.

#### Smaller choice 2: how an issued claim is corrected (Tentative: a new invoice that points at the original)
- **(i) Edit.** Rejected for an issued invoice: it destroys the asserted fact.
- **(ii) Void and reissue.** Right only when the invoice never took effect (unpaid, unanswered, no transaction yet); today's [voided](status/voided/voided.md) rule.
- **(iii) Corrective invoice with negative lines, pointing at the original (recommended).** Matches the compensating record of [transaction invariant 6](../transaction/transaction.handoff.md#decisions) and the ledger's own rule in [account](../account/account.research.001.md#2-minimal-kernel-and-what-must-be-pluggable). The refund rule consumes it. Cost: reporting must net corrections.

#### Smaller choice 3: invoices between organizations (Explored; recommendation Tentative)
Memar's [one authoritative location per concern's data](../../../docs/modeling.md#one-authoritative-location-per-concerns-data) is scoped to one model; another organization's model is a counterpart ([handoff](invoice.handoff.md#open-questions)).
- **(i) One shared invoice both organizations read.** Needs a place both trust; a mismatch cannot exist; the price is the claimant's alone. Breaks the sibling pattern that each organization's ledger is authoritative for its own accounts ([account, question 13](../account/account.research.001.md#open-questions)).
- **(ii) Two invoices, one per organization, as counterparts.** Each is authoritative in its own organization; the buyer's side books a purchase invoice. Needs a rule for which holds the agreed price when they differ.
- **(iii) One authoritative invoice at the issuer; the counterparty organization holds a received reference and its own booking (recommended default).** The claim is the claimant's assertion; the counterparty's organization answers it with an event (accepted, rejected per line with the seller's current price version) and books its own purchase against its own accounts. A buyer-initiated purchase request is then a draft authored by the buyer's organization that the seller issues or rejects; the draft is the "purchase request" the owner names. Product identifiers then differ per organization with a mapping (agreeing with [Product Research 001, question 4](../product/product.research.001.md#open-questions)). Booking before acceptance is not allowed (already answered 2026-10-10, unratified, [handoff](invoice.handoff.md#open-questions)).

### 4. What the domain must own, as requirements questions

Written as questions favouring no answer where unsettled. A citation means the document already answers or constrains the question; "open" means nothing in the tree decides it.

#### Identity
- What makes two invoices the same: the `ThingUUID` alone? A legal number is a reference (names and handles are never identity, the synthesis agreement) but in a jurisdiction it may be what a tax authority calls the invoice; is it a `uri`-like reference, and can two organizations have the same number? Open.
- Is the issued invoice the same identity as its draft, or does issue mint one? Open (question 3).
- Does an invoice survive a change of seller or buyer (a merger, an assignment of receivable)? Open.
- Is a line an identity of its own? `data_model.kh` carries `InvoiceItemID` valued as a thing identity ([handoff](invoice.handoff.md#khayyam-conversion-2026-10-03)), so the line is a record with fields; the edge is then a node in effect. Open (contradiction 3).
- When the invoice crosses organizations, one identity or one per organization with a mapping? Open (question 8).

#### Lifecycle
- What are the acquired events: drafted, issued, answered, voided, expired? Which are one-way? Open (question 3).
- Can an invoice exist with no lines (a pure claim)? The document asks it ([invoice.md](invoice.md#unresolved-questions)); S8 says yes. Open (question 4).
- Is the answer by the other party a status or an event with content (lines accepted, price offered)? Open (question 8).
- What does a rejection by the counterparty organization carry, and may the sender reissue in one step? Open ([handoff](invoice.handoff.md#open-questions)).
- Can a voided invoice be reopened? Open; default no, a new invoice.
- Does a price-validity window expire an issued but unpaid invoice, per invoice or per line? Open ([expired](status/expired/expired.md), [item](edges/item/item.md#open-questions)).
- What happens to open invoices when a product is withdrawn? Product's default: unaffected ([Product Research 001, question 9](../product/product.research.001.md#open-questions)). Cited.
- Retention: may an issued invoice ever be archived or erased? Open (question 15).

#### Authorization
- Who may draft: the orderer, a rule, an authority, either party? Open.
- Who may issue: the claimant, the claimant's organization, a rule, the party claimed against (self-billing, S4), an authority? Open (question 2).
- Who may answer for an organization: any member, a role, a rule? Open.
- Who may add, change or remove a line or an adjustment before issue? [item.md](edges/item/item.md) says `DiscountedPrice` is assigned "by users with enough authorization access (usually org staff)" ([data_model.kh](edges/item/protocol/data_model.kh)): which authorization? Open.
- Who may void; who may correct? Open.
- Who may read an invoice: both parties, the payer, the consumer, an authority? The voided state says "the customer cannot view it". Cited in part.
- Who may attach each pluggable relation? Mostly unstated (finding 2).
- Across organizations: whose authorization admits an incoming invoice, and is each delivery metered? The handoff already asks it of follow-style delivery. Open.

#### Rules
- Which rules does the kernel itself require? Candidates (own proposal): lines are editable only in draft; an issued invoice is immutable; every line has one product, a quantity in the product's count unit and the price as issued; the invoice has one unit; a correction cannot exceed what was claimed; a voided invoice takes no settlement; the payable equals the sum of line payables. Open.
- Where does the same-unit rule live between an invoice and its settling transactions (S11)? Open (question 12; compare [account, question 15](../account/account.research.001.md#open-questions)).
- Does the line price chain (Suggested, Discounted, Rule, Payable) stay four fields, or reduce to an agreed price plus adjustments with causes? Open (question 5).
- May the seller's rule reject an exchanged invoice for a price difference automatically? The handoff states it as a process error; open.
- Are reserve-validity and its action a rule or item state? Open ([item.md](edges/item/item.md#open-questions)).

#### Events
- Which facts must the domain emit: drafted, issued, answered, voided, corrected, expired? The kernel exposes an event target, not a new event model ([Event as a Module Capability](../../../docs/modularity.md#event-as-a-module-capability)). Open.
- Who listens: adjustment and tax (draft), numbering and clearance (issue), exchange (issue, answer), payment-schedule, replacement cost (accepted purchase), refund (correction), analytics, followers. Is each reaction the listener's own rule, never a cascade the invoice performs? Open.
- May a listener refuse a transition before it is final, as the Memar example has an optional module do? Open; the default is yes, for issue and void only.
- Are invoice events delivered across organizations by the follow mechanism or by the exchange capability? Open ([handoff](invoice.handoff.md#open-questions)).

### 5. How the existing edge folders map

Without moving anything. Verbs: **keep**, **reclassify**, **retire**, **missing**. The mapping applies [Modules → Edge folder](../../modules.md#edge-folder).

| Folder | Verb | Proposed disposition | Basis |
|---|---|---|---|
| `protocol/dt-uuid.kh` | keep | `InvoiceID` valued as `ThingUUID`; no local abstraction (decided in the conversion) | [handoff](invoice.handoff.md#khayyam-conversion-2026-10-03) |
| [edges/item](edges/item/item.md) | keep | The kernel line; its record is a node in effect (own id, quantity, prices, request); reduce the four-price chain only if question 5 is accepted; the reserve-validity policy moves to a rule | its own Placement |
| `edges/item/protocol/data_model.kh`, `storage.kh` | keep (unconverted) | Stay blocked on the money amount; do not convert before question 5 decides the fields | [handoff](invoice.handoff.md#unconverted-and-what-blocks-it) |
| [edges/conditional](edges/conditional/conditional.md) | keep | The `condition_is` attachment; also the place where deferred-payment rules attach today, which the payment-schedule sketch would take out | its own Placement |
| [edges/user-seller](edges/user-seller/user-seller.md) | keep | Kernel claimant relation; add who creates, who removes (before issue), what it triggers | finding 2 |
| [edges/user-buyer](edges/user-buyer/user-buyer.md) | keep, correct | Kernel party-claimed-against relation; its policy defines a buyer as a purchasing employee (contradiction 4); add the three gaps | finding 2 |
| [edges/user-customer](edges/user-customer/user-customer.md), [user-consumer](edges/user-consumer/user-consumer.md) | reclassify | Decided as distinct roles (not re-argued); processing sits in fulfilment or loyalty capabilities; each document must state creator, remover, trigger or it is a bare edge | [handoff](invoice.handoff.md#decisions) |
| [edges/user-payer](edges/user-payer/user-payer.md) | reclassify | The payer capability (shares); the actual payer is discovered from settling transactions | finding 2 |
| [edges/pay_by](edges/pay_by/pay_by.md) | retire (as written) | Its first two lines are the same relation as the transaction's `transaction_reference_is` in both directions, which is the source edge, so `pay_by` is at most a shortcut that must name it; its third line `(pos)-[:pos_issued]->(invoice)` is [pos-issuer](../../../modules-plugable/economics/pos/edges/pos-issuer/pos-issuer.md)'s edge; its policy "any pay type as Direct, Supporter, Sponsor" is payer's | [reference](../transaction/edges/reference/reference.md#policies-rules) |
| [edges/user-orderer](edges/user-orderer/user-orderer.md) | reclassify | The origin capability; "orderer is creator of the invoice" is the one stated policy | its Policies |
| [edges/user-provider](edges/user-provider/user-provider.md) | reclassify | The fulfilment capability; "a rule set this relation" (a staff) | its Policies |
| [edges/user-agent](edges/user-agent/user-agent.md), [user-broker](edges/user-broker/user-broker.md), [user-franchise](edges/user-franchise/user-franchise.md) | reclassify | The intermediary capability; each states only a model | finding 2 |
| [edges/user-applicant](edges/user-applicant/user-applicant.md) | reclassify | The origin capability (a request to an authority, S4); it is the party claimed against in some cases | S4 |
| [edges-shortcut/pre-order](edges-shortcut/pre-order/pre-order.md) | keep, correct | A derived walk over items and a product's future production; but the edges `shipped_in` and `produced_in` it walks are defined in no document found by search (grep over modules, modules-plugable and bundles finds them only in this file); the document must name its source edges | [Edge buckets](../../modules.md#edge-buckets) |
| [status/paid](status/paid/paid.md), [paid-partially](status/paid-partially/paid-partially.md) | reclassify | Discovered from transactions (smaller choice 1), not statuses; their view-only policies become the voiding rule's precondition | finding 3 |
| [status/voided](status/voided/voided.md) | keep | The acquired event; limited to "never took effect"; the rest is a corrective invoice | smaller choice 2 |
| [status/expired](status/expired/expired.md) | keep, reclassify | An event raised by a validity rule; where the time lives is a rule's configuration | its review question |
| [status/status.md](status/status.md) | keep | The retail chain (checkout, packaging, shipping) is a pluggable retail specialization; reconciliation with the shared status domain waits on R4 | its open question |
| `_import/invoice/**`, `_import/invoice-voucher/storage.sql` | retire | Legacy service code; delete or re-model, not convert (already the handoff disposition) | [handoff](invoice.handoff.md#unconverted-and-what-blocks-it) |
| **Not this domain's, reported:** [pos pos-issuer / pos-editor](../../../modules-plugable/economics/pos/pos.md), [refund](../../../modules-plugable/economics/refund/refund.md), [club-coin](../../../modules-plugable/economics/club-coin/club-coin.md), [invoice-totals](../../../modules-plugable/economics/analytics/invoice-totals/invoice-totals.md) | keep | Each already hangs an invoice relation off its own module, as the kernel intends; each should state its creator, remover and trigger | their own documents |
| **Not this domain's, reported:** [gift-product](../../../modules-plugable/economics/gift-product/gift-product.md) `(product)-[:invoice]->(gift)`, [budget](../../../modules-plugable/economics/budget/budget.md) `(account)-[:invoice]->(budget)`, [inventory](../../../modules-plugable/economics/inventory/inventory.md) `(batch)-[:product_inventory]->(invoice)` | — | Three relations whose far end or direction is unexplained; the budget one repeats the relation reported in the [account research](../account/account.research.001.md#contradictions-found), contradiction 6 | their documents |

### 6. Missing edges and modules

Each is a proposal (Tentative or Explored as marked); none is created here. Each names what, who creates and removes, and what it triggers, because an edge without those does not exist ([Modules → Placement](../../modules.md#placement)).

**6.1 Draft and issue — kernel status events (Tentative).** Draft is the state before the issue event; issue is an acquired fact with a time and a declarer (a person, a rule or an authority). Created by whoever may issue (question 2); removed by no one (history). Triggers an event to listeners (numbering, clearance, exchange, schedule) and freezes lines. Sits on the shared statuses and waits on survey question R4.

**6.2 `corrects` — a kernel relation (Tentative).** `(invoice)-[:corrects]->(invoice)` with a reason label; the corrective invoice carries negative lines. Created by the issuer of the original (or an authority) after issue; removed by no one. Triggers the refund rule and a recomputation of the discovered settled state. Check whether thing's `supersedes` plus a label can carry it; its policy says supersession leaves one record standing, which does not fit an offset (question 6).

**6.3 `adjustment` — a pluggable beside `discount` and `voucher` (Tentative).** A signed amount with a cause on a line or on the invoice. Created by a rule or authorized staff before issue; none after. Triggers a payable recomputation and an event. Check against [discount](../../../modules-plugable/economics/discount/discount.md) and [voucher](../../../modules-plugable/economics/voucher/voucher.md) (which both say they adjust an invoice's payable) before it is a new module: it may be a common record they both write. The name is the owner's (the [RulePrice](invoice.handoff.md#decisions) question).

**6.4 `numbering` (Tentative).** A legal number in a series, assigned at issue. Created by the issuing organization's configuration; the assigned number is never removed. Triggers a gap report; the series may be gapless by rule. Check against `uri` references for the form.

**6.5 `clearance` (Explored).** Registration of the invoice with an authority before or after issue, with its answer and identifier. Created by the issuer where required; removed by no one. Triggers a pending issue or a rejection event; a cancellation window is the authority's rule. It is the shape of S2 and of S10's certification; one capability may serve both.

**6.6 `exchange` (Explored; the owner's [purchase request](invoice.handoff.md#open-questions)).** Delivery to the counterparty organization, its receipt, answer and timeout, and the product-identifier mapping. Created by the sender (by rule on issue, or on request); the receiver answers; no one removes a delivery. Triggers the receiver's `condition_is` rules and, on acceptance, the buyer's replacement-cost re-evaluation. Waits on question 8.

**6.7 `payer` (Tentative).** Shares of the payable declared per payer; the actual payer comes from the settling transactions. Created by the issuer at draft or by agreement; removed before issue. Triggers an unmet-share event. Absorbs `user-payer` and the sponsor policy of `pay_by`.

**6.8 `intermediary` (Tentative).** The agent, broker or franchise relation and the invoice it causes (commission, royalty). Created by the issuer by rule from a standing agreement. Triggers the caused-by invoice. Needs a caused-by relation between invoices (question 9).

**6.9 `payment-schedule` (Explored).** Dated due entries, each a deferred transaction referencing the invoice; amounts fixed by a rule, optionally indexed by [price-index](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales). Created by the issuer from agreed terms; changed only by a correction. Triggers the transaction at each due date and the approval warning. The three candidate homes (credit, settlement, the invoice conditional) all say it is not theirs.

**6.10 `contract-billing` (Explored).** Cumulative billing against a contract, retention and its release, certification. Created by the contract's parties. Triggers "claimable now" evaluation. Check against `rights/contract` and `clearance`.

**6.11 `billing-cycle` (Explored; probably a rule, no module).** Periodic production of invoices from discovered usage. Check against the task recurrence pluggable before a module is sketched.

### 7. Test scenarios

Given/when/then in prose, so another session can write tests once the owner decides. Each is marked with what it depends on: **kept** if it follows from settled text, **B** if it assumes model B, **Q n** if it assumes the default of open question n.

1. **A paid invoice is not edited or deleted (kept).** Given an invoice with a realized settling transaction. When someone tries to remove a line. Then it is refused; a correction is the way.
2. **Roles stay distinct (kept).** Given an order for a table of five, placed by a waiter, consumed by five, paid by one. When the invoice is read. Then orderer, consumer and payer are different users and no role implies another.
3. **Settlement is discovered (Q 4).** Given an invoice of 100 with transactions of 60 and 40 referencing it. When its state is read. Then it reads fully paid from the transactions; no stored state was changed.
4. **Partial payment (kept).** Given an invoice of 100 and one transaction of 60. When the state is read. Then 60 settled, 40 outstanding, and the invoice cannot be voided.
5. **Draft lines are editable (B, Q 3).** Given a draft with three lines. When a staff member with authorization adds a line and a VAT listener adds a tax line. Then both are in the draft; after issue neither can be changed.
6. **Issue freezes (B).** Given a draft. When it is issued by the claimant. Then the issue event carries declarer and time, the lines become immutable and the listeners are told once.
7. **Price as issued (kept, unratified).** Given a product price changes from 100 to 120 after issue. When the issued invoice is read. Then the line still reads 100 with a reference to the price version it came from.
8. **Void only if never effective (B, Q 6).** Given an issued invoice with no answer and no transaction. When it is voided. Then a voided event is recorded and it takes no settlement; with a transaction present the void is refused.
9. **Correction by a new invoice (B, Q 6).** Given a paid invoice with two returned items. When the issuer corrects. Then a corrective invoice with negative lines points at the original, the original is unchanged, and the refund rule is told.
10. **Zero lines (Q 4).** Given a fine issued by an authority to a person with no lines and a reference to a case. When it is issued. Then it is a valid claim, and the person may settle it by a transaction referencing it.
11. **Self-billing (Q 2).** Given an organization issues a payslip with the employee as claimant. When it is issued. Then the issue event names the organization as declarer and the employee as claimant; the employee did not issue.
12. **Authority clearance (Q 2).** Given an invoice that requires clearance. When the authority rejects it. Then issue does not complete, the rejection is an event with reasons, and no number was consumed (or a gap is reported if the series is gapless).
13. **Numbering gap (B).** Given a gapless series and numbers 1 to 5 issued. When number 4 is lost. Then a gap report names it; nothing renumbers.
14. **Split payers (Q 11).** Given three payer shares of 40, 40 and 20. When two settle and one does not. Then the unmet share raises an event and the invoice reads partially settled.
15. **Caused invoices (Q 9).** Given a marketplace sale of 100 with a 10 percent commission. When the sale is issued. Then a second invoice from the marketplace to the seller is produced with a reference to the first.
16. **Partial acceptance by an insurer (Q 8).** Given an invoice of ten lines to an insurer. When it accepts eight at a lower tariff and rejects two. Then the answer is per line with amounts; the invoice stays valid; the clinic's claim against the patient is a separate invoice.
17. **Exchange: reject on price (Q 8).** Given a buyer-authored draft at last month's price. When the seller's rule rejects it. Then the rejection carries the items refused and the current price version; the buyer's organization booked nothing.
18. **Exchange: accept books once (Q 8).** Given an accepted invoice. When the buyer's organization books it. Then its booking is in its own accounts; the seller's ledger is untouched by the buyer's booking.
19. **Instalments (Q 10).** Given a pre-sale with 24 due entries indexed to a basket. When the sixth due date arrives. Then a deferred transaction of the indexed amount is created referencing the invoice.
20. **Cross-unit settlement (Q 12).** Given an invoice in euros paid by a lira transaction and an exchange pair. When the state is read. Then "settled" is in euros through the exchange, and the invoice has no account.
21. **Progress billing (Q 14).** Given statements 1 to 3 under a contract with 10 percent retention. When statement 4 is issued. Then it claims the cumulative minus earlier statements, the retention is a claim not yet demandable, and certification is the same event shape as clearance.
22. **Pre-order (kept).** Given an invoice whose product is produced in the future. When it is read. Then it is a pre-order by walk, and no stock is reserved.
23. **Expiry by rule (Q 5).** Given a price-validity window of 30 days. When it passes unpaid. Then a rule raises an expired event; the invoice is view-only, not deleted.
24. **Event target refusal (B).** Given a transport rule that forbids a service for the goods. When issue is attempted. Then the listener refuses the transition before it is final and the invoice stays a draft.
25. **Erasure detaches identity, not the claim (Q 15).** Given a person obtains erasure of personal data. When it is executed. Then the party link and the legal-number references to the person are removed and the claim, its amounts and its settlement remain.

### Contradictions found

Reported, not resolved, as asked. Each cites both sides.

1. **What the invoice is for.** [invoice.md](invoice.md) opens "Main purpose of invoice use to ChangeOwner of products" while its Definition says an invoice is "a statement of what is claimable"; [account.md](../account/account.md) (per the account research) and the [ownership document](../../rights/ownership/ownership.md) say holding is not title and rights come first; services have no owner to change.
2. **Discount.** [The handoff](invoice.handoff.md#decisions) records the proposal that "invoice should not carry a `discount` field", but [data_model.kh](edges/item/protocol/data_model.kh) has a `DiscountedPrice` ("directly assign by users with enough authorization") beside `RulePrice`, and [discount.md](../../../modules-plugable/economics/discount/discount.md) says a discount adjusts the invoice's payable. The field is on the item rather than the invoice, but its name is the cause the handoff counter-argument says the model should not import.
3. **The item is an edge and a record.** [item.md](edges/item/item.md) models `(invoice)-[:invoice_item]->(product)` as a candidate edge, while `data_model.kh` gives it an identity (`InvoiceItemID`), a label, a quantity, four prices and a request identifier: a node in effect. [Modules](../../modules.md#graph-edges) allows an edge to carry some data (time, status); an identity is more.
4. **Buyer.** [user-buyer](edges/user-buyer/user-buyer.md) says a buyer is "someone whose job is to choose and buy the goods for a shop or company", an employee role, while [invoice.md](invoice.md#definition-in-memar) makes the organization the buyer in a payslip and the handoff decides buyer, customer and consumer as three invoice roles.
5. **VAT adds a line to an issued invoice.** [invoice.md](invoice.md#definition-in-memar) says VAT "adds a line to an existing invoice" while [paid](status/paid/paid.md) and the statement of an asserted claim make an issued invoice immutable; nothing states the draft phase that reconciles them.
6. **Voiding versus compensating.** [voided](status/voided/voided.md) says a voided invoice is "not refundable" and the [review question](status/voided/voided.md) asks if void is pre-booking only, while [transaction.handoff.md](../transaction/transaction.handoff.md#decisions) item 6 says no rollback and corrections are compensating. Already asked in the voided document; the answer here is smaller choice 2.
7. **Paid is both a status and a computation.** [paid](status/paid/paid.md) and [paid-partially](status/paid-partially/paid-partially.md) are status folders, while [invoice.md](invoice.md#unresolved-questions) asks whether "partially paid" is invoice-side or analytics-side and [invoice.md](invoice.md#definition-in-memar) says transactions settle invoices.
8. **The settlement relation twice.** [pay_by](edges/pay_by/pay_by.md) states `(invoice)-[:pay_by]->(transaction)` and `(transaction)-[:reference]->(invoice)`; [transaction reference](../transaction/edges/reference/reference.md#model) states `(transaction)-[:transaction_reference_is]->(thing)` and `(thing)-[:financial_transaction_is]->(transaction)`, and says the reference "can't be changed after registered". The names differ and one is not defined by the other. Its third line duplicates [pos-issuer](../../../modules-plugable/economics/pos/edges/pos-issuer/pos-issuer.md).
9. **Direction of a role relation.** Each `user-*` document records two edges in two directions in one folder (`buyer_is` and `buyer_for`), and the prefix "(note: product)" on the first line has no stated meaning; [Agency](../../../docs/agency.md#the-agent_for-relationship) requires the direction convention to be stated (as the [user research](../../identity/user/user.research.001.md) also reports, its C7).
10. **Names that differ for one idea.** `provider` and `provides` (user-provider) against the `x_is` / `x_for` pattern of the other ten; the edge folder `user-franchise` has `franchise_by`/`franchise_for`; `user-orderer` has `orderer_of`; the pattern is not one.
11. **The pre-order walk uses undefined edges.** [pre-order](edges-shortcut/pre-order/pre-order.md) names `shipped_in` and `produced_in`; a search over the repository finds them in no other document.
12. **The kernel names pluggables.** [conditional.md](edges/conditional/conditional.md) names discount, VAT and restriction; [item.md](edges/item/item.md) names the rule domain and pricing; against "Kernel does not reference the rule domain directly" ([Modules](../../modules.md#placement)). The same finding as [Product Research 001, contradiction 5](../product/product.research.001.md#contradictions-found) and [Account Research 001, item 8](../account/account.research.001.md#contradictions-found).
13. **Unit of the claim and of its settlement.** The [account research](../account/account.research.001.md#5-how-the-existing-edge-folders-map) says the payment's unit must equal the invoice's currency; [transaction.md](../transaction/transaction.md#policies-rules) says cross-unit intent is two transactions linked by an exchange (S11). Neither says who refuses.
14. **Purpose of the invoice's own record.** The handoff reports that [invoice.md](invoice.md) "has no `## Model` section" ([handoff](invoice.handoff.md#open-from-this-pass)) while the status folders and the item assume the invoice record's fields (total, currency, issue date, parties).

### Reconciliation with the sibling researches

The same task was done for [product](../product/product.research.001.md), [task](../../management/task/task.research.001.md), [content](../../knowledge/content/content.research.001.md), [text](../../knowledge/text/text.research.001.md), [group](../../management/group/group.research.001.md), [thing](../../identity/thing/thing.research.001.md), [user](../../identity/user/user.research.001.md) and [account](../account/account.research.001.md). Read as claims; only the passages cited are relied on, and only product and account were read beyond search hits.

**Agreements.**
1. **The same kernel shape.** Identity, one or two structural relations, events, a `condition_is` attachment, and pluggables that own relation and processing together (the [synthesis](../../../temp/sessions/20261014T071207Z-28148-0/concept-synthesis.md#one-shape-appears-in-all-four)).
2. **A correction is a new fact.** Bookkeeping, tombstones, immutable text values, task supersession (synthesis addendum). Here: the corrective invoice.
3. **Status as events on the shared vocabulary, waiting on R4.** Product, task, content, account; here too.
4. **An explicit act with a declarer.** Product admission and account opening; here the issue.
5. **Reference, not embed.** The item's price is a reference to a price version plus its own fact; a settling transaction references the invoice and does not copy it.
6. **Sender is not requester.** The account's `Field_RequestID` chain; here the issuer (declarer) and the claimant differ (S4).
7. **The exchange default agrees.** Product defaults to one node per organization with a mapping ([question 4](../product/product.research.001.md#open-questions)); the account research to each ledger authoritative for its own accounts, linked by settlement ([question 13](../account/account.research.001.md#open-questions)); task to creation inside the creator's organization. Smaller choice 3 (iii) is consistent with all three.
8. **Roles belong to the other domain.** The user research ([X2](../../identity/user/user.research.001.md)) puts the eleven invoice roles in the invoice domain, not the user's; this research agrees and adds that nine of them are capabilities.
9. **Tax is a product.** Product S4 and default for question 13: a compulsory purchase is a rule on issue; here the tax line is an item of an authority-declared product, and S4's payslip and property tax are claims issued by rules.
10. **The invoice research starts from the account research's three facts about the invoice:** the invoice has no account link and should not; the payment's unit must equal the invoice's currency; the exchange question is the same shape as account question 13 ([account research, reconciliation](../account/account.research.001.md#reconciliation-with-the-four-sibling-researches)). Confirmed, with S11 qualifying the second.

**Contradictions and tensions across the researches.**
1. **Zero lines versus the product's necessity.** [Product Research 001](../product/product.research.001.md#2-minimal-kernel-and-what-must-be-pluggable) argues the product is core because "invoice items must refer to something" and notes that invoice.md asks whether an invoice may have zero products; this research says yes (S8), which weakens that argument further. Not a contradiction in text but a shared dependency: product question 2 and invoice question 4 move together.
2. **Never erased versus erased.** The same tension the account research reports for the ledger: an issued invoice is a fiscal fact and names persons. The answer proposed there (detach the identity link, keep the effect) is adopted as the default here (question 15).
3. **Who owns price-settlement.** The pos edge `price-settlement`, batch and product each hold a copy ([synthesis](../../../temp/sessions/20261014T071207Z-28148-0/concept-synthesis.md#contradictions-the-researches-found-that-outlive-any-one-domain)); the adjustment sketch here touches it and does not settle it.
4. **Correction by supersedes or by a new relation.** Thing's `supersedes` says the earlier record stays in the graph and a replaced record is replaced ([supersedes](../../identity/thing/edges/supersedes/supersedes.md)); content keeps one identity with edits as events; task supersedes on reopen. A credit note offsets rather than replaces, so the invoice would need its own relation unless thing's is widened. Not resolved.
5. **Draft identity.** Content's work-level identity with immutable revisions (synthesis agreement 1) versus a mutable draft that is not a fact: the invoice proposes the draft is not an acquired fact until issued. The same pattern would apply to an unpublished content draft; the researches do not say.
6. **The statuses ruling R4** blocks product, task, content, account, and this domain alike.
7. **Does a negotiation produce an invoice or change a draft.** Task research makes negotiation a task kind whose accepted result changes "the price fact it concerns" and is "blocked on the invoice-exchange question" ([task research](../../management/task/task.research.001.md)); the draft/answer here is where that result lands.

**On transaction (read, not edited).** The optional source, the duplicate same-unit rule and the reference edge's mandatory-or-convention status ([transaction.handoff.md](../transaction/transaction.handoff.md#open-questions), items 2 and 3) all bear on this domain: question 12 and contradiction 8. A transaction research is best read with this one.

## Recommendation (unratified)
The owner has not reviewed this, and nothing in it is decided.

1. **Say what the invoice is for (Tentative, medium confidence).** The invoice owns the memory of an agreed claim: drafted freely, a fact when issued, answered by the other party, then only settled, corrected or withdrawn by further facts. This changes the first line and the opening of [invoice.md](invoice.md) and nothing else visible.
2. **Keep a seven-element kernel (Tentative):** identity, the two party relations, the line with the price as issued, lifecycle events (issued, answered, voided), `corrects`, an event target, and the `condition_is` attachment. Everything else is a capability, a rule or an existing domain.
3. **Choose B over A, and keep C open until a rights/obligation domain is decided (Tentative).**
4. **Store no payment status (Tentative).** `paid` and `paid-partially` are discovered from referencing transactions; `voided` stays; `expired` is a rule's event.
5. **Correct by a new invoice, void only the never-effective (Tentative).**
6. **Reduce the roles to two kernel relations and group the other nine into capabilities that each state creator, remover and trigger (Tentative);** the Decided distinction of customer, buyer and consumer is not touched.
7. **Make an invoice between organizations one authoritative invoice at the issuer, with an answer event and the counterparty's own booking (Explored).**
8. **Do not move, delete or convert anything on this evidence.** `data_model.kh` stays unconverted; `InvoiceModel` stays unwritten ([Khayyam rule 6](../../../temp/Khayyam.practice.md#governing-rules)); any `.kh` import path in this repository carries no `org/` prefix, only `memar/` is a prefix, which a future conversion must follow.
9. **Ask the questions that change what the work is first:** question 1 (what the domain is responsible for), question 2 (who issues, and whether issue is a fact separate from the claim), question 3 (the draft/issue boundary).

## Open Questions
This is the research's eighth section. Only the owner can decide these. Ordered by what they change: those that change what the domain is first, then those that change how a part is done ([Ask rather than assume](../../../docs/cognition.md#discourse-norms-derived-from-this-model)). Each carries a recommended default and what it blocks. They are also entered in the [handoff](invoice.handoff.md#open-questions).

1. **Is the invoice a domain whose responsibility is the agreed claim (draft, issue, answer, settle, correct), or a document form of a more basic claim/obligation, a classification with the invoice as a pluggable?** Default: a domain. Blocks: the rewrite of the first lines of [invoice.md](invoice.md), model B versus C, `InvoiceModel` beyond `ThingModel` (Khayyam rule 6), the "ChangeOwner" sentence, any rights/obligation domain.
2. **Who issues, and is issuing a fact separate from being the claimant: may a rule, the party claimed against (self-billing) or an authority issue?** Default: yes; the issue event carries a declarer distinct from the claimant. Blocks: payslip, tax and fine cases, `user-seller` and `user-orderer` policies, the authorization of issue.
3. **Is a draft a phase before issue in which lines and adjustments may change, with issue the acquired fact that freezes the invoice, and is the issued invoice the same identity as its draft?** Default: yes to both; the draft is not an acquired fact. Blocks: VAT adding a line, `DiscountedPrice` assignment, kitchen and POS flows, the exchange draft, the status events, contradiction 5.
4. **May an invoice have no lines (a pure claim)?** Default: yes. Blocks: invoice.md's unresolved question, product question 2's dependency, fines and notebook credit, the kernel's line element being optional.
5. **Does the line keep the four-price chain, or an agreed price plus adjustments each with a cause, whose name the owner picks?** Default: agreed price plus signed adjustments; neutral name (`adjustment`); the aggregation `RulePrice`/`PriceAdjustment` question stays the owner's. Blocks: `data_model.kh` conversion, discount and voucher, the handoff naming question, contradiction 2.
6. **How is an issued invoice corrected: always a corrective invoice pointing at the original, with void only for the never-effective, and does the pointing relation live in thing's `supersedes` or in the invoice?** Default: corrective invoice; the relation `corrects` in the invoice domain. Blocks: voided and paid documents, refund, transaction invariant 6's reading, test 9.
7. **Are `paid`, `paid-partially` stored statuses or discovered from referencing transactions?** Default: discovered; `voided` acquired; `expired` a rule's event. Blocks: the status folders, analytics, the partial-payment open question, contradiction 7.
8. **For invoices between organizations: one authoritative invoice at the issuer with the counterparty's received reference, answer and own booking, or two counterpart invoices, or one shared invoice? And what does an answer carry (per line, price version, reason), and what are the timeout and offline rules?** Default: one authoritative invoice at the issuer; a per-line answer with the seller's current price version; a timeout set by the receiving organization's rule; an offline organization holds the invoice as sent. Blocks: the exchange handoff question and its seven sub-questions, product question 4, task question 16, account question 13, test 17 and 18.
9. **May an invoice cause other invoices (commission, tax, royalty), and is that a relation of the invoice kernel or of the capability that produces them?** Default: of the capability; the kernel only records the cause as `transaction_reference_is`-style reference. Blocks: intermediary, tax, payslip compositions, S7.
10. **Where does a schedule of dated, possibly indexed amounts live: the invoice conditional, credit, settlement, or a payment-schedule capability?** Default: a payment-schedule capability producing deferred transactions. Blocks: [price-index](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales), credit, settlement, the pre-order instalment question, test 19.
11. **Are the nine roles beyond seller and buyer capabilities (payer, fulfilment, intermediary, origin), each stating creator, remover and trigger, and does the actual payer come from settling transactions?** Default: yes. Blocks: the eleven edge documents, contradictions 4, 9 and 10, S1, S7, S9.
12. **Who refuses a settlement whose unit differs from the invoice's: the transaction's rule, the invoice, or the exchange pair?** Default: the transaction at registration; the invoice states its unit only. Blocks: S11, the duplicate same-unit rule (compare [account question 15](../account/account.research.001.md#open-questions)), test 20.
13. **Do numbering and clearance (an authority's answer) exist as capabilities that may make issue wait?** Default: yes, as optional capabilities listening on the event target. Blocks: e-invoicing jurisdictions, S2, tests 12 and 13.
14. **Is progress billing against a contract (cumulative statements, retention, certification) a capability of the invoice domain or of contract?** Default: a contract-billing capability; the invoice stays unaware. Blocks: S10, test 21.
15. **May the party links of an issued invoice be detached on erasure, leaving the claim and its settlement?** Default: yes, by an authority-gated event; the invoice is never erased. Blocks: retention policy, convergence with content question 7, text question 15 and account question 14, test 25.
16. **Does the invoice keep a name other than "ChangeOwner of products" for its purpose, and does "buyer" mean the party claimed against rather than a purchasing employee?** Default: the claim reading in both. Blocks: the first line of invoice.md, the `user-buyer` policy, contradictions 1 and 4.
17. **Are the retail statuses (UserCheckout, PendingReview, Packaging, Shipping, Done) and the legacy numbered list a pluggable retail specialization?** Default: yes. Blocks: [status.md](status/status.md), model D, reconciliation with the shared status domain.
18. **Does an issued but unpaid invoice expire by a price-validity window (per invoice or per line), set by whom?** Default: a rule's event, per line, window set by the issuer's rule. Blocks: [expired](status/expired/expired.md), the pre-order question, discount validity.

## Related Artifacts
- [invoice.md](invoice.md) — the first lines and the Unresolved questions change if question 1 is accepted; the Model is still absent (Review; not edited)
- [invoice.handoff.md](invoice.handoff.md) — gains questions 1 to 18 and Next Steps (Update, done in this session)
- [invoice.changelog.md](invoice.changelog.md) — created with an entry for this research (Create, done)
- [edges/item/item.md](edges/item/item.md), [status/status.md](status/status.md) — questions 3, 5, 7 (Review)
- [Account Research 001](../account/account.research.001.md), [Product Research 001](../product/product.research.001.md), [Task Research 001](../../management/task/task.research.001.md), [Content Research 001](../../knowledge/content/content.research.001.md), [Text Research 001](../../knowledge/text/text.research.001.md), [Group Research 001](../../management/group/group.research.001.md), [Thing Research 001](../../identity/thing/thing.research.001.md), [User Research 001](../../identity/user/user.research.001.md) — the sibling researches reconciled above (Related)
- [transaction.md](../transaction/transaction.md), [transaction.handoff.md](../transaction/transaction.handoff.md) — the other half; questions 8, 12 (Review; not edited)
- [discount](../../../modules-plugable/economics/discount/discount.md), [voucher](../../../modules-plugable/economics/voucher/voucher.md), [refund](../../../modules-plugable/economics/refund/refund.md), [pricing](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md), [price-index](../../../modules-plugable/economics/price-index/price-index.md), [pos](../../../modules-plugable/economics/pos/pos.md), [payroll](../../../modules-plugable/economics/payroll/payroll.md) — the capabilities the mapping reclassifies or keeps (Review)
- [contract](../../rights/contract/contract.md), [ownership](../../rights/ownership/ownership.md) — question 1 (Review)
