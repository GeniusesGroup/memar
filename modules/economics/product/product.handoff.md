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

## Assumptions
- **Weak-sellable criterion** ("capable of being sold") — stability: Weak; risk: content nodes pulled into product too eagerly; guard so far: edge rules only.
- **One flat product node can carry definition + spec + instance roles** (no split yet) — stability: Weak; the node may prove overloaded, forcing a Product-Definition split (see brand README question).

## Key Definitions Established
- Working base (Decided): dictionary *"an artifact that has been created by someone or some process"* — to be established as comprehensive and exclusive via the boundary suite, not replaced by a descriptive pseudo-definition. Artifact drift warning: the ecosystem's loose use of "artifact" is not the dictionary sense used here.

## Proposed Next Steps
1. Run the shared 10-case boundary suite with the estate side (see [`../../identity/estate/estate.handoff.md`](../../identity/estate/estate.handoff.md)) — cases 4, 5, 6, 10 are product-heavy.
2. Dedicated batch/traceability session (sub-batches, per-invoice identity, recall flows) — see [`../../modules-plugable/economics/batch/README.md`](../../../modules-plugable/economics/batch/README.md) questions.
3. Converge `README.md`'s priceability capability test with the asset-management reading into one core rationale.

## Related Artifacts
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
  1. `data_model.kh` imports `org/modules/fields/money/protocol` — a path this repository has never had. `storage.kh` and 24 other files import `org/modules/economics/money/protocol`, which also does not exist: the module lives at `modules-plugable/economics/money/`, and [money.md](../../../modules-plugable/economics/money/money.md) places it deliberately outside core. So the core price edge currently points at a core `money` that the org decided not to have. Whether `price` is a core edge at all is [product.md](product.md)'s first Unresolved question ("Are `price`/`pricing` kernel edges of product or rule-driven capabilities?") — the stale paths are evidence that this was answered "core" once and then answered "pluggable".
  2. `modules-plugable/economics/money/protocol/dt-money-amout.kh` is unconverted, so `Field_Amount` / `Amount` have no Khayyam declaration to import. It also needs its own decision first: [money.md](../../../modules-plugable/economics/money/money.md) lists "`int64` scaling vs `decimal_p.Quantity` used on bookkeeping fields — reconcile the two quantity representations" as unresolved, and `bookkeeping` already uses `Decimal_Quantity`. Until that is settled there is no correct return type for a price.
  Also note `storage.kh` names `fcp.UUID` (the count-unit currency label) without ever importing `currency_p` in that file.
- **`_import/product-auction/**`, `_import/product-cost/**`, `_import/product-price/**` (17 files)** — **old, non-architectural code**: `ds.DataStructure` descriptors with hand-written Syllab codecs and `index-hash` struct tags against `libgo/pehrest`/`libgo/ganjine`. The `price` protocol and the `product-price` `_import` describe the same record twice, once per storage engine. Disposition: delete or re-model, not convert.
- The remaining edge folders (`buyers`, `comment`, `coordinate`, `customable`, `material`, `optional`, `price-settlement`, `provider`, `qa`, `sell-limit`, `supplier`, `variant`, `buy-limit`, `type-flags`) hold documents only — no protocol sources in the tree.
