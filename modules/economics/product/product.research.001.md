# Product Research 001 — What the product domain is for, and what is kernel and what is pluggable

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
- [Recommendation (unratified)](#recommendation-unratified)
- [Open Questions](#open-questions)
- [Related Artifacts](#related-artifacts)

## Status
Active

Nothing here is ratified. Every proposal carries a confidence mark in the sense of [Handoff Practice](../../knowledge/documentation/handoff/handoff.practice.md): Decided, Tentative, Explored (explored but unresolved), or Deferred. **No item below is Decided by this research.** Items already Decided in the domain documents are cited as such and are not re-argued.

## Question and Goals
- **Questions:**
  - What is the product domain for, once it is tested against cases that do not look like a shop? — Answered as finding 1 (proposal, Tentative).
  - Which part of it is kernel, and which part must be pluggable, under the placement tests of [Modules → Placement](../../modules.md#placement)? — Answered as finding 2 (proposal, Tentative).
  - Which of the rival models survives the cases and Memar's modeling criteria? — Answered as finding 3; the choice is the owner's.
  - What must the domain own, and which of that is still unsettled? — Asked as requirements questions in finding 4.
- **Goals:**
  - Move the domain forward by modeling, not by housekeeping: a sharper reading of what a product is, a kernel small enough to defend, a placement for every existing edge folder, and the missing pieces named. — Met as proposal
  - Leave the owner a short list of decisions, each with a recommended default and the work it blocks. — Met
- **Scope:** the `modules/economics/product` domain and the edge folders under it. Out of scope: the data-model pass for any edge, any `.kh` file, moving or deleting any folder, and re-arguing what the domain documents already mark Decided or confirmed.

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — Questioner, Goal-setter, Reviewer (Not yet reviewed). He asked for this work on 2026-10-15 and was unavailable for questions while it ran.
- An AI agent (Claude, model `claude-sonnet-5-5` as reported by the runtime; [CONTRIBUTORS.md](../../../CONTRIBUTORS.md) has no entry for it) — Researcher, task `20261016-T001246Z-16012`.

## Starting Evidence
The domain's own documents are the starting evidence, read in full: [product.md](product.md), [product.handoff.md](product.handoff.md), [product.changelog.md](product.changelog.md), and the fifteen edge documents under [edges/](edges/README.md). The questions that move this research are the ones those documents already hold open:

- "Are `price`/`pricing` kernel edges of product or rule-driven capabilities?" and "Does a price belong to the product or to the batch?" ([product.md → Unresolved questions](product.md#unresolved-questions)).
- "Capability test vs asset-management reading": if pricing is the core test, what carries the half of the domain that is never priced? ([product.md](product.md#unresolved-questions); handoff Next Step 3).
- "Is the product-to-product relation a single parent/child edge, or do several relations hide here?" ([product.md → Product relation to product](product.md#product-relation-to-product)).
- The owner's eight questions on price ownership ([Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions)).

The survey of 2026-10-14 is a claim, read at the passages cited: [master plan](../../../.agents/tasks/20261014T071207Z-28148-0/plan-master.md), the [mgmt-econ-rights-storage report](../../../.agents/tasks/20261014T071357Z-29392-0/report.md) (defects D5, D7, D10, D11), and the [owner-question catalogue](../../../.agents/tasks/20261014T071404Z-26308-0/report.md) (D1, E4, B4).

## Methodology
One reasoning pass by one agent. No second cognitive system was consulted and no organization was asked. The scenarios are reasoning from general knowledge of practice in several countries and industries, not retrieval and not observation; a figure or a custom named in a scenario is illustrative and nothing in the findings rests on its exact value.

1. **Reading.** Read in this chat: the Memar sources named below; [modules.md](../../modules.md); [Khayyam practice](../../../temp/Khayyam.practice.md) (only to know what this chat must not write); the domain's documents and all fifteen edge documents; [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md) in full; and, for the neighbours a product touches, [invoice](../invoice/invoice.md), [item](../invoice/edges/item/item.md), [invoice handoff open questions](../invoice/invoice.handoff.md#open-questions), [account](../account/account.md), [economics](../economics.md), [thing](../../identity/thing/thing.md) with its [supersedes](../../identity/thing/edges/supersedes/supersedes.md), [template](../../identity/thing/edges/template/template.md), [count_unit](../../identity/thing/edges/count_unit/count_unit.md), and [follow](../../identity/thing/edges/follow/follow.md) edges, [estate handoff](../../identity/estate/estate.handoff.md), and in `modules-plugable/economics` [batch](../../../modules-plugable/economics/batch/batch.md) with its accounting, exist, and price-settlement edges, [good](../../../modules-plugable/economics/good/good.md) with best_before and reserve-quantity, [service](../../../modules-plugable/economics/service/service.md) with number, [brand](../../../modules-plugable/economics/brand/edges/brand/brand.md), [packages](../../../modules-plugable/economics/discount/packages/packages.md), [pricing](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md), [replacement-cost source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md), [restriction](../../../modules-plugable/economics/restriction/restriction.md), [refund](../../../modules-plugable/economics/refund/refund.md), and [product-label](../../../modules-plugable/economics/product/labels/labels.md).
   **Not read, so any statement about them is unverified:** the `.md` of timing-interval, multiple-use, item-seat, seat, service/estate, item-ingredient, good/material, vat/edges/product, the batch cost edge, the three product-label loops, the discount module beyond packages, the price-index component edge, and the `.kh` files except the three small ones named in finding 5.
2. **Memar's criteria,** read from the sources and used as written:
   - [Modularity → Core Structure and Optional Modules](../../knowledge/modularity/modularity.md#core-structure-and-optional-modules), [What Earns Foundational Status](../../knowledge/modularity/modularity.md#what-earns-foundational-status), [Pluggable Behavior](../../knowledge/modularity/modularity.md#pluggable-behavior), [Capability Completeness](../../knowledge/modularity/modularity.md#capability-completeness), [Foundational Concepts Should Remain Few](../../knowledge/modularity/modularity.md#foundational-concepts-should-remain-few).
   - [Modeling → Concept Existence vs. Model Existence](../../../docs/modeling.md#concept-existence-vs-model-existence), [Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels), [False Taxonomies](../../../docs/modeling.md#false-taxonomies-hide-shared-structure), [Acquired vs. Discovered Data](../../../docs/modeling.md#acquired-data-vs-discovered-data), [State Change as Events](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates), [Constraints Belong to the Constraining Concern](../../../docs/modeling.md#constraints-belong-to-the-constraining-concern), [One Authoritative Location](../../../docs/modeling.md#one-authoritative-location-per-concerns-data), [A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once), [Separating Structure from Policy](../../../docs/modeling.md#separating-structure-code-from-policy-rule).
   - [Modeling Practice → The Modeling Workflow](../../../docs/modeling.practice.md#the-modeling-workflow), [Premature Classification Check](../../../docs/modeling.practice.md#premature-classification-check), [Relationship Audit](../../../docs/modeling.practice.md#relationship-audit), [Placing a relation](../../../docs/modeling.practice.md#placing-a-relation).
3. **Terms, defined before use.** A word below with no Memar definition carries its ordinary meaning ([Terminology → The Default Meaning of an Unreferenced Term](../../../docs/terminology.md#the-default-meaning-of-an-unreferenced-term)).

| Term | Meaning used here | Governing source |
|---|---|---|
| **Product** | In this repository: "anything that can be priced", the unit of priceability, with the marketing sense (an object, system, or service made available for consumer use) as its prior art. Memar's terminology does not define "product", so outside that domain document the ordinary meaning applies. This research asks whether "priceable" is the right test (finding 1). | [product.md → Definition in Memar](product.md#definition-in-memar) and [Prior art](product.md#prior-art) |
| **Kernel / core** | A concept whose removal would force a foundational type to be fabricated or distorted. Not importance, not prevalence. | [Modules → Placement](../../modules.md#placement); [Modularity → What Earns Foundational Status](../../knowledge/modularity/modularity.md#what-earns-foundational-status) |
| **Pluggable** | An optional capability attached through an explicit relationship, owning that relationship and its processing together, installable and removable as a whole. Not a dynamically loaded plugin. | [Modules → Placement](../../modules.md#placement); [Modularity → Pluggable Behavior](../../knowledge/modularity/modularity.md#pluggable-behavior) |
| **Capability** | A relationship with independent domain meaning plus the rules governing when it may exist and the processing that realizes its effects. | [Modularity → Capability Completeness](../../knowledge/modularity/modularity.md#capability-completeness) |
| **Edge, loop-edge, shortcut** | `edges/`: two distinct nodes, an acquired relation. `edges-loop/`: a classification of one node on itself. `edges-shortcut/`: a derived cache of a walk already in the graph. | [Modules → Edge buckets](../../modules.md#edge-buckets) |
| **Acquired / discovered** | Acquired data is stated by an external source and cannot be recomputed. Discovered data is derived from acquired data. | [Modeling → Acquired Data vs. Discovered Data](../../../docs/modeling.md#acquired-data-vs-discovered-data) |
| **Thing, count unit** | A thing is a subject or object one need not or cannot name specifically; almost every thing has exactly one count unit. | [thing.md](../../identity/thing/thing.md); [count_unit](../../identity/thing/edges/count_unit/count_unit.md#policies-rules) |
| **Account** | The bookkeeping holder of one countable quantity with one count unit; it is not financial by nature. Holding is not legal title; title is `rights/ownership`. | [account.md](../account/account.md#policies-rules) |
| **Batch** | The identity of produced goods, singly or as a group; whether a realization or a grouping is open. | [batch.md](../../../modules-plugable/economics/batch/batch.md) |
| **Rule** | Policy attached to structure through the generic `condition_is` edge; the kernel does not reference the rule domain directly. | [Modules → Placement](../../modules.md#placement); [Separating Structure from Policy](../../../docs/modeling.md#separating-structure-code-from-policy-rule) |
| **Admission** (agent term) | A declaring organization's act that makes a thing available to economic acts: being named on an invoice item, held in an account, transferred, appraised. Introduced by this research; not a repository term. | agent proposal |
| **Offer** (agent term) | A seller's commitment: this item, at this price, in this unit, valid until then, for these buyers. Borrowed in shape from [schema.org Offer and UnitPriceSpecification](https://schema.org/UnitPriceSpecification) as read in [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#methodology); the repository's legacy `ProductAuction` record had the same shape ([storage.kh](_import/product-auction/storage.kh)). | agent proposal |

**Limits.** One agent, one pass, no organization consulted. Statements about what a buyer, a seller, or a state does in a scenario are the researcher's judgment. The `.kh` sources were read only where a document cites them.

## Findings

Marks: **(source)** names the document the claim is read from. **(agent)** is the researcher's own proposal or judgment.

### 1. What the domain is for

**Statement (agent, Tentative).** The product domain answers one question for the rest of economics: *what exactly may an economic act refer to?* What an invoice item names, what an account counts, what a stock lot is a lot of, what an appraisal values or a transfer moves. It gives that "what" an identity that exists before any sale, survives every sale, and is the same identity for everyone who refers to it, while deciding nothing about how it is sold, priced, made, or stored. Everything that varies between organizations, such as price, eligibility, shelf life, a seat, a provider, a bundle, is a capability that attaches to this identity.

**What the documents already say (source).**
- A product is anything priceable; the invoice claims something and that something must be identifiable and priceable ([product.md](product.md#definition-in-memar)). An invoice is "a statement of what is claimable between parties" and its main purpose is to change the owner of products ([invoice.md](../invoice/invoice.md)).
- A product is not necessarily sold, not necessarily physical, may precede production, may also be content, and may be a spec with no producer ([confirmed positions](product.md#definition-in-memar)).
- "Product is anything the system sells — not goods": tax, insurance, healthcare, charity packages, API subscriptions (Decided 2026-09-16, [handoff](product.handoff.md#decisions-from-organization-ideas-backlog-2026-09-16)).

**The finding that moves the domain (agent, Tentative; owner question 1).** The word "priceable" carries two jobs that the cases pull apart.

- **J1, admission.** The product is what economic acts can refer to: billed, held, moved, valued. This is the museum piece, the organization's furniture, the design that is never produced.
- **J2, carrier of the stated price.** The product holds the seller's price.

The documents already show the strain. The confirmed position says a product may never be sold or priced ([product.md](product.md#definition-in-memar)) while the definition says it is whatever is priceable; the domain's own Unresolved question asks what carries the asset-management half if pricing is the test ([product.md](product.md#unresolved-questions)). The pricing research then shows J2 does not want to live on the product alone: the owner leans to the batch, services need a slot, quotes and exchange-traded goods have no stated price at all ([Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#what-each-scenario-says-about-the-candidates)). So "priceable" works as a proxy for the real test only while J1 and J2 happen to coincide, as they do in a shop. The proposal is to define the product by J1 and let price be one capability that a product may or may not have.

The completable classification sentence ([Modeling → Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels)) for the proposal: *a thing may be classified as a product because a declaring organization has admitted it to economic acts (an acquired fact with a time and a declarer) and it has one count unit, and therefore it may be named on an invoice item, counted by an account, be the subject of an offer, be superseded by another product, and be the parent or child of another product.* If a label cannot complete that sentence, it is not a product relation (finding 5 uses this to sort the edge folders).

**What the domain is not for (agent, with sources).**
- It is not the catalogue, the shop, the warehouse, or the price list. Those are views and capabilities over it; aggregates are consequences of modeling, not primitives ([Domain Decomposition over Aggregate-Root Modeling](../../../docs/modeling.md#domain-decomposition-over-aggregate-root-modeling)).
- It is not a kind taxonomy. Good versus service is a lens an organization draws differently ([product.md](product.md#definition-in-memar), [good](../../../modules-plugable/economics/good/good.md), [service](../../../modules-plugable/economics/service/service.md)).

#### Scenarios

Eleven cases from several countries and industries. For each: what is sold, what the obvious model says, what breaks, and what it asks of the domain. The first six are the load-bearing ones for the proposal; all eleven are used in the model comparison.

**S1. Loose goods and break-bulk (an Iranian bazaar, an Indonesian roadside warung, an Indian corner shop).**
- *Sold:* saffron weighed out by the gram from a bulk bag or sold in a sealed tin; cigarettes bought as a carton, a pack, or a single stick; rice from a sack.
- *Obvious model:* one product per sellable item, each with one count unit and one price.
- *What breaks:* the stick, the pack, and the carton are three products with three prices, but one physical stock that converts between them at fixed ratios, in one direction at a time (open a carton, never reseal it). The ratio is neither a variant (same unit, different attribute) nor a material (a made-of composition): it changes the count unit. The only place the repository holds such a ratio is a procurement edge ([replacement-cost source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md), the `Quantity` field). The legacy note on wholesale glass "bought only in batches of 100 m²" ([product-min-slice-to-buy.txt](_import/product-min-slice-to-buy.txt), Persian) is the same family: a purchase multiple.
- *Asks:* a relation between two products of the same stock that carries a quantity ratio, owned by whoever moves the stock; and a place for a minimum purchase quantity that is not on the product.

**S2. Mobile airtime top-up resold by a shop (East Africa, South Asia).**
- *Sold:* credit of another company, in an amount the buyer picks (or from a short menu), with a small reseller margin.
- *Obvious model:* a product with a stated price.
- *What breaks:* the quantity sold is itself money; the buyer chooses the amount, so there is no stated price to read before the sale, only a rule (amount paid, less commission). The product is a third party's product, resold; the reseller does not produce it, hold it, or set its face value.
- *Asks:* that a product may exist with no stated price, with the price a rule over the buyer's chosen quantity; and that the same identity can be referred to by the issuer and by the reseller (cross-organization identity, open in the [invoice exchange question](../invoice/invoice.handoff.md#open-questions)).

**S3. Prescription medicine with recall by lot (Japan, the EU, anywhere with a regulator).**
- *Sold:* a medicine a user may not add to an invoice without a valid prescription, and which a regulator can recall by manufacturing lot.
- *Obvious model:* a flag on the product (`Type_NeedPrescription`, [type-flags](edges/type-flags/type-flags.md#model)).
- *What breaks:* who may buy is a policy of the organization and the regulator, not a property of the medicine ([Constraints Belong to the Constraining Concern](../../../docs/modeling.md#constraints-belong-to-the-constraining-concern)); a recall must find every position of a lot without giving identity to each box ([batch.md](../../../modules-plugable/economics/batch/batch.md) consumer-protection case).
- *Asks:* the product stays the same identity under any number of eligibility rules, attached from outside; the lot, not the product, is the recall unit.

**S4. Compulsory charges: a municipal property tax and a traffic fine (anywhere).**
- *Sold:* nothing the payer chose. An authority assesses an amount per person by rule.
- *Obvious model:* a product an organization decides to sell.
- *What breaks:* the declaring party is an authority, not a seller; there is no offer a buyer may decline; the price is an assessment rule over the payer's facts. The repository already says mandatory charges are "forced purchases of a government-offered product" ([invoice.md](../invoice/invoice.md#prior-art)) and that tax is a product (Decided 2026-09-16), but [price.md](edges/price/price.md#policies-rules) says only "the organization that owns the product" creates its price.
- *Asks:* who may declare a product (an authority acting by a law, not only an organization); and that compulsion is a rule on issuing the invoice, not a product property.

**S5. Charity sponsorship: "support a child for a month" (decided in [handoff](product.handoff.md#decisions-from-organization-ideas-backlog-2026-09-16)).**
- *Sold:* a monthly commitment; what the payer receives is a report and a photograph, and the benefit goes to a third person.
- *Obvious model:* a service product with a price.
- *What breaks:* nothing in the product, which is the point: the payer, the consumer, and the beneficiary are three parties, and invoice already has `consumer_is` ([user-consumer](../invoice/edges/user-consumer/user-consumer.md)). The amount may be "at least X, any more is welcome".
- *Asks:* that the offer side (a floor with free top-up) not be forced into a single stated price; the product itself is plain.

**S6. An apartment sold off-plan, years before it exists (Tehran, Dubai, many cities).**
- *Sold:* a unit in a building under construction, paid in instalments over years, with a price the buyer fears will be a fraction of the real cost by the last instalment.
- *Obvious model:* a pre-order on a product ([pre-order](../invoice/edges-shortcut/pre-order/pre-order.md)).
- *What breaks:* identity precedes production by years (confirmed, [product.md](product.md#definition-in-memar)); the instance (the realized estate) does not exist at sale, so a batch-only price model fails ([Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#made-to-order-goods)); the payment terms need an index link ([deferred-payment sales](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales)); when built, the estate is the realized form of what was sold ([estate handoff](../../identity/estate/estate.handoff.md): lineage `realized_from` is Unexamined).
- *Asks:* a product with no instance for a long time; a link from the product to the thing that later realizes it, kept on `thing` rather than invented here ([Placing a relation](../../../docs/modeling.practice.md#placing-a-relation)).

**S7. A museum piece, never sold, then deaccessioned (a national museum, an organization's own furniture).**
- *Sold:* nothing, for decades. It is stored, moved between buildings, lent to another museum, insured, and once in a century sold at auction.
- *Obvious model:* it is not a product, because nothing prices it.
- *What breaks:* the confirmed position says it is a product ([product.md](product.md#definition-in-memar)); then "priceable" is false for it. Holding it is an account of one piece ([account.md](../account/account.md)); who owns it is `rights/ownership`; a loan changes custody and not title ([account.md](../account/account.md#policies-rules)). The only thing missing is the declaration that makes the piece available to those acts.
- *Asks:* admission as the defining act, with price a capability that may attach later (deaccession) without changing the identity. This is the decisive case for finding 1.

**S8. A lucky bag (Japan, the fukubukuro) and a festival gift basket (Nowruz, Eid, Christmas).**
- *Sold:* a sealed bag at a fixed price whose contents the buyer does not know, and which the seller promises are worth more than the price; the basket's contents change each year.
- *Obvious model:* a bill of materials on the product ([material](edges/material/material.md)).
- *What breaks:* the composition is a plan at best at sale time and a fact only when packed. A composition declared on the product would be wrong for every bag.
- *Asks:* the product-level composition is intent; the actual composition is a fact of the lot that was packed (acquired at production). That puts the fact on the batch/production side and leaves the product with at most a declared intent. The value promise is a rule evaluated against replacement cost ([replacement-cost](../../../modules-plugable/economics/replacement-cost/replacement-cost.md)).

**S9. Rebar by specification, and on a commodity exchange (a designer's BIM model; a steel bourse).**
- *Sold:* "rebar A3, 4400 kg/cm², 16 mm", with no brand and no producer; later, the same steel traded on an exchange where no seller states a price.
- *Obvious model:* a product per brand and mill.
- *What breaks:* the spec is a product with all product responsibilities and no seller (confirmed, [product.md](product.md#definition-in-memar)); many sellers' concrete products satisfy it; on the exchange the price is discovered by matching, so a stored product price would be a derived copy with no re-derivation path ([Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#exchange-traded-goods)).
- *Asks:* a way for a concrete product to *satisfy* a spec product (open in [brand](../../../modules-plugable/economics/brand/edges/brand/brand.md)), owned by `thing` since the same relation serves a design and the building that realizes it.

**S10. A returnable bottle with a deposit (Germany's Pfand, the Nordic systems, bottle returns elsewhere).**
- *Sold:* a drink plus a deposit refunded when the empty bottle comes back, regardless of where the drink was bought.
- *Obvious model:* two invoice lines.
- *What breaks:* the second line is coupled to the first by a future event (the return) and has a different life: it is a claim that reverses. Nothing in the product domain pairs them; [refund](../../../modules-plugable/economics/refund/refund.md) is an invoice-to-rule edge that does not name a coupled product.
- *Asks:* a coupling between two products, owned by the capability that processes the return.

**S11. Shoes in three size systems (EU 42, US 9, JP 27).**
- *Sold:* one model of shoe in a dozen sizes, each tracked and priced alone ([variant](edges/variant/variant.md)).
- *Obvious model:* parent plus one child product per size (confirmed, [product.md](product.md#product-relation-to-product)).
- *What breaks:* nothing structural; two questions surface. The three size names are labels of one child ("names are labels; identity is the UUID", [Modules → Placement](../../modules.md#placement)). And if the parent holds a price, does a child inherit it? The repository's only precedent resolves most-specific first (batch over product over POS over organization, [price-settlement](edges/price-settlement/price-settlement.md#policies-rules)), not by inheritance.
- *Asks:* a decision on whether a child inherits its parent's attachments; the answer decides whether "variant" is a structure or a shorthand.

**What the scenarios force, in one table (agent):**

| Case | Forces on the domain |
|---|---|
| S1 | A quantity-carrying relation between products that share a stock; purchase multiples live off the product |
| S2 | A product may have no stated price; the same identity may be referred to by two organizations |
| S3 | Eligibility attaches from outside; the recall unit is the lot, not the product |
| S4 | A declarer that is an authority; compulsion is on invoice issue, not on the product |
| S5 | The product stays plain while payer, consumer, and beneficiary differ |
| S6 | Identity long before any instance; a link to what later realizes it |
| S7 | Admission without price; price is a capability, not the test |
| S8 | Composition is a fact of the lot, intent of the product |
| S9 | A product with no seller; relation "satisfies"; price discovered, not stored |
| S10 | A coupling between two products owned by the capability that processes it |
| S11 | Whether a child inherits its parent's attachments |

### 2. Minimal kernel and what must be pluggable

**Tests applied (source).** [Modules → Placement](../../modules.md#placement): kernel only if removal forces a foundational type to be fabricated or distorted; pluggable if an optional capability attaches through an explicit relationship and owns edge plus processing together; an edge becomes its own module only with independent identity, lifecycle, authorization, rules, or processing; no bare edges; a difference in parameters is configuration, a difference in processing semantics may be a module; the kernel never references the rule domain directly; analytics is never kernel; a capability is filed under the domain through which it is instantiated; no `modules-plugable/<category>/<core-domain-name>/`.

#### The removal test run on the product itself (agent, Tentative)

Remove the product domain. What is forced?
- Invoice items must refer to something. They can refer to a `thing` ([thing.md](../../identity/thing/thing.md)), and a thing already carries its count unit ([count_unit](../../identity/thing/edges/count_unit/count_unit.md#policies-rules)). No new type is fabricated.
- But "this thing may be claimed on an invoice, counted in a stock, offered for sale" is then a fact with no home. It must be expressed as a marker on a thing: either the thing becomes economic by nature (distortion of a foundational type), or the marker is a classification of the thing by a declaring organization. That marker is the product.

So the product earns its place not by price (which pricing research shows can live elsewhere) but by this marker and the rules around it. Two honest weaknesses follow (both are open questions, not conclusions):
- The product's original rationale, "an invoice claims something and that something must be identifiable and priceable" and its rejection of "invoices referencing any `thing` directly with Product as a pluggable label" because "price/pricing semantics need a single home" ([product.md → Rationale](product.md#rationale-and-alternatives)), rests on J2. If price leaves the product (model B below), that rejection's reason lapses and model C (product as a classification on thing) returns as a serious rival.
- [invoice.md](../invoice/invoice.md#unresolved-questions) itself asks "Can an invoice exist with zero products (a pure claim)?" If yes, the invoice kernel does not strictly need the product, and the necessity argument weakens further.

The independent-lifecycle test ([Concept Existence vs. Model Existence](../../../docs/modeling.md#concept-existence-vs-model-existence)) decides between B and C: does admission have a lifecycle and rules of its own (declared, admitted, suspended, withdrawn, superseded; one count unit; who may declare)? The cases say yes (S4 declarer, S6 long pre-existence, S7 deaccession, finding 4). That is why the recommendation is B (Tentative); the independent-lifecycle answer is owner question 2.

#### Proposed kernel (agent, Tentative)

| Kernel element | Why kernel | Note |
|---|---|---|
| Product identity: a `thing` UUID admitted by a declaring organization | the marker above | `ProductModel` already composes `ThingModel` only ([model.kh](protocol/model.kh), [handoff](product.handoff.md#khayyam-conversion-2026-10-03)); this research is the missing "what is added" (Khayyam rule 6) |
| Admission status, as events with time and declarer | acquired fact; overwriting would discard it ([State Change as Events](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates)) | the vocabulary is a shared status, defined once with the other statuses ([Placing a relation](../../../docs/modeling.practice.md#placing-a-relation)); where statuses live is owner question R4 of the [survey](../../../.agents/tasks/20261014T071207Z-28148-0/owner-questions.md) |
| One kind link, parent to child (`variant`) | confirmed substrate; no Variant entity ([product.md](product.md#product-relation-to-product)) | the only product-to-product relation this research keeps in the kernel; the rest are capabilities (finding 3) |
| The generic `condition_is` attachment point | the kernel exposes where rules attach and never what they say ([Extensible Behavior](../../../docs/modeling.md#extensible-behavior-belongs-to-pluggable-modules)) | replaces `customable`'s direct rule edges (survey D10) |

Not product's, though a product has them: the count unit (`thing`), the legal owner (`rights/ownership`), names and descriptions (text, [Attribute-or-Edge Test](../../../docs/modeling.md#the-attribute-or-edge-test)), the stock (an `account` plus `batch`), the supersession (`thing`).

#### Pluggable: the capability each would own

"Created/removed by" and "Triggers" are read from the cited document where it states them, otherwise marked. A document that states neither is a no-bare-edges gap ([Modules → Placement](../../modules.md#placement)), reported, not filled in.

| Capability (home) | Relationship and processing it owns | Created / removed by | Triggers |
|---|---|---|---|
| **offer** (proposed, new, `modules-plugable/economics`) | A seller's stated price for an item (product, later batch or slot): amount, count unit or display basis, validity, eligible buyers, as versions | agent proposal: only the seller organization that owns the item (the rule [price.md](edges/price/price.md#policies-rules) already states); never overwritten or deleted, superseded by a new version | one delivery per follower ([follow](../../identity/thing/edges/follow/follow.md#policies-rules)); re-evaluation of dependent replacement costs; recomputation of indices holding it ([price.md](edges/price/price.md#policies-rules)) |
| **pricing** (exists) | `(rule)-[:process_pricing_for]->(product)`; evaluation on `replacement_cost_changed`, `price_index_divergence` | only the organization that owns the product ([pricing.md](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#policies-rules)) | a new price version, as above |
| **replacement-cost** `source`, `quote` (exists) | where a product is replenished from; evaluation | only the organization that owns the subject product ([source.md](../../../modules-plugable/economics/replacement-cost/edges/source/source.md#policies-rules)) | re-evaluation of the subject's replacement cost |
| **good** (exists): best_before, reserve-quantity, material, item-ingredient | inventory-facing semantics of physical goods | best_before and reserve-quantity record no creator or trigger ([best_before](../../../modules-plugable/economics/good/edges/best_before/best_before.md), [reserve-quantity](../../../modules-plugable/economics/good/edges/reserve-quantity/reserve-quantity.md#policies-rules)): gap; material and item-ingredient not read | not recorded |
| **service** (exists): number, timing-interval, multiple-use, item-seat, estate, seat, provider | capacity, duration, use caps, seats, location, operator of a service | `number` records none ([number](../../../modules-plugable/economics/service/edges/number/number.md)): gap; others not read | not recorded |
| **batch** (exists): exist, cost, accounting, price-settlement | lots, their places, their recorded cost, their share of a price | `price-settlement`: sets the share percent (priority Batch, Product, POS, Organization); others not stated in what was read | not stated |
| **brand** (exists) | commercial-name grouping | not stated | not stated |
| **packages** in discount (exists) | bundle slots and limits | not stated; bundle rules are rules ([packages](../../../modules-plugable/economics/discount/packages/packages.md#policies-rules)) | not stated |
| **restriction** (exists) | global quantity constraints on a target (a freeze) | not a sales-audience limit ([sell-limit](edges/sell-limit/sell-limit.md#placement)) | not applicable to product |
| **pack** (proposed, new) | break-bulk: a quantity ratio between two products of one stock and the stock movement when one is opened | agent proposal: the organization that owns both products; removal does not undo past conversions | on sale of the child with no child stock: open one parent (event); converts stock |
| **deposit** (proposed, new, beside `refund`) | the coupling of a returnable item to its refundable claim | agent proposal: the seller; removal ends future couplings only | the return event repays the deposit |
| **eligibility** (no module: rule configuration through `condition_is`) | who may buy, when, how many; approval | the owner organization | the rule's own outcome; the kernel is told nothing |
| **comment / qa** (knowledge) | discussion and questions about a product through its content identity | not product's ([comment](edges/comment/comment.md#placement), [qa](edges/qa/qa.md#placement)) | not applicable |
| **buyers** (analytics, derived) | the audience of a product, derived from invoice items | not stored ([buyers](edges/buyers/buyers.md#placement)) | not applicable |

The pattern across the table: where a capability is new (offer, pack, deposit) it is proposed with all three of what, who, and what-it-triggers, and where it exists the tree often does not say. The gaps are listed in finding 5 as work, not repaired here.

### 3. Rival models

Four rival models of the product, with the status of each, then two smaller choices that the larger one depends on.

#### The models

- **A. Status quo: product = priceable node with the kernel `price` edge (Explored; the current state, not decided).** [product.md](product.md#unresolved-questions) itself asks whether price and pricing are kernel edges. Simple and right for a shop, a subscription, made-to-order goods ([Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#a-price-on-product-the-status-quo)). Trade-offs: the test fails for the museum piece and the spec (S7, S9); the kernel names pluggables in its own price policies (survey D11); one product holds one seller's price (S2, marketplace).
- **B. Thin product plus an offer capability (Tentative; recommended).** The kernel product is the admitted thing (finding 1); the stated price moves to the `offer` capability, keyed by seller and item, with validity and eligibility; pricing rules produce offers; the invoice item records the agreed price as its own fact referencing the offer version (already answered unratified, [item](../invoice/edges/item/item.md#open-questions)). **Migration cost is low by construction:** today's `price` edge is exactly a degenerate offer (seller = the owning organization, item = the product, eligible = everyone, validity open), so adopting B changes nothing visible until a second seller, a validity, or an eligibility is needed. Trade-offs: one more capability to define; the domain's defining word changes from "priceable" to "admitted", which touches the first paragraph of [product.md](product.md#definition-in-memar).
- **C. Product as a classification on thing, no domain (Explored; the strongest rival).** Following the [Premature Classification Check](../../../docs/modeling.practice.md#premature-classification-check): "Is X a product?" cannot be answered without caveats (the museum piece is, the unsold design may be), so a product may be a role, not a type. Fewest foundations ([Foundational Concepts Should Remain Few](../../knowledge/modularity/modularity.md#foundational-concepts-should-remain-few)). It becomes the better model if the independent-lifecycle test fails (owner question 2): if admission has no state and no rules of its own, there is no domain, only a loop-edge on thing. Trade-offs: the invoice, account, and offer then refer to `thing` plus the marker; `ProductModel` disappears; the existing "core by necessity" statement in [product.md](product.md) is rewritten.
- **D. Offering-centred: product = a seller's offering (Explored; rejected by confirmed positions).** The marketing sense: item plus seller plus terms. Rejected because the confirmed positions make the product independent of sale and of seller (≠ sellable, one product with many sellers, [product.md](product.md#definition-in-memar)); it would also copy the shared spec once per seller.
- **E. Product (kind) plus supply instance (batch, slot, movement) as a kernel pair (Deferred).** [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#c-a-general-supply-instance-batch-for-goods-slot-for-services-movement-for-transport) finds it conceptually strongest and not yet forced: only the batch exists as a node. Deferred until the `schedulable` module [service](../../../modules-plugable/economics/service/service.md#future-possibilities) anticipates has a second consumer. Model B is compatible: an offer's item may later be a batch or a slot.

**Not re-argued (Decided or confirmed, source):** Variant/SKU entities rejected; Requirement/Product split rejected; `Artifact` as unifying super-concept withdrawn ([handoff](product.handoff.md#decisions)); a price is derived from current stated prices, never from historical stock cost (Decided 2026-10-10, [pricing](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#decisions-2026-10-10)); pricing is a module family attached at product level while invoice-level adjustments are another level (Decided 2026-09-16).

#### How each model meets the cases (agent judgment)

"Fits" means no distortion; "strained" means it works only with a workaround; "fails" means it forces a wrong statement.

| Case | A status quo | B thin + offer | C classification | D offering | E kind + instance |
|---|---|---|---|---|---|
| S1 break-bulk | strained (no owner for the ratio) | fits, with `pack` | fits, with `pack` | strained (ratio per seller) | fits (lot) |
| S2 airtime | strained (no stated price) | fits (rule-priced offer) | fits (identity only) | fits | strained (no instance) |
| S3 prescription, recall | strained (flag on product) | fits | fits | strained | fits (batch) |
| S4 compulsory charge | strained (owner-declared) | fits if declarer may be an authority | same | strained (not an offering) | not applicable |
| S5 sponsorship | fits | fits | fits | fits | not applicable |
| S6 off-plan | strained (index terms) | fits (offer with terms) | fits | strained | fails (no instance) |
| S7 museum piece | fails (not priceable) | fits (admitted, no offer) | fits | fails | strained |
| S8 lucky bag | strained (composition on product) | strained, resolved at the lot | same | same | fits (instance) |
| S9 spec, exchange | fails (stored price) | fits (no offer; discovered) | fits | fails | strained |
| S10 deposit | strained (no coupling) | fits, with `deposit` | same | fits | not applicable |
| S11 sizes | strained (inheritance undefined) | fits (most-specific-first) | fits | strained | fits |

B and C never fail where A and D do; B and C differ only on whether the product has a domain of its own, which is the lifecycle test. That is why the recommendation is conditional (see [Recommendation](#recommendation-unratified)).

#### Smaller choice 1: one product-to-product relation, or several (Tentative: several)

The domain asks "single parent/child edge, or do several relations hide here" ([product.md](product.md#product-relation-to-product)). The cases show at least five relations, which differ in what they do to the count unit, to the stock, and to who may create them:

| Relation | Child or related product is | Count unit | Stock effect | Created by | Home |
|---|---|---|---|---|---|
| variant-of | the same thing differing in an attribute (size, colour) | same | independent stock per child | the owner of both | kernel (`variant`), Tentative |
| pack-of | the same stock in another unit (S1) | different, with a ratio | converts between them | the owner of both | `pack` (proposed) |
| component-of / material | what a made product consists of | any | consumption at production | the owner | `good` material (plan), batch/production (fact, S8) |
| bundle slot | a member of a sold set; may be optional | any | none until sold | the owner | `packages` |
| satisfies | a concrete product meeting a spec product (S9) | same | none | whoever asserts conformity, per its rule | `thing` (lineage; shared by design and building) |
| source | where a bought product comes from | any | none | the buyer | replacement-cost `source` |

A single edge with a type field would hide five sets of rules in a label, which the [Relationship Audit](../../../docs/modeling.practice.md#relationship-audit) (step 2) names as a defect, and would break "capability owns its edge and processing together" ([Modularity](../../knowledge/modularity/modularity.md#capability-completeness)) because the processing differs. `optional` is then a property of a bundle slot, not of any product relation ([optional](edges/optional/optional.md#placement) already suspects this).

One further observation (Explored): the thing `template` edge says a templated thing "MUST not [be used] in direct manner" ([template](../../identity/thing/edges/template/template.md)), and a variant parent is described as "itself a product even with no direct realization/transaction" ([variant](edges/variant/variant.md#model)). Whether a never-sold parent is a template-marked product, rather than a product of a special kind, is worth one question (owner question 6).

#### Smaller choice 2: what becomes of the type-flag space (Tentative: dissolve)

The `Type uint64` flag space on the product record ([type-flags](edges/type-flags/type-flags.md#model)) puts the good/service split, sales limits, and the rest of its 30 flags into one kernel field. That contradicts "Good and service are NOT core" ([product.md](product.md#definition-in-memar)) and is the implementation contamination of a bitmask ([Implementation Contamination Check](../../../docs/modeling.practice.md#implementation-contamination-check)). The proposal: each flag is read as the thing it names, owned by the capability that gives it meaning; the kernel keeps no flag. The owner-question catalogue already recommends this direction ("dissolve to named loop labels", E4, [catalogue](../../../.agents/tasks/20261014T071404Z-26308-0/report.md)). Mapping, flag by flag (agent; "source" where a document says so, otherwise a guess to verify):

| Flag | Proposed owner | Basis |
|---|---|---|
| `Type_Good` / `Type_Unset` | not a flag: a lens an organization draws; or a loop label in `good` | [type-flags](edges/type-flags/type-flags.md#open-questions) asks this; [good](../../../modules-plugable/economics/good/good.md) |
| `ReserveValidity`, `ReserveQuantity` | `good` reserve-quantity; reserve validity is an item matter | [item](../invoice/edges/item/item.md#policies-rules); [reserve-quantity](../../../modules-plugable/economics/good/edges/reserve-quantity/reserve-quantity.md) |
| `PreSale` | derived: a product whose first instance is in the future, i.e. the invoice's pre-order | [buy-limit](edges/buy-limit/buy-limit.md#open-questions); [pre-order](../invoice/edges-shortcut/pre-order/pre-order.md) |
| `NeedApprove`, `NeedPrescription`, `SellLimit_Role/Group/User` | eligibility rules via `condition_is`; the product-role basis is a missing edge | [sell-limit](edges/sell-limit/sell-limit.md#placement) |
| `InvoiceSell`, `OrderSell` | unknown: no read document says what these select; agent guess: sales channels | none |
| `Inventory`, `BestBefore`, `CustomIngredient`, `Custom` | `good` capabilities and `customable` | [type-flags](edges/type-flags/type-flags.md#model) |
| `TimeValidity`, `Duration`, `Share`, `Shipping`, `Area` | unknown: no read document defines them | none |
| `Timing`, `TimingInterval`, `MultipleUse`, `Number`, `Seat`, `Place`, `Provider_Staff`, `Provider_Role` | `service` edges of the same names | [type-flags](edges/type-flags/type-flags.md#model); [service](../../../modules-plugable/economics/service/service.md) |
| `Transport` | strip the coordinate recipe | [coordinate](edges/coordinate/coordinate.md#placement) |
| `Content` | the content identity (Product ∩ Content is confirmed) | [product.md](product.md#definition-in-memar) |

### 4. What the domain must own, as requirements questions

Written as questions favouring no answer where unsettled. A citation means the document already answers or constrains the question; "open" means nothing in the tree decides it.

#### Identity
- What makes two nodes the same product: the UUID alone? Names are labels, identity is the UUID ([Modules → Placement](../../modules.md#placement)); a part number identifies a design within a corporation ([product.md → Part Number](product.md#part-number)). May a part number, barcode, or ISBN identify, or only label (`isbn_is` is a [uri](../../../modules-plugable/uri/isbn/isbn.md) reference)?
- When does a thing take the product identity: by an explicit act of a declaring organization (acquired), or by being referred to by its first economic act (discovered)? (S7 and S6 favour explicit; the [handoff](product.handoff.md#open-questions) holds the weak criterion "capable of being sold".) Open.
- Is there one product node per organization with a mapping, or one shared identity across organizations? The owner has not decided ([invoice exchange](../invoice/invoice.handoff.md#open-questions)); S2 and S9 push both ways. Open.
- Does identity survive a change of count unit, of lens (good to service), of owning organization (a merger), of producer? [Supersedes](../../identity/thing/edges/supersedes/supersedes.md) says a size or colour child is not a supersession; it does not say what a unit change is. Open.
- Is a spec product defined by a body that neither produces nor sells it, and who may define one ([brand](../../../modules-plugable/economics/brand/edges/brand/brand.md))? Open.
- Is a never-sold parent a product, or a template-marked thing? Open.

#### Lifecycle
- What states does admission have: declared, admitted, suspended, withdrawn, superseded? Which are one-way? Open.
- May a product be admitted when no one can ever produce it (a chair design never to be produced)? The handoff names this as blocking the Product-versus-Definition boundary ([handoff](product.handoff.md#open-questions)). Open.
- May the count unit change after the first act on the product? Every quantity ever recorded changes meaning if so. Open (default proposed in owner question 8).
- What does withdrawal do to what depends on the product: open invoice items, live offers, stock, pricing rules attached, sources and index components that point at it, followers, parents and children? Is withdrawal blocked while dependents exist, or does it emit an event the dependents answer? Open.
- Is deletion ever allowed? A price is never deleted ([price.md](edges/price/price.md#policies-rules)) and state change is modeled as events ([Modeling](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates)). Open for the product itself.
- When a parent is withdrawn, what happens to its children? Open.

#### Authorization
- Who may declare a product: staff by a role, or by delegation ([delegate](../../rights/delegate/delegate.md))? May an authority declare one acting under a law (S4)? [price.md](edges/price/price.md#policies-rules) says only "the organization that owns the product" creates its price; the tax decision says tax is a product. Open.
- Who may attach or detach each capability on a product: the rule in the tree is "only the organization that owns the product" for price and pricing; is that universal? A buyer's source pointing at a seller's product is authorized by the seller through follow ([source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md#policies-rules)).
- Who may read a product: is a catalogue entry public by default? May a product be hidden from some users (the confidential spec, the prescription product)? Open.
- Who may withdraw, and does withdrawing another organization's reference (its `source` to your product) need your consent? Open.
- Who may assert that a concrete product satisfies a spec: the producer, the spec's definer, an independent assessor? The estate handoff already distinguishes a certificate (a trusted claim) from a permission ([estate handoff](../../identity/estate/estate.handoff.md#decisions)). Open.

#### Rules
- Which rules does the kernel itself require, and which are organization policy through `condition_is`? Candidate kernel rules: one count unit; no cycle in the kind link; a child shares the parent's count unit (variants only). Open.
- Which rule attaches to the parent and which to the child, and which wins when both exist? The only precedent is most-specific-first for price settlement. Open.
- Is "may be bought" ever a property of the product rather than of the buyer, the time, and the seller's policy? S3 says no. Open.
- May a product's declaring rule change after acts exist, for example a new eligibility rule applying to an already-issued but unpaid invoice (compare [item open question](../invoice/edges/item/item.md#open-questions))? Open.
- Where do customization rules for made-to-order goods live: on the product ([customable](edges/customable/customable.md)) or on the offer? Open.

#### Events
- Which facts must the product domain emit: declared, admitted, suspended, withdrawn, superseded, structure changed (child added or removed)? The kernel exposes an event target, not a new event model ([Modularity → Event as a Module Capability](../../knowledge/modularity/modularity.md#event-as-a-module-capability)).
- Who listens: offers (close), pricing (detach or hold), replacement-cost sources and price-index components that point here, followers (deliver), packages (a bundle slot loses a member), inventory (stop receiving), invoice (refuse new items). Is each reaction the listener's own rule, never a cascade the product domain performs? Open.
- Are events delivered across organizations through follow, and is a withdrawal a followable fact with its own time? ([follow](../../identity/thing/edges/follow/follow.md#open-questions) holds the delivery questions.) Open.

### 5. How the existing edge folders map

Without moving anything. Verbs: **keep** (stays a product relation), **reclassify** (a different home or form), **retire** (the claim belongs elsewhere or is derived), **missing** (nothing exists yet). The mapping applies the [Modules → Edge folder](../../modules.md#edge-folder) sections and each document's own Placement, and flags where it departs from them.

| Folder | Verb | Proposed disposition | Basis |
|---|---|---|---|
| [variant](edges/variant/variant.md) | keep | The one kernel kind link, parent/child, with a cycle rule and the inheritance decision (owner questions 5, 6); name stays a vocabulary choice | its own Placement; confirmed parent/child |
| [price](edges/price/price.md) | reclassify (conditional) | Under model B the price edge becomes a degenerate case of `offer`; until the owner decides, keep as is. Its policies name the replacement-cost, follow, and index consequences: those belong to the capability that owns the price, not the kernel doc (survey D11) | owner questions 3; [price.md](edges/price/price.md#placement) says "on product, for now" |
| [price-settlement](edges/price-settlement/price-settlement.md) | retire (duplicate) | The batch module holds the same edge with the same priority text ([batch price-settlement](../../../modules-plugable/economics/batch/edges/price-settlement/price-settlement.md)). Two copies of one edge is the defect [One Authoritative Location](../../../docs/modeling.md#one-authoritative-location-per-concerns-data) names; catalogue B4 default: "price-settlement with batch" | both documents |
| [type-flags](edges/type-flags/type-flags.md) | retire as a flag space | Dissolve per the flag table in finding 3; `edges/product.kh` goes with it; nothing converts | owner question 10; catalogue E4 |
| [customable](edges/customable/customable.md) | reclassify | Generic `condition_is` attachment; the kernel must not name the rule domain (survey D10); the configuration semantics of made-to-order goods need an owner (owner question, rules) | [Modules → Placement](../../modules.md#placement) |
| [sell-limit](edges/sell-limit/sell-limit.md) | reclassify | Rule configuration through `condition_is`; the `product-role` basis is a missing edge | its own Placement |
| [buy-limit](edges/buy-limit/buy-limit.md) | reclassify | Rule configuration; `Type_PreSale` is derived from a future-instance product (invoice pre-order); a pre-sale warning belongs to the offer's terms | its own Placement; [price-index deferred-payment](../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales) |
| [provider](edges/provider/provider.md) | reclassify | `service` capability (proposed in its own Placement) | its own Placement |
| [supplier](edges/supplier/supplier.md) | reclassify | Fold into replacement-cost `source` (the procurement reading); the "parallel nodes per provider" reading needs no edge. Needs owner ratification (the document asks it) | [source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md#placement) |
| [material](edges/material/material.md) | reclassify | One home: [good material](../../../modules-plugable/economics/good/edges/material/material.md) for the declared composition (plan); actual composition on the batch/production side (S8). The document itself says "never two copies" | its own Placement; S8 |
| [optional](edges/optional/optional.md) | retire | A property of a bundle slot in `packages`, not a product relation | its own Placement |
| [buyers](edges/buyers/buyers.md) | retire | Derive from invoice items (analytics) | its own Placement |
| [comment](edges/comment/comment.md) | retire | Knowledge/reaction through the content identity | its own Placement |
| [qa](edges/qa/qa.md) | retire | `knowledge/question` plus ordinary group membership | its own Placement |
| [coordinate](edges/coordinate/coordinate.md) | retire | Not an edge: a lookup recipe | its own Placement |
| `edges/README.md` | reclassify | A pointer list; the survey proposes folding it into product.md (D7); membership is the directory ([Modules → Edge folder](../../modules.md#edge-folder)) | survey T6 |
| `protocol/*.kh` (two files) | keep | Converted, accepted; `ProductModel ab { ThingModel }` is only identity, and this research is the design rule 6 asks for before it grows | [handoff](product.handoff.md#khayyam-conversion-2026-10-03) |
| `edges/price/protocol/*.kh` | blocked | Follows the price decision and the money module; not touched | [handoff](product.handoff.md#also-unconverted) |
| `_import/product-auction/**` | retire after harvest | The legacy `ProductAuction` record (organization, product, discount minus from price, authorization of users and groups, type, status) is the evidence for the `offer` shape; harvest it into the offer sketch, then delete or re-model as the handoff already says | [handoff](product.handoff.md#also-unconverted); [storage.kh](_import/product-auction/storage.kh) |
| `_import/product-cost`, `product-price` | retire | cost belongs to batch cost; price duplicates the price protocol | [handoff](product.handoff.md#also-unconverted) |
| `_import/product-min-slice-to-buy.txt` | reclassify | A purchase multiple on the offer (schema.org `eligibleQuantity` is the closest outside shape, [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#methodology)) | S1 |

**Missing** (nothing in the tree): `offer`, `pack`, `deposit`, the product-role/approver edge, a `satisfies` edge on thing, a batch-level actual composition, the admission status vocabulary, and a product-level event target. Finding 6 sketches each.

**The proposal in numbers (agent):** of 15 edge folders, 1 stays, 7 are reclassified (one conditionally), and 7 retire as product edges; `edges/README.md` is a pointer. The kernel shrinks from "everything a product can have" to four elements.

### 6. Missing edges and modules

Each is a proposal (Tentative or Explored as marked); none is created here. Each names what, who creates and removes, and what it triggers, because an edge without those does not exist ([Modules → Placement](../../modules.md#placement)).

**6.1 `offer` — pluggable under `modules-plugable/economics/offer` (Tentative).** The seller's stated price as a node-shaped record: the seller, the item it covers (a product now; a batch or a slot when those exist), amount, count unit or display basis (a compound unit such as kg·km, passenger-km, per hour, or a state such as "on request", "negotiable", "market"), validity, eligible buyers, and a purchase multiple or minimum (S1). It owns versions: a change is a new version, never an overwrite, and each version references the inputs it came from. Only the seller that owns the item creates an offer and a new version; withdrawal is a new fact, never a deletion. A version triggers what any price version triggers today: one delivery per follower, replacement-cost re-evaluation of dependents, index recomputation ([price.md](edges/price/price.md#policies-rules)). It absorbs the `price` edge as a degenerate case and the legacy `ProductAuction` ([storage.kh](_import/product-auction/storage.kh)). Open: whether a rule-stated price is written here on the owner's behalf or carried by `pricing` ([pricing open questions](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#open-questions)).

**6.2 Admission status vocabulary — kernel loop-edge, not a module (Tentative).** A small shared status set (declared, admitted, suspended, withdrawn) recorded as events with time and declarer, defined once with the other shared statuses and taken by the product under the product's own rule for when a product may take each ([Placing a relation](../../../docs/modeling.practice.md#placing-a-relation)). Created by the declaring organization (or an authority, S4); never deleted. Its triggers are the events in finding 4. Where statuses live (`edges-loop/` or `status/`) is the survey's R4.

**6.3 `pack` — pluggable under `modules-plugable/economics/pack` (Tentative, to be checked against `inventory`).** Break-bulk (S1): a relation between two products that share one stock, carrying the quantity ratio, with the processing of converting stock when one is opened. Created and removed by the organization that owns both products; removal ends future conversions only. When a child is sold with no child stock, the capability opens one parent unit (a recorded event) and credits the child stock. It is not a variant (the unit changes), not a material (it is not made of), and not a source (the relation is internal to one organization's stock). The replacement-cost `Quantity` field is the same fact seen from procurement, which suggests the ratio should have one owner. Open: whether this belongs in `inventory` ([inventory](../../../modules-plugable/economics/inventory/inventory.md) holds only a stub edge today).

**6.4 `satisfies` — an edge on `thing`, owned by thing (Explored).** A concrete product meets a spec product (S9), and a building realizes a design (S6, [estate handoff](../../identity/estate/estate.handoff.md#assumptions) lists `realized_from` as Unexamined). Because a design, a law, an estate, and a product can all need it, it is defined once on thing ([A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once)) and not copied into product. Who creates it, and what it triggers (price comparison across satisfying products, a recall of every satisfying product when the spec is found defective), is open; the estate handoff's certificate split (a trusted claim versus a permission) is the closest existing distinction.

**6.5 Product-role approver — an edge for approval, owner to be decided (Explored).** `NeedApprove` is "base on product-role" ([type-flags](edges/type-flags/type-flags.md#model)) and the sell-limit document asks whether `product-role` is a missing edge ([sell-limit](edges/sell-limit/sell-limit.md#open-questions)). If approval is an act with a request, an approver, and an outcome, it is a capability (management/authorization territory, [authorization](../../../modules-plugable/management/authorization/authorization.md) not read here); if it is a rule attached by `condition_is`, there is no module. The research cannot decide which without reading that module.

**6.6 `deposit` — pluggable beside `refund` (Explored).** The coupling of a returnable item to its refundable claim (S10). Created by the seller on the sale; the return event triggers repayment to whoever returns the item, not necessarily the buyer. The existing [refund](../../../modules-plugable/economics/refund/refund.md) is `(invoice)-[:refund]->(rule)` and names no coupled product, so this may be a rule family inside refund rather than a module. Open: whether the deposit is a product of its own (it has a price and a life) or a term of the offer.

**6.7 Batch-level actual composition — an edge in `batch`/`production` (Tentative).** For S8: what was packed is recorded as a fact of the lot at production; the product's material edge is declared intent. This is an extension of [production](../../../modules-plugable/economics/production/production.md) and batch, not a product module. The value promise of a lucky bag is a rule evaluated against replacement cost.

**6.8 Product event target — a capability of the kernel product (Tentative).** The kernel exposes an event target for admission and structure facts; it does not introduce an event model ([Modularity](../../knowledge/modularity/modularity.md#event-as-a-module-capability)). Listeners are the capabilities in finding 4. Without it, every dependent re-implements discovery of a withdrawal.

**6.9 Authority-declared product — no module (Tentative).** S4 needs nothing new in the product domain: the declarer may be an authority acting under a law; the compulsion is a rule that issues an invoice, not a property of the product. The change is to the sentence in [price.md](edges/price/price.md#policies-rules) and the product documents, and to the declarer authorization question.

### 7. Test scenarios

Given/when/then in prose, so another session can write tests once the owner decides. Each is marked with what it depends on: **kept** if it follows from settled text, **B** if it assumes model B, **Q n** if it assumes the default of open question n.

1. **Identity before production (kept).** Given an organization declares a product "car, model X" with count unit "piece" and no batch exists. When the product is admitted. Then an invoice item may name it (a pre-order), no stock exists, and nothing requires a producer or a brand.
2. **A price is a new version, never an overwrite (kept).** Given a product with a stated price of 100 in one currency. When its owner states 120. Then both versions exist in order, the first is not altered, and each follower receives one delivery with the new version. An invoice item issued under the first keeps 100 as its own fact (answered unratified).
3. **Only the owner states the price (kept).** Given product P of organization A. When organization B tries to attach a pricing rule or state a price for P. Then it is refused; B may follow A's price and point its own product's `source` at P.
4. **No bare delete (kept in spirit, Q 9).** Given a product with history. When its owner tries to delete it. Then the request is refused or recorded as withdrawal; history stays readable.
5. **Count unit is fixed once acts exist (Q 8).** Given product P with count unit "kg" and one issued invoice item. When the owner changes its unit to "g". Then the change is refused and the owner is directed to supersede P by a new product.
6. **Parent and child (kept).** Given a shoe parent and children "size 40" and "size 41", each with its own stock. When one pair of size 41 is sold. Then only the size-41 stock changes and the parent has no stock of its own.
7. **No cycle (Q 5).** Given A is the parent of B. When B is declared the parent of A. Then the kind link is refused.
8. **Child inheritance (Q 6).** Given a parent with an offer of 80 and a child with none. When the child is offered for sale. Then, under the default of no inheritance, the child has no price until it is stated; under a most-specific-first rule, the child's own offer would win if it existed and the parent's would not apply by itself.
9. **Break-bulk (B, Q 5).** Given a carton of 12 sticks with 2 cartons in stock and 0 sticks, and a `pack` relation of ratio 12. When one stick is sold. Then one carton is opened (recorded), stock reads 1 carton and 11 sticks, and the stick sale proceeds.
10. **Withdrawal with live dependents (Q 9).** Given a product with an issued unpaid item, a live offer, a pricing rule attached, and a buyer organization's `source` pointing at it. When the owner withdraws it. Then new items and offers are refused, the live offer is closed by an event, the unpaid item remains valid at its issue-date price, and the buyer's replacement cost falls back to quotes.
11. **Admission without an offer (B).** Given a museum piece admitted with no offer and held by an account of one piece. When it is lent to another museum. Then custody changes in the account and legal title does not; no invoice is required; the piece never appears in a catalogue.
12. **Deaccession adds an offer without changing identity (B).** Given the same piece. When the museum decides to auction it and an offer is attached. Then the product identity, its history, and its provenance are unchanged and the offer is the only new fact.
13. **Authority-declared product (Q 7).** Given a law-created product "annual property tax" declared by an authority. When the assessment rule runs for person X. Then an invoice is issued to X without X's choosing, the price is the rule's result referencing its inputs, and X cannot remove the product.
14. **Eligibility from outside (kept).** Given a product with a `condition_is` rule requiring a valid prescription credential. When a user without one adds it to an invoice. Then the rule denies; the product domain was not asked and holds no flag.
15. **Recall by lot (kept).** Given a product with three lots and one contaminated. When the recall is triggered. Then every position of that lot (and its sub-lots) is found without giving identity to each unit, and the product's identity and its other lots are unaffected.
16. **Lucky bag (B, Q 12).** Given a "lucky bag at 10000" product. When a lot of bags is packed. Then the actual composition is recorded as a fact on the lot, the product carries no composition, and a value rule compares the contents' replacement cost with 10000.
17. **A spec with no seller (kept).** Given the spec product "rebar A3, 16 mm" and two sellers' products that satisfy it. When a user views the spec. Then a "from" price and a seller count are discovered from the satisfying offers and not stored on the spec; neither seller can edit the other's product.
18. **Exchange-traded goods (kept).** Given a fungible commodity traded by order matching. When no seller states a price. Then the product exists, has no offer, and its price is the last deal, discovered.
19. **Returnable bottle (B, sketch 6.6).** Given a drink sold with a deposit. When the empty bottle is returned at another shop. Then the deposit is repaid to the returner and the claim is closed.
20. **Cross-organization withdrawal (Q 4, Q 9).** Given a buyer's product that points at a seller's product through `source`. When the seller withdraws its product. Then the buyer is told through the follow it created, its replacement cost falls back to quotes, and nothing in the buyer's history changes.
21. **Co-typing (kept).** Given an educational course that is both a product and content. When it is admitted. Then the same node is a product (economic lens) and content (knowledge lens), with no second identity.
22. **Edge-doc completeness (a documentation test).** Given every edge document under `edges/` after the mapping is applied. When read against [Modules → Edge folder](../../modules.md#edge-folder). Then each has Model, Policies, Placement, and Open questions, and each edge states who creates or removes it and what it triggers.

### Contradictions found

Reported, not resolved, as asked. Each cites both sides.

1. **The definition's base.** [product.md](product.md#definition-in-memar) defines a product as the unit of priceability, with the marketing definition as prior art; the [handoff](product.handoff.md#key-definitions-established) records as Decided a dictionary base "an artifact that has been created by someone or some process" and says it graduated into README.md, where it is absent.
2. **What a product is relative to sale.** "Product is anything the system sells — not goods" (Decided 2026-09-16, [handoff](product.handoff.md#decisions-from-organization-ideas-backlog-2026-09-16)) and the owner-question catalogue's default for D1 ("product = organization-declared sellable", [catalogue](../../../.agents/tasks/20261014T071404Z-26308-0/report.md)) against "Product ≠ Sellable/Commercial Product" ([product.md](product.md#definition-in-memar)).
3. **Graduations claimed and absent.** The handoff says its Decided items graduated into the domain's confirmed positions, naming "one-product-many-sellers", "dictionary definition as base", and "designer specification precision"; [product.md](product.md#definition-in-memar) holds the spec-like-nodes position but not the first two as positions.
4. **Who owns a product versus many sellers.** [price.md](edges/price/price.md#policies-rules) and the price data model say only the organization that owns the product creates its price, while [brand](../../../modules-plugable/economics/brand/edges/brand/brand.md) says one product has many sellers; already noted in [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#a-marketplace-where-several-sellers-offer-one-product).
5. **The kernel names pluggables.** [price.md](edges/price/price.md#policies-rules) names replacement cost, price index, and follow; [economics.md](../economics.md#everything-else-is-pluggable) says core domains must not know pluggables (survey D11). Follow is on thing and is fine; the other two are the issue.
6. **Good and service are not core, but the flag space is.** [product.md](product.md#definition-in-memar) says good and service are pluggable; [type-flags](edges/type-flags/type-flags.md#model) keeps `Type_Good` ("if flag not set means product is service") in the product record, and its Placement says "core keeps only the ability to carry org-chosen type bits", which is a partial reconciliation.
7. **Two copies of price-settlement.** [product price-settlement](edges/price-settlement/price-settlement.md) and [batch price-settlement](../../../modules-plugable/economics/batch/edges/price-settlement/price-settlement.md) hold the same priority text under different subjects.
8. **A kernel edge to the rule domain.** [customable](edges/customable/customable.md#model) is `(product)-[:customable_by]->(rule)`, against "Kernel does not reference the rule domain directly" ([Modules → Placement](../../modules.md#placement); survey D10, R5 in the owner questions).
9. **The handoff's header.** [product.handoff.md](product.handoff.md#status) is "Paused (2026-08-09)" and holds decisions of 2026-09-16 and 2026-10-10.

## Recommendation (unratified)
The owner has not reviewed this, and nothing in it is decided.

1. **Redefine the test (Tentative, medium confidence).** Replace "anything that can be priced" with "a thing a declaring organization has admitted to economic acts", and treat price as one capability a product may or may not have. The museum piece and the spec stop being exceptions, and pricing research's finding that price does not belong on the product alone stops contradicting the definition. This changes the first paragraph of the domain document and nothing else visible.
2. **Keep a four-element kernel (Tentative):** identity, admission status as events, the one kind link, and the `condition_is` attachment point. Everything else is a capability or a rule.
3. **Choose B over A, and keep C open until the lifecycle test is answered (Tentative).** B costs almost nothing to adopt because today's price edge is a degenerate offer. C wins only if admission has no lifecycle or rules of its own; question 2 asks it.
4. **Split the product-to-product relation by what each relation does to the count unit, the stock, and who creates it (Tentative).** Keep `variant` in the kernel; give `pack`, material, bundle slot, `satisfies`, and `source` to their owners.
5. **Dissolve the type-flag space (Tentative),** flag by flag as in finding 3, and convert nothing from `edges/product.kh`.
6. **Do not move, delete, or convert anything on this evidence.** The mapping in finding 5 is a reading list for the sessions that will, after the owner answers.
7. **Ask the three questions that change what the work is first:** question 1 (what is the test), question 2 (is there a domain at all), and question 3 (does the stated price leave the product).

## Open Questions
This is the research's eighth section. Only the owner can decide these. Ordered by what they change: those that change what the domain is first, then those that change how a part is done ([Ask rather than assume](../../../docs/cognition.md#discourse-norms-derived-from-this-model)). Each carries a recommended default and what it blocks. They are also entered in the [handoff](product.handoff.md#open-questions).

1. **What is the product domain's defining test: priceability, or admission to economic acts?** Default: admission; priceability is a capability. Blocks: the domain Definition rewrite, the type-flags mapping, the asset-management half (handoff Next Step 3), and the price edge's location.
2. **Does admission have a lifecycle and rules of its own, so that product is a domain and a node, or is product a classification (loop-edge) on thing?** Default: a domain, because the cases show a declarer, long pre-existence, and withdrawal. Blocks: model B versus C, the design of `ProductModel` beyond `ThingModel` (Khayyam rule 6), and whether the invoice's "zero products" question (invoice Unresolved) matters.
3. **Does the stated price leave the product for an `offer` capability, with today's price edge as its degenerate case?** Default: yes in principle; migrate only when a second seller, a validity, or an eligibility first appears. Blocks: the price edge's `.kh` conversion, Pricing Research 001 questions 1 and 7, how the invoice item references what it copied, price-settlement's home.
4. **One product node per organization with a mapping, or one shared identity across organizations?** Default: one per organization; a shared spec product that sellers' products `satisfy` covers the marketplace. Blocks: invoice exchange, `supplier`/`source`, brand's open questions, S2.
5. **Is the product-to-product relation split by what it does (kind link in the kernel; `pack`, material, bundle slot, `satisfies`, `source` elsewhere)?** Default: split. Blocks: the variant, optional, material, and supplier documents, and any parent-child conversion.
6. **Does a child inherit its parent's attachments (offers, rules, labels), and is a never-sold parent a template-marked thing?** Default: no inheritance; most-specific-first only where a setting says so; the parent is a product of the same kind (the confirmed position). Blocks: variant semantics, price resolution for sizes, the template relation.
7. **Who may declare a product: only the owning organization, or also an authority acting under a law?** Default: also an authority; compulsion is a rule on invoice issue. Blocks: tax as a product, the sentence in price.md, the declarer authorization.
8. **Is a product's count unit immutable once any act refers to it?** Default: immutable; change by supersession. Blocks: the lifecycle, the supersedes policy, and any unit conversion design.
9. **Is withdrawal blocked while dependents exist, or an event the dependents answer?** Default: an event; dependents react by their own rules; existing invoices are unaffected. Blocks: lifecycle, the event target, cross-organization effects.
10. **Do the type flags dissolve into their owners (finding 3)?** Default: yes. Blocks: `edges/product.kh` (stays unconverted), catalogue E4.
11. **Where does the asset-management half live?** Default: an `account` of the piece, `rights/ownership` for title, `batch`/`exist` for place, and admission without an offer; no new module. Blocks: the survey's inventory-scope question (P6), the handoff's open question 4.
12. **Is a product's composition a plan and a lot's composition a fact?** Default: yes. Blocks: convergence of the two material documents, lucky-bag and recall designs.
13. **How is a compulsory purchase issued: a rule that issues the invoice, or an offer the buyer may not decline?** Default: a rule on issue. Blocks: the tax and VAT modules' relation to product, the "forced purchase" statement in invoice.
14. **Where does `satisfies` live and who may assert it?** Default: an edge on thing; the asserter is decided by the rule of the domain (a certificate, not a permission). Blocks: brand's three questions, estate suite cases 4 and 5.

## Related Artifacts
- [product.md](product.md) — the first paragraph of Definition and the Unresolved questions change if question 1 is accepted (Review)
- [product.handoff.md](product.handoff.md) — gains questions 1 to 14 and Next Steps (Update, done in this chat)
- [product.changelog.md](product.changelog.md) — entry for this research (Update, done)
- [edges/type-flags](edges/type-flags/type-flags.md), [edges/price](edges/price/price.md), [edges/price-settlement](edges/price-settlement/price-settlement.md) — most changed by the mapping (Review)
- [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md) — shares questions 1, 3, 4 (Review)
- [replacement-cost source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md), [batch](../../../modules-plugable/economics/batch/batch.md), [good](../../../modules-plugable/economics/good/good.md), [service](../../../modules-plugable/economics/service/service.md) — receive the reclassified edges (Review)
- [invoice](../invoice/invoice.md) and its [handoff](../invoice/invoice.handoff.md#open-questions) — the zero-products and invoice-exchange questions (Related)
- [estate handoff](../../identity/estate/estate.handoff.md) — the co-developed boundary and the suite cases (Related)
- [thing](../../identity/thing/thing.md) — would own `satisfies` (Review)
