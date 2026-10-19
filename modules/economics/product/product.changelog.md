# Product Changelog

## Changelog

### Price edge rules and the pricing session's open questions
- Time: 2026-10-10T14:45:00Z
- Type: added
- Cited:
  - [Pricing → Decisions (2026-10-10)](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md#decisions-2026-10-10) - Reference: a price is derived from current stated prices, never from the historical cost of stock held
  - [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions) - Reference: where the price-ownership and display-basis questions are held
  - [Follow](../../identity/thing/edges/follow/follow.md#policies-rules) - Depends_on: the delivery a new price version triggers
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided the lessons
  - An AI agent via Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- [price](edges/price/price.md): Policies gained who creates the edge (only the organization that owns the product, from `protocol/data_model.kh`), that it is never overwritten or deleted but superseded by a new version kept per product and currency (`protocol/storage.kh`), and what a new version triggers (delivery to followers, re-evaluation of replacement cost where a source points at the product, recomputation of indices with it as a component). New Placement section: on product for now, not pricing, not the invoice item's price. New Open questions section: product or batch, which edge carries a rule-stated price, display basis and compound units, valid-until and staleness of a stated price.
- [price-settlement](edges/price-settlement/price-settlement.md), [variant](edges/variant/variant.md): an open question each on what changes if the price moves to the batch.
- [supplier](edges/supplier/supplier.md): an open question on one product across organizations and the follow its price implies.
- [material](edges/material/material.md): an open question on which material edge replacement cost reads for a made product.
- [buy-limit](edges/buy-limit/buy-limit.md): an open question on pre-sale risk under deferred payment.
- [product.md](product.md) Unresolved questions and [product.handoff.md](product.handoff.md) Open Questions: price ownership, product or batch.
- Nothing was removed or reworded.

### Product Research 001: what the domain is for, its kernel, and the owner's questions
- Time: 2026-10-16T00:40:00Z
- Type: added
- Cited:
  - [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md) - Evidence: the four-things reading of "price" and the scenarios the product research extends
  - [Modules → Placement](../../modules.md#placement) - Reference: the kernel and pluggable tests the research applies
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-15)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted

#### What changed
- [product.research.001.md](product.research.001.md) is added: eleven scenarios from several cultures and industries; a proposal that the domain's test is admission to economic acts and not priceability; a four-element kernel; five rival models with a recommendation (unratified); a mapping of all fifteen edge folders; nine missing pieces sketched; twenty-two test scenarios; and fourteen owner questions with defaults. Nine contradictions between the domain's documents are reported, not resolved.
- [product.handoff.md](product.handoff.md) gains the fourteen questions with their defaults and what each blocks, five Next Steps, a pointer to the contradictions, and the research in Related Artifacts.
- Nothing in [product.md](product.md), in any edge document, or in any `.kh` file was changed; nothing was moved or deleted.
