# Product Handoff

## Topic & Purpose
Drawing Product's boundary: against Sellable/Commercial Product, against physical goods, against Content, against Estate, and against separate Variant/SKU/Definition/Batch entities. Co-developed with the Estate boundary discussion (building-as-product-for-sale, furniture-in-estate, designs).

## Status
Paused (2026-08-09) — resumed with the estate boundary work.

## Decisions from Organization ideas backlog (2026-09-16)
- **Product is anything the system sells — not "goods".** Tax is a product (bought under compulsion, with per-person pricing rules); insurance, healthcare services, charity sponsorship packages ("adopt a child for a month" is a product with a different output), API subscriptions. There is no organization — hospital, charity, government — without products; they differ in output, not in structure. *(decided)*
- **Pricing is a module family, not one module.** A transportation service's price varies by city, hour, route, zone, demand — hundreds of independently evolving pricing modules for one organization (Uber example), all attached to the Product level while invoice-level rules (zeroing a user's bill) are a *different* level: an Invoice-level rule making the payable zero does not make the service's price zero. *(decided)*

## Decisions
All Decided items are graduated into [`README.md`](README.md): "Confirmed positions" (≠ sellable, ≠ physical good, identity-before-production, one-product-many-sellers, parent/child without Variant, Product∩Content, dictionary definition as base, spec-like nodes are products, designer specification precision) and the Discussion section (rejected alternatives). Do not restate them here.

Rejections recorded there for the record (with reasoning):
- Separate Variant/SKU/Model entity types — rejected (category proliferation; the child-shoe is genuinely a product).
- Requirement/Product split — rejected (the spec-like rebar node has all product responsibilities; artificial boundary).
- `Artifact` as unifying super-concept — withdrawn (too broad; the content domain would swallow it).

## Ambiguities Resolved
- Assistant's conflation of Product with Commercial Offering — resolved by Omid's museum/furniture cases (asset management is the other half of product's purpose).
- Assistant's conflation of Product with physical goods — resolved by the services case; "needs physical realization?" is not a product question at all.
- Assistant's tree-thinking (Product as child layer of Estate) — resolved by the multi-typing principle (Omid's repeated correction); OOP class-lens named as the bias source.

## Open Questions
Canonical homes per the map in [`README.md`](README.md). Still cross-cutting here:
- When does a thing take the Product identity? (weak criterion "capable of being sold" — economic/asset-management treatment, not necessarily a transaction) — does not block, but shapes everything.
- Producibility test: a chair design never to be produced — product or not? — **blocks** the Product-vs-Definition boundary (#3 in brand README).
- Product ∩ Content ∩ Estate tri-boundary and the edge-rule caveat (one identity may forbid another) — **blocks** the estate suite cases 4, 5.
- Asset-management half vs inventory/logistics pluggable: does warehousing/transfer belong here or in the inventory module? — does not block.
- Price ownership: product or batch (owner's leaning: batch, 2026-10-10; the service analogue unsettled; price and pricing not finished) — shapes the priceability test, what an invoice item references, and what a buyer's replacement-cost source follows. Canonical question in [product.md](product.md#unresolved-questions); the owner's eight questions are in [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions).

### From Product Research 001 (2026-10-16, agent proposals, nothing ratified)
Each entry: the question, the recommended default, what it blocks. Ordered by what they change: those that change what the domain is first. Reasoning, scenarios, and rival models are in [Product Research 001](product.research.001.md#open-questions).
1. **What is the domain's defining test: priceability, or admission to economic acts?** Default: admission; priceability is a capability a product may or may not have. Blocks: the Definition rewrite in [product.md](product.md#definition-in-memar), the type-flags mapping, the asset-management half (Next Step 3), the price edge's location.
2. **Does admission have a lifecycle and rules of its own (so product is a domain and a node), or is product a classification on thing?** Default: a domain. Blocks: model B versus model C in the research, the design of `ProductModel` beyond `ThingModel` (Khayyam rule 6), the weight of the invoice's "zero products" question.
3. **Does the stated price leave the product for an `offer` capability, today's price edge being its degenerate case?** Default: yes in principle, migrate only when a second seller, a validity, or an eligibility first appears. Blocks: the price edge's `.kh` conversion, [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions) questions 1 and 7, what the invoice item references, price-settlement's home.
4. **One product node per organization with a mapping, or one shared identity across organizations?** Default: one per organization; a shared spec product that sellers' products satisfy covers the marketplace. Blocks: [invoice exchange](../invoice/invoice.handoff.md#open-questions), supplier/source, brand's open questions.
5. **Is the product-to-product relation split by what it does to the count unit, the stock, and who creates it** (kind link in the kernel; pack, material, bundle slot, satisfies, source elsewhere)? Default: split. Blocks: the variant, optional, material, and supplier documents; any parent-child conversion.
6. **Does a child inherit its parent's attachments (offers, rules, labels)? Is a never-sold parent a template-marked thing?** Default: no inheritance; most-specific-first only where a setting says so; the parent stays a product. Blocks: variant semantics, price resolution across sizes.
7. **Who may declare a product: only the owning organization, or also an authority under a law?** Default: also an authority; compulsion is a rule on invoice issue. Blocks: tax as a product, the creator rule in [price](edges/price/price.md#policies-rules).
8. **Is the count unit immutable once any act refers to the product?** Default: immutable; change by supersession. Blocks: the lifecycle, the supersedes policy.
9. **Is withdrawal blocked while dependents exist, or an event the dependents answer?** Default: an event; existing invoices unaffected. Blocks: the lifecycle, the product event target, cross-organization effects.
10. **Do the type flags dissolve into their owners?** Default: yes, flag by flag as in the research. Blocks: `edges/product.kh` (stays unconverted), the catalogue's E4.
11. **Where does the asset-management half live?** Default: an account of the piece, `rights/ownership` for title, `batch`/`exist` for place, admission without an offer; no new module. Blocks: the survey's inventory-scope question (P6), the open question on asset-management above.
12. **Is a product's composition a plan and a lot's composition a fact?** Default: yes. Blocks: convergence of the two material documents, lucky-bag and recall designs.
13. **How is a compulsory purchase issued: a rule that issues the invoice, or an offer the buyer may not decline?** Default: a rule on issue. Blocks: the tax and VAT modules' relation to product.
14. **Where does `satisfies` (a concrete product meets a spec product, a building realizes a design) live, and who may assert it?** Default: an edge on thing; the asserter is decided by the rule of the domain. Blocks: [brand](../../../modules-plugable/economics/brand/edges/brand/brand.md)'s open questions, estate suite cases 4 and 5.

### Contradictions between this domain's documents (reported by Product Research 001, not resolved)
See [Contradictions found](product.research.001.md#contradictions-found): the definition's base (marketing prior art and "unit of priceability" versus the Decided dictionary base); "anything the system sells" versus "Product ≠ Sellable"; graduations claimed here and absent from product.md; one owner of a product's price versus many sellers; the kernel naming pluggables; Good/Service as a kernel flag; two copies of price-settlement; a kernel edge to the rule domain; this handoff's Status header ("Paused 2026-08-09") against decisions dated later.

## Assumptions
- **Weak-sellable criterion** ("capable of being sold") — stability: Weak; risk: content nodes pulled into product too eagerly; guard so far: edge rules only.
- **One flat product node can carry definition + spec + instance roles** (no split yet) — stability: Weak; the node may prove overloaded, forcing a Product-Definition split (see brand README question).

## Key Definitions Established
- Working base (Decided): dictionary *"an artifact that has been created by someone or some process"* — to be established as comprehensive and exclusive via the boundary suite, not replaced by a descriptive pseudo-definition. Artifact drift warning: the ecosystem's loose use of "artifact" is not the dictionary sense used here.

## Proposed Next Steps
1. Run the shared 10-case boundary suite with the estate side (see [`../../identity/estate/estate.handoff.md`](../../identity/estate/estate.handoff.md)) — cases 4, 5, 6, 10 are product-heavy.
2. Dedicated batch/traceability session (sub-batches, per-invoice identity, recall flows) — see [`../../modules-plugable/economics/batch/README.md`](../../../modules-plugable/economics/batch/README.md) questions.
3. Converge `README.md`'s priceability capability test with the asset-management reading into one core rationale. [Product Research 001](product.research.001.md#1-what-the-domain-is-for) proposes the converged reading: the test is admission to economic acts, price is a capability (owner question 1 above).
4. After the owner answers questions 1 to 3 above: rewrite the first paragraph of Definition in [product.md](product.md#definition-in-memar) and its Unresolved questions, and decide between the thin-product-plus-offer model and the classification-only model ([Product Research 001, rival models](product.research.001.md#3-rival-models)).
5. Apply the edge mapping ([Product Research 001, finding 5](product.research.001.md#5-how-the-existing-edge-folders-map)) edge by edge, one session per area, adding to each edge document the creator, remover, and trigger it lacks (the gaps are listed in finding 2): `price-settlement` with the batch copy first (a duplicate), then `type-flags` flag by flag, then `customable`, `sell-limit`, `buy-limit` to rule configuration.
6. Design the missing pieces the research sketches ([finding 6](product.research.001.md#6-missing-edges-and-modules)): `offer`, `pack` (check against `inventory`), `deposit` (check against `refund`), the batch-level actual composition, the product event target, and the `satisfies` edge on thing; each as its own handoff before any module folder exists.
7. Turn the test scenarios ([finding 7](product.research.001.md#7-test-scenarios)) into tests once questions 1 to 9 are answered; scenarios marked "kept" can be written now.
8. Reconcile the contradictions the research reports (the section above) by the owner's answers, recording each through the changelog; this handoff's Status header is stale (Paused 2026-08-09) and waits on the same decision.

## Related Artifacts
- [`product.research.001.md`](product.research.001.md) — what the domain is for, kernel and pluggable, rival models, edge mapping, missing modules, test scenarios, 14 owner questions (Review; unratified)
- [`README.md`](README.md) — graduated positions and open questions (Update when decisions change)
- [`../../../modules-plugable/economics/brand/edges/brand`](../../../modules-plugable/economics/brand/edges/brand/README.md) — brandless/definition products (Review)
- [`../../../modules-plugable/economics/batch/README.md`](../../../modules-plugable/economics/batch/README.md) — batch identity questions (Review)
- [`../../knowledge/content/edges-loop/course`](../../knowledge/content/edges-loop/course/README.md) — Product∩Content case (None)
- [`../../identity/estate/estate.handoff.md`](../../identity/estate/estate.handoff.md) — the co-developed other side

## Notes
- The source conversation (2026-08-05..09) is retired; everything durable graduated here or into the artifacts above.

## Khayyam conversion (2026-10-03)

Converted: `protocol/dt-uuid.kh` (`Field_ProductID` → `ProductID`, `Field_ProductsID` → `ProductsID`, both valued as `ThingUUID` / `Array_ThingUUID` imported from `identity/thing`) and `protocol/model.kh` (`ProductModel ab { ThingModel }`). Both return `accept` from the Khayyam frontend.

The Go's `type UUID record_p.UUID` was not carried over as a local `ProductUUID ab`: the established shape (rule, module, taxon, estate, text, label) imports `ThingUUID` instead, and rule 6 forbids the empty abstraction the Go's type would become. Nothing in the tree imported `product_p.UUID` from a Khayyam file, so nothing breaks.

### `edges/product.kh` — the type-flag space: left unconverted, deliberately

The brief for this pass asked what the code actually contains and whether the flag space is data or a type surface. What it contains:

- The file declares `package label` and sits loose in `edges/` — not inside any of the seven edge folders, not under `protocol/`. Nothing else in `product/edges/` is a `.kh`.
- One field surface, `Field_Type` with accessor `ProductType()` (the method name does not match the `Field_*` convention the rest of the repository uses).
- One value type, `Type uint64`.
- One constant, `Type_Unset Type = 0`.
- Three `const` groups of bit flags — 11 "common", 4 "good", 15 "service" — written as `Type_Good Type = (1 << iota)` and continued across the later groups, so every constant is a distinct bit position in a single 64-bit word.

**My reading: this is a flag-space on one record field, and it is closer to data than to a type surface — but unlike a pure label list it is a judgment call, not a formality.**

Why it differs from the unconverted label folders (`identity/organization/edges/`, the rights label folders, `taxon/edges/sexuality/data/`): those hold bare edge-label constants that name relations. These hold bit positions that *classify one node*. A flag is not a relation of its own — `(product)-[:Type_NeedApprove]->` names nothing — so it is not an edge vocabulary in the sense those folders are, and it is not a `Field_*` accessor that a generated body can return either, because a `uint64` of unnamed bits answers no question on its own.

Why I still did not convert it: converting it means declaring the flag space as an abstraction, and the flag space is an empty `ab` — rule 6 says design it before conversion, not translate it. Concretely, the design is not decided:

- The migration map's open item — "one parent/child edge, or distinct relations?" across `variant` / `optional` / `material` / `supplier`, and "Optional is a status on a relation, or its own edge?" — is exactly the question of what a flag *is*. Until it is answered, `Type_Good`, `Type_NeedApprove`, `Type_Provider_Role` and their siblings cannot be said to be flags-on-the-record, statuses-on-a-relation, or relations of their own, and the vocabulary's owner cannot be named.
- [type-flags.md](edges/type-flags/type-flags.md) settles where the *space* sits ("Flags stay with the product record they flag") but not what the flags *are*: its own Open questions ask whether Good/Service is a flag pair or two identity lenses, whether SellLimit flags belong to product or to the rule domain, and whether the kernel set is closed.
- The seven edge documents each take a slice of the same constant list by meaning (`buy-limit` takes PreSale, `sell-limit` takes the SellLimit_* trio, `provider` takes Provider_Staff/Provider_Role, `coordinate` says the InvoiceID lookup recipe riding `Type_Transport` is to be stripped). A flag list that seven documents partition by meaning is not yet one vocabulary with one owner.

What behavior is missing, stated as rule 6 asks: nothing in the Go says whether a flag may be set, by whom, when it is cleared, or how a set flag relates to the edge it names. The record needs at minimum "does this product carry flag X" and "which flags does this product carry" as *named* queries over an enumerated set, and the enumeration has to be decided before those queries can be written.

So the file stays as its Go clue block. When the open item above is answered, the shape to write is one flag-space type owned by the product record plus named predicates over it, and the per-edge slices move with their owners.

### Also unconverted

- **`edges/price/protocol/data_model.kh` and `storage.kh` — blocked on the money module.** `Price() fmp.Amount` and `minPrice, maxPrice fmp.Amount` need a money amount type that no `.kh` in the tree declares, and the path they name does not exist. Two separate problems, both outside this domain:
  1. `data_model.kh` imports `modules/fields/money/protocol` — a path this repository has never had. `storage.kh` and 24 other files import `modules/economics/money/protocol`, which also does not exist: the module lives at `modules-plugable/economics/money/`, and [money.md](../../../modules-plugable/economics/money/money.md) places it deliberately outside core. So the core price edge currently points at a core `money` that the org decided not to have. Whether `price` is a core edge at all is [product.md](product.md)'s first Unresolved question ("Are `price`/`pricing` kernel edges of product or rule-driven capabilities?") — the stale paths are evidence that this was answered "core" once and then answered "pluggable".
  2. `modules-plugable/economics/money/protocol/dt-money-amout.kh` is unconverted, so `Field_Amount` / `Amount` have no Khayyam declaration to import. It also needs its own decision first: [money.md](../../../modules-plugable/economics/money/money.md) lists "`int64` scaling vs `decimal_p.Quantity` used on bookkeeping fields — reconcile the two quantity representations" as unresolved, and `bookkeeping` already uses `Decimal_Quantity`. Until that is settled there is no correct return type for a price.
  Also note `storage.kh` names `fcp.UUID` (the count-unit currency label) without ever importing `currency_p` in that file.
- **`_import/product-auction/**`, `_import/product-cost/**`, `_import/product-price/**` (17 files)** — **old, non-architectural code**: `ds.DataStructure` descriptors with hand-written Syllab codecs and `index-hash` struct tags against `libgo/pehrest`/`libgo/ganjine`. The `price` protocol and the `product-price` `_import` describe the same record twice, once per storage engine. Disposition: delete or re-model, not convert.
- The remaining edge folders (`buyers`, `comment`, `coordinate`, `customable`, `material`, `optional`, `price-settlement`, `provider`, `qa`, `sell-limit`, `supplier`, `variant`, `buy-limit`, `type-flags`) hold documents only — no protocol sources in the tree.
