# Invoice Handoff

## Topic & Purpose
Load-bearing commercial decisions that attach to Invoice: adjustment/aggregation field naming, party-role distinctions (customer / buyer / consumer), and core-vs-optional placement relative to organizational purpose.

## Status
Active — party-role and core-vs-optional decided; invoice adjustment field naming still open.

## Decisions

### From Organization ideas backlog

- **Invoice should not carry a `discount` field.** Omid's proposal: an aggregation method (`RulePrice() → money_p.Amount`) summing all rules that applied (vouchers + discounts + gift + auctions); counter-argument recorded: naming the field after its cause (`RulePrice`) imports causality into the model and breaks when an adjustment comes from something that is not a rule (cost allocation, carbon tax, currency adjustment) — alternatives `PriceAdjustment` / `AdjustmentAmount` left Pricing to reveal composition. *(naming — open for the org)*
- **Customer ≠ buyer ≠ consumer.** A restaurant order may be placed by one person and consumed by two; the model connects through *User* with distinct identity edges per role. Care applies even in examples — dozens of "financial account" kinds differ only in unit, not in the nature of the account concept. *(decided)*
- **Core vs. optional is relative to purpose.** Discount without which the organization still buys and sells; Product/Invoice/Account without which an ERP is unrepresentable — but the attribute is not intrinsic to the module (a charity or a government has "sales" too). *(decided)*

## Open Questions
- Field naming for the invoice adjustment aggregation (`RulePrice` vs. `PriceAdjustment`) and the quantity-bookkeeping concept's final name. *(from consolidated open-questions backlog #10 — invoice half)*
- **Invoice exchange between organizations — a purchase request.** The owner's statement (2026-10-10, translated): a new purchase means a new invoice, and it must be inserted automatically in every organization the invoice involves. An invoice registered in the buyer's or the seller's organization needs a way to reach the other involved organizations; traditional organizations know this as a purchase request. Once this is built, the product is registered in both organizations, with the same identifier or a different one — the owner has not decided which. The price is settled at the same moment. An invoice cannot be registered in the buyer's organization at the previous price: as soon as the send-invoice service calls the seller's organization, a process error arises, because the seller declares, by hand or by rule, that it does not accept the sale invoice — for example for a price difference.
  - *What invoice already has:* the parties as [user-seller](edges/user-seller/user-seller.md) and [user-buyer](edges/user-buyer/user-buyer.md), but no statement of which organization each party's invoice is registered in; [pre-order](edges-shortcut/pre-order/pre-order.md), an invoice issued before its product exists; and the states under [status/](status/status.md) (paid, paid-partially, voided, expired), none of which is "sent, awaiting the other organization" or "rejected by the other organization". Whether a rejection is a status, a rule outcome, or a process error the sender receives is open.
  - *The question to state, not decide:* is it one invoice that both organizations see, or two invoices, one in each? Memar's [One Authoritative Location per Concern's Data](../../../docs/modeling.md#one-authoritative-location-per-concerns-data) is scoped to one model: another organization's model is authoritative at its own level and is a counterpart, not a derived copy. Two invoices are therefore allowed only as counterparts, each authoritative in its own organization, and then it is open which one holds the agreed price when they disagree. One shared invoice instead needs one place both organizations read.
  - *Same or different product identifier:* a different identifier is what [replacement cost](../../../modules-plugable/economics/replacement-cost/replacement-cost.md) already assumes, where the buyer's product points at the seller's through [source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md).
  - *Replacement cost:* the purchase is an event the buyer's [replacement cost](../../../modules-plugable/economics/replacement-cost/replacement-cost.md) reacts to. The price agreed on the exchanged invoice is the seller's current price, so the purchase re-evaluates the buyer's replacement cost and needs no separate quote.
  - *Follow or request:* delivering an invoice to the organizations it involves is a request to a party, not a [follow](../../identity/thing/edges/follow/follow.md) — the receiving organization did not ask for it, and it answers by accepting or rejecting — but it needs the same AAA: the sender authenticated, the receiver's rule deciding which senders' invoices it accepts, each delivery metered. Is it carried by the same mechanism as a follow's delivery?
  - *Product identity mapping:* if the two organizations' product identifiers differ, which of them records the mapping — the buyer's [source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md) edge, or the invoice item — and is it created by the first exchanged invoice?
  - *Rejection protocol:* what does a rejection carry — the items refused, the seller's current price version for each, a reason — and may the sender re-issue at that price in one step, as a new invoice referencing the rejected one?
  - *Partial acceptance:* may the receiving organization accept some items and reject others, or is an exchanged invoice accepted or rejected whole?
  - *Timeouts:* how long does a sent invoice wait for an answer, who sets that time, and what fact is recorded when it passes?
  - *Offline organizations:* when the other organization is unreachable, or not on the platform at all, is the invoice held as sent and awaiting an answer, and how does an organization outside the platform answer?
  - *Booking before acceptance:* may the buyer's organization book a purchase before the seller accepts it? No: the price is agreed at issue and the seller may reject a mismatch, so until it accepts there is no agreed price to book; the buyer holds a sent invoice awaiting an answer. (answered 2026-10-10, unratified)
  - *Why it matters, and the path:* it decides whether any invoice between two organizations in the graph can be registered on one side alone. It blocks nothing in the current data-model work. Suggested path: a dedicated session that settles one-versus-two invoices first, then the rejection's shape, then the product identifier. Prior thinking on an invoice held by the buyer's governance organization is in [device ownership and authority transfer](../../computer/device/edges/device-ownership-and-authority-transfer.md). *(owner, 2026-10-10 — open)*

### From Invoice Research 001 (2026-10-18, agent proposals, nothing ratified)
Each entry: the question, the recommended default, what it blocks. Ordered by what they change: those that change what the domain is first. Reasoning, eleven scenarios and five rival models are in [Invoice Research 001](invoice.research.001.md#open-questions).
1. **Is the invoice a domain whose responsibility is the agreed claim (draft, issue, answer, settle, correct), or a document form of a more basic claim/obligation?** Default: a domain. Blocks: the first lines of [invoice.md](invoice.md), model B versus C, `InvoiceModel` beyond `ThingModel` (Khayyam rule 6), the "ChangeOwner" sentence.
2. **Who issues, and is issuing a fact separate from being the claimant (a rule, the party claimed against, an authority)?** Default: yes; the issue event has its own declarer. Blocks: payslip, tax and fine cases, the seller and orderer policies.
3. **Is a draft a phase before issue where lines and adjustments change, with issue the acquired fact that freezes the invoice, and is the issued invoice the same identity as its draft?** Default: yes to both. Blocks: VAT adding a line, `DiscountedPrice` assignment, POS and kitchen flows, the exchange draft.
4. **May an invoice have no lines (a pure claim)?** Default: yes. Blocks: the unresolved question in invoice.md, product question 2's dependency, fines and notebook credit.
5. **Four-price chain or an agreed price plus signed adjustments each with a cause (the name stays the owner's)?** Default: agreed price plus adjustments. Blocks: `data_model.kh` conversion, discount and voucher, the naming question above.
6. **How is an issued invoice corrected: always a corrective invoice pointing at the original, void only for the never-effective; the relation in thing's `supersedes` or in the invoice?** Default: corrective invoice, relation `corrects` in the invoice. Blocks: voided and paid documents, refund.
7. **Are `paid` and `paid-partially` stored statuses or discovered from referencing transactions?** Default: discovered; `voided` acquired; `expired` a rule's event. Blocks: the status folders, the partial-payment question.
8. **Between organizations: one authoritative invoice at the issuer with the counterparty's received reference, answer and own booking, or two counterparts, or one shared? What does an answer carry, and what are timeout and offline rules?** Default: one authoritative invoice at the issuer; per-line answer with the seller's current price version; timeout by the receiver's rule. Blocks: the exchange question above and its sub-questions, product question 4, task question 16, account question 13.
9. **May an invoice cause other invoices (commission, tax, royalty): a kernel relation or the producing capability's?** Default: the capability's. Blocks: intermediary, tax and payslip compositions.
10. **Where does a schedule of dated, possibly indexed amounts live?** Default: a payment-schedule capability producing deferred transactions. Blocks: price-index deferred payment, credit, settlement, pre-order instalments.
11. **Are the nine roles beyond seller and buyer capabilities (payer, fulfilment, intermediary, origin), each stating creator, remover and trigger?** Default: yes; the Decided customer/buyer/consumer distinction is untouched. Blocks: the eleven user-* documents.
12. **Who refuses a settlement whose unit differs from the invoice's?** Default: the transaction at registration. Blocks: cross-border sales, the duplicate same-unit rule.
13. **Do numbering and clearance (an authority's answer) exist as optional capabilities that may make issue wait?** Default: yes. Blocks: e-invoicing jurisdictions.
14. **Is progress billing against a contract a capability of contract rather than invoice?** Default: yes. Blocks: retention and certification cases.
15. **May the party links of an issued invoice be detached on erasure, leaving the claim and its settlement?** Default: yes, by an authority-gated event. Blocks: retention policy, convergence with content, text and account erasure questions.
16. **Is the invoice's purpose the claim (not "ChangeOwner of products"), and does "buyer" mean the party claimed against rather than a purchasing employee?** Default: yes. Blocks: the first line of invoice.md, the user-buyer policy.
17. **Are the retail statuses (UserCheckout ... Done) and the legacy numbered list a pluggable retail specialization?** Default: yes. Blocks: [status.md](status/status.md), reconciliation with the shared status domain.
18. **Does an issued but unpaid invoice expire by a price-validity window, per line, set by the issuer's rule?** Default: yes. Blocks: [expired](status/expired/expired.md), the pre-order question.

### Contradictions between this domain's documents and its neighbours (reported by Invoice Research 001, not resolved)
See [Contradictions found](invoice.research.001.md#contradictions-found): the purpose line "ChangeOwner" against the claim definition and holding-is-not-title; the item `DiscountedPrice` against "no discount field"; the item as an edge and as a record with its own identity; "buyer" as a purchasing employee against the organization-buyer; VAT adding a line to an issued invoice; void against compensating records; paid as status and as computation; `pay_by` against the transaction reference edge and pos-issuer; direction and naming of the role edges; the pre-order walk over undefined edges; kernel documents naming pluggables; the claim's unit against the settling transaction's.

## Proposed Next Steps
1. After the owner answers Invoice Research 001 questions 1 to 3 (the domain's responsibility, who issues, the draft/issue boundary): write the opening and a `## Model` section of [invoice.md](invoice.md), and decide between the claim-kernel model and the claim-as-concept model.
2. Decide questions 5 and 7 before the `item` data model is converted; keep `data_model.kh` unconverted until then.
3. Give each of the eleven `user-*` documents its creator, remover and trigger, or fold them into the capabilities of question 11.
4. Settle the exchange (question 8) in one session together with product question 4, task question 16 and account question 13, then the rejection's shape and the product identifier.
5. Sketch the missing pieces ([finding 6](invoice.research.001.md#6-missing-edges-and-modules)) one at a time, checking `adjustment` against discount and voucher, `payment-schedule` against credit and settlement, `clearance` against contract-billing.
6. Name the source edges of the `pre-order` shortcut and reconcile `pay_by` with the transaction reference edge.
7. Turn the test scenarios ([finding 7](invoice.research.001.md#7-test-scenarios)) into tests once questions 1 to 8 are answered; those marked "kept" can be written now.
8. Start a transaction research from the shared contradictions (optional source, same-unit rule, reference edge status); read it with this one and the account research.

## Related Artifacts
- [`invoice.research.001.md`](invoice.research.001.md) — what the domain is for, kernel and pluggable, rival models, folder mapping, missing modules, 25 test scenarios, 18 owner questions (Review; unratified)
- [`invoice.changelog.md`](invoice.changelog.md) — entry for the research (Update, done)

- [`README.md`](README.md)
- [`../product/product.handoff.md`](../product/product.handoff.md)
- [`../../../modules-plugable/economics/pricing/edges/pricing/README.md`](../../../modules-plugable/economics/pricing/edges/pricing/README.md)
- Invoice party edges: [`edges/user-customer`](edges/user-customer/README.md), [`edges/user-buyer`](edges/user-buyer/README.md), [`edges/user-consumer`](edges/user-consumer/README.md)

## Notes
- Provenance: Organization ideas backlog → Commercial / organizational concepts (2026-09-16 migration).
- **Enterprise-software foundations are stable.** The bases of organizational systems have not changed in ~200 years when modeled correctly; the churn ("requirements") is evidence of a bad model, not of a changing business — DDD attempted this correction but propagated wrong readings (its examples blurred the concepts). *(Omid's working thesis)*

## Khayyam conversion (2026-10-03)

Converted: `protocol/dt-uuid.kh` (`Field_InvoiceID` → `InvoiceID`, valued as `ThingUUID` imported from `identity/thing`), `edges/item/protocol/dt-uuid.kh` (`Field_InvoiceItemID` → `InvoiceItemID`, same value type), and `edges/item/protocol/gui-widget.kh`. All three return `accept` from the Khayyam frontend.

Decisions:

- **No local `InvoiceUUID` abstraction** for the Go's `type UUID thing_p.UUID`; `ThingUUID` is imported, matching the rule/module/taxon/estate/ownership conversions and rule 6.
- **`gui-widget.kh`'s two interfaces were qualified, not left bare.** Eight modules in the tree declare `GUI_Widget_Conditions` / `GUI_Widget_Service`, so the plain name would collide on import; they are declared `Invoice_ItemGUIWidget_Conditions` and `Invoice_ItemGUIWidget_Service`, following the shape `knowledge/question/widgets/question/gui.kh` already uses (`Question_GUI_Widget`). This is the first of that family to be converted — the other seven still carry the bare Go spelling in their clue blocks and will need the same treatment when their domains are converted, or a shared `GUI_Widget_Conditions` abstraction will have to be recognised as one concept declared many times.

### Unconverted, and what blocks it

- **`edges/item/protocol/data_model.kh` — blocked on the money module.** Four of its fields return `money_p.Amount`: `SuggestedPrice`, `DiscountedPrice`, `RulePrice`, `PayablePrice`. No `.kh` in the tree declares an `Amount`, and the path the Go names — `modules/economics/money/protocol` — does not exist; the module is at `modules-plugable/economics/money/`, whose `dt-money-amout.kh` is itself unconverted and whose own document lists "`int64` scaling vs `decimal_p.Quantity` used on bookkeeping fields — reconcile the two quantity representations" as unresolved. Declaring a local amount type here would give two owners of one concept. Until money declares an amount, this file cannot be written without either dropping four fields or inventing a type.
- **`edges/item/protocol/storage.kh` — blocked transitively.** Its signatures are `Get(invoiceID, productID)` and the two `FIND_*_BY_*` queries, none of which need money, but it names `DataModel`, which is the file above. Converting it first would produce a file importing a name its target does not declare.
- **`_import/invoice/**`, `_import/invoice-voucher/storage.sql`** — legacy service/storage code (Syllab/JSON codecs, `ds.DataStructure`), same disposition as product's `_import`: delete or re-model, not convert.

### Open from this pass

- **`invoice.md` has no `## Model` section.** Every other economics domain states its record fields and edge set; invoice states a purpose ("ChangeOwner of products"), a definition, and discussion. So the invoice record's own fields — as opposed to the `item` edge's — have no statement anywhere in the domain, and nothing in this pass could be derived from the document rather than from the Go. This is worth closing before invoice reaches the data-model pass: which fields the invoice record itself carries (total, currency, issue date, parties) is exactly what `item`'s aggregation and the `status/` folders assume.
- **`RulePrice` naming is still open** and this pass could not settle it — the Go already carries `RulePrice()`, and the Decisions section above keeps it open between `RulePrice` and `PriceAdjustment`. The converted `item` files do not touch it (the field lives in the blocked `data_model.kh`), so nothing is frozen either way.
