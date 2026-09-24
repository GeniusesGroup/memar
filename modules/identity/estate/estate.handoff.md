# Estate Handoff

## Topic & Purpose
Modeling the Estate concept: what it covers, what it must never absorb, and its boundary with Product. Triggered by the territorial-rules use-case (density/occupancy/green-space/certificates as replaceable policies over shared base concepts, instead of jurisdiction-specific bureaucracy). Co-developed with the Product boundary discussion.

## Status
Paused (2026-08-09) — deliberately resumed-later; definition work intentionally not started.

## Decisions
All Decided items are graduated into [`README.md`](README.md) ("Positions confirmed in discussion") — land/building as two estates, observations-over-relations, immutable identity, multi-typing, runtime qualification, domain exclusions. Do not restate them here.

Additional Tentative design insights (not yet governing any module; graduates when a territorial-policy design starts):
- **Metric-choice principle** (Tentative): a word naming several quantities (e.g. "density" = FAR / population / unit / built-volume / economic density) is a badly defined concept; a rule on an ambiguous metric misleads regardless of execution. Evidence: 1000% building density with 1/10 the human density of a 300% district.
- **Outcome-over-method principle** (Tentative): rules should constrain outcomes (`OpenSpace >= 80%` for everyone) rather than approval processes — trivially verifiable, no permission machinery. Corrected caveat (Explored-but-unresolved): action still occurs with rule-checking by an intermediary organization (ISO-style conformity assessment); Approval ≠ Certification — a certificate is a trusted conformance claim, not a permission to act.
- **Certificate non-monopoly** (Tentative): "completion certificate" is one of many certificate types (food-safety, air quality, accessibility, energy efficiency); structure = issuer, scope, trust, evidence, validity; the municipality is one issuer of thousands.
- **Justification chains** (Tentative): a rule's number must be derivable from goals (green space per capita, permeability, ventilation, biodiversity, infrastructure cost) — a law is not just a number. Test case: Omid's draft constitution article 12.

## Ambiguities Resolved
- "Approval before action" vs "action + rule-check" — resolved: the two models were conflated in a linear example; the corrected model has action accompanied by rule-checking and independent assessment (certification), not pre-approval. Resolved by Omid's ISO analogy.
- Economics as Estate's category home — resolved: rejected after review under Omid's own economics definition (optimal allocation of scarce resources); the allocation rationale motivates *modeling* an estate, not the concept's *essence*. Placement now open between Identity and Management.

## Open Questions
Full map with canonical homes lives in [`README.md`](README.md). The blocking ones for definition work:
- Identity-continuity criterion (wall-moving case; who changed it) — **blocks** the definition.
- What makes a Thing *take* the Estate identity (waterfall case: is an unmodeled waterfall an estate?) — **blocks**.
- Spatial relations: first-class edges or derived observations — **blocks** edge design (see [`edges/estate`](edges/estate/README.md)).
- Virtual-estate hypothesis and movable-objects question — inform but do not block.

## Assumptions
- **Estate may be virtual** (an estate that never becomes physically real) — stability: Weak; Omid explicitly flagged "maybe this assumption is wrong". If it falls, physical realization enters the definition.
- **"Capable of being represented as a physical environment/entity" is the estate criterion** — stability: Weak (toward agreement, not final).
- **Lineage edges (`derived_from`, `forked_from`, `realized_from`) belong to `thing`, not estate** — stability: Unexamined.

## Key Definitions Established
None — deliberately. The definition is expected to emerge from the boundary-case suite, not be imposed (vocabulary discipline: definition precedes term, but here even the definition waits for the model). Rename guard is weak: the name is good enough for now, not defended to the death.

## Proposed Next Steps
1. Run the 10-case boundary suite (land, building, room, furniture, electrical switch, museum, waterfall, virtual building, design-realized building, service product), producing the graph for each; per-case starting homes are annotated in [`README.md`](README.md) / `topic` history — cases 3 (room) may need a new `type-room`.
2. Only after the suite converges: draft the Estate definition (comprehensive and exclusive, dictionary-anchored).
3. Extract the Certificate concept (issuer/scope/trust/evidence/validity) as its own design.
4. Prototype the territorial-policy module (article-12-style outcome rules) as the first optional estate policy.

## Related Artifacts
- [`README.md`](README.md) — graduated positions (Update when decisions change)
- [`edges/estate`](edges/estate/README.md), [`edges/neighborhood`](edges/neighborhood/README.md), [`edges/type-building`](edges/type-building/README.md) — edge-level questions (Review during suite)
- [`../../identity/object/edges/movable`](../object/edges/movable/README.md) — movable-vs-estate rule conflict (Update during suite)
- [`../../economics/product/product.handoff.md`](../../economics/product/product.handoff.md) — co-developed Product boundary
- [`../../rights/law/README.md`](../../rights/law/README.md) — territorial rules / founding law side

## Notes
- The source conversation (2026-08-05..09) is retired; everything durable graduated here or into the artifacts above.
- A missing `type-room` edge was noticed while annotating the suite (case 3).
