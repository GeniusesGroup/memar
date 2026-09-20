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
