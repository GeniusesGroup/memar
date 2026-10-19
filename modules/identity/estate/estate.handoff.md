# Estate Handoff

## Topic & Purpose
Modeling the Estate concept: what it covers, what it must never absorb, and its boundary with Product. Triggered by the territorial-rules use-case (density/occupancy/green-space/certificates as replaceable policies over shared base concepts, instead of jurisdiction-specific bureaucracy). Co-developed with the Product boundary discussion.

## Status
Paused (2026-08-09) — definition work deliberately resumed-later. The protocol layer was converted to Khayyam on 2026-10-03; that pass is recorded under Decisions below and adds no claim about the definition.

## Decisions
All Decided items are graduated into [`README.md`](README.md) ("Positions confirmed in discussion") — land/building as two estates, observations-over-relations, immutable identity, multi-typing, runtime qualification, domain exclusions. Do not restate them here.

Additional Tentative design insights (not yet governing any module; graduates when a territorial-policy design starts):
- **Metric-choice principle** (Tentative): a word naming several quantities (e.g. "density" = FAR / population / unit / built-volume / economic density) is a badly defined concept; a rule on an ambiguous metric misleads regardless of execution. Evidence: 1000% building density with 1/10 the human density of a 300% district.
- **Outcome-over-method principle** (Tentative): rules should constrain outcomes (`OpenSpace >= 80%` for everyone) rather than approval processes — trivially verifiable, no permission machinery. Corrected caveat (Explored-but-unresolved): action still occurs with rule-checking by an intermediary organization (ISO-style conformity assessment); Approval ≠ Certification — a certificate is a trusted conformance claim, not a permission to act.
- **Certificate non-monopoly** (Tentative): "completion certificate" is one of many certificate types (food-safety, air quality, accessibility, energy efficiency); structure = issuer, scope, trust, evidence, validity; the municipality is one issuer of thousands.
- **Justification chains** (Tentative): a rule's number must be derivable from goals (green space per capita, permeability, ventilation, biodiversity, infrastructure cost) — a law is not just a number. Test case: Omid's draft constitution article 12.

### Phase 2 protocol conversion (2026-10-03)

- **`EstateModel` composes `ThingModel` only (Decided).** Go embedded `thing_p.Model` and `product_p.Model`, but `product_p.Model` is itself only `thing_p.Model`, so the second embedding adds no requirement; `modules/economics/product/protocol/model.kh` is not converted, so no `ProductModel` exists to import and declaring one here would be this domain claiming another domain's concept. - reason: an abstraction states requirements, and a requirement already implied by a composed requirement is not restated.
- **`Field_EstateID` / `EstateID` and `Field_EstateIDs` / `EstateIDs`, both over `ThingUUID` (Decided).** Go declared a local `type UUID record_p.UUID`; the ~90 per-domain `UUID` declarations are one concept owned by the thing domain. The plural keeps the Go's own spelling (`Field_EstateIDs` + `EstateIDs`) rather than the `ThingsIDs` shape of the thing domain — reason: `Field_X` + `X` is the convention, and the Go already wrote `X` as `EstateIDs`.
- **`Field_WarehouseID` / `WarehouseID` over `ThingUUID` (Decided).** `warehouse_p.UUID` was `estate_p.UUID`, so a warehouse is identified by the estate's own identifier, not by one of its own. The warehouse is a classification the estate loop-edge attaches, not a second identity.
- **`Array_ThingUUID` imported, not redeclared (Decided).** `knowledge/label/protocol/dt-uuid.kh` declares its own copy of that same abstraction; estate does not repeat the mistake. - reason: qualified-names rule, one concept one owner.
- **No `cp` under `protocol/` (Decided).** The three converted files are abstractions and body-less contract methods only; the estate's identity and version semantics are still undefined, so there is nothing to implement yet.

## Ambiguities Resolved
- "Approval before action" vs "action + rule-check" — resolved: the two models were conflated in a linear example; the corrected model has action accompanied by rule-checking and independent assessment (certification), not pre-approval. Resolved by Omid's ISO analogy.
- Economics as Estate's category home — resolved: rejected after review under Omid's own economics definition (optimal allocation of scarce resources); the allocation rationale motivates *modeling* an estate, not the concept's *essence*. Placement now open between Identity and Management.

## Open Questions
Full map with canonical homes lives in [`README.md`](README.md). The blocking ones for definition work:
- Identity-continuity criterion (wall-moving case; who changed it) — **blocks** the definition.
- What makes a Thing *take* the Estate identity (waterfall case: is an unmodeled waterfall an estate?) — **blocks**.
- Spatial relations: first-class edges or derived observations — **blocks** edge design (see [`edges/estate`](edges/estate/README.md)).
- Virtual-estate hypothesis and movable-objects question — inform but do not block.
- **Whether the `type-*` loop-edges belong under `edges-loop/` at all (Explored-but-unresolved).** Twenty-eight `type-*` folders sit under `edges-loop/`, each a loop-edge with only a Markdown model and, for `type-warehouse` alone, a protocol folder. Only `type-warehouse` carried declarations, so only it converted. Whether a warehouse (or any `type-*`) is a *classification the estate loop attaches* — which is what the folder name asserts — or a *sub-type the estate model composes* is not stated anywhere; the Go supports the reading, since `warehouse_p.UUID` was `estate_p.UUID`. Nothing in the domain document settles it, and the estate definition itself is still open, so the folder placement cannot be settled before the definition.
- **The stale `physical_model` edge reference (Explored-but-unresolved).** The Go comment on the estate UUID said to "use `physical_model` edge to store and show as map". No such edge exists; the nearest is `object/edges/model-physical`, and `README.md` places coordinates and physical modelling outside this domain. Whether the comment meant `object/edges/model-physical` or a graph-rendering concern nobody modeled is open. Its settled half — that a physical location is reached through edges outside estate — is already graduated into `README.md`'s domain exclusions.
- **Whether `WarehouseID` should exist at all (Deferred).** If the warehouse turns out to be a plain classification label rather than an identified estate, the accessor is the label domain's business and this file goes away. It waits on the placement question above.

## Assumptions
- **`EstateModel` gains requirements once the definition lands (Strong).** It currently carries only `ThingModel`, which is what the Go said; the definition work above is what would fill it in. Rule 6 (an empty abstraction is a design smell) is satisfied here only in the weak sense that `EstateModel` is not empty — what it requires beyond `ThingModel` is genuinely not yet decided, and that is the same blocking question the definition carries, not a gap the conversion introduced.
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

## Research 001 questions and next steps (2026-10-18)

### Status
Proposals only, from [estate.research.001.md](estate.research.001.md) (eleven place scenarios, seven for person and six for taxon, a five-element kernel, six rival-model choices, a mapping of every folder, 28 test scenarios and a replay of the ten-case boundary suite, a reconciliation with the thing, user, organization and group researches, and the identity-through-change scenarios). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. The Decided positions in [estate.md](estate.md) are untouched. The definition sentence, the Model and Policies sections, every `.kh` and every folder are unchanged.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](estate.research.001.md#8-open-questions). Ordered by what they change.

1. **ES.1 — Which facts of an estate are identity-bearing, so that "any change produces a new estate" has a range?** Default: declared extent and composition; use, occupancy, ownership, name, address, status and condition are not. Blocks: the definition, the wall-moving case, `supersedes` policy text, every `Field_EstateID` consumer.
2. **ES.2 — Does each reference to an estate carry a mode (pinned or following) set by its owning domain and recorded as a successor rule in the succession event?** Default: yes; pointers follow, obligations are recorded with the event, evidence of a past state is pinned. Blocks: voucher, inventory, discount, address, task site, department office, staff attendance; thing's `supersedes`; content's quoting.
3. **ES.3 — What makes a thing take the estate identity?** Default: the declaration of an organization (admission), no hard exclusion; `movable` becomes one organization's default. Blocks: the definition, the waterfall case, the `movable` document.
4. **ES.4 — Are spatial relations stored or derived?** Default: by source; an authority's `within` assertion wins over geometry and a discrepancy is recorded; adjacency and neighborhood are discovered. Blocks: `edges/estate`, `part`, `neighborhood`.
5. **ES.5 — May a succession be many-to-many with shares?** Default: yes. Blocks: parcel division and merger, mortgages.
6. **ES.6 — Where do the person-to-place relations live?** Default: one `situated_at` record on the estate side with role vocabulary, each consumer keeping its rules; `born_in`, `live_in`, `work_in` retired as filed. Blocks: the three edges, the survey's Q2, six consumers' place pointers.
7. **ES.7 — Are the 26 `type-*` loops a property of estate or classifications declared by an organization in five families?** Default: the latter; a folder only where processing exists (warehouse). Blocks: 26 folders, `WarehouseID`, `type-warehouse/edges/product`.
8. **ES.8 — Is the definition sentence (a housing estate) replaced by one drawn from the positions, and is the name kept?** Default: replace, keep the name provisionally. Blocks: estate.md wording only.
9. **ES.9 — Are Occupied and Vacant discovered, and Reserved and Closed acquired?** Default: yes. Blocks: the `estate-status` move.
10. **ES.10 — When two organizations declare different extents, who governs?** Default: each is authoritative for what it states; one global identity; a discrepancy is recorded. Blocks: cross-organization follow, territorial policy.
11. **ES.11 — Is a virtual or unbuilt place an estate, physical Earth being one frame among others?** Default: yes, admitted by the declarer of the frame. Blocks: the definition criterion.
12. **ES.12 — What does `EstateModel` require beyond `ThingModel`?** Default: the declared extent as a reference, held until ES.1. Blocks: `protocol/model.kh`.
13. **ES.13 — Is a persistent place concept a separate layer?** Default: no, an ordinary thing with a seat role. Blocks: heritage and pilgrimage cases only.

Questions for the two neighbours (PS.1 to PS.7 for person, TN.1 to TN.6 for taxon) are in the research and pointed to from their handoffs.

### Contradictions found (reported, not resolved)
The definition sentence against the positions (ES-C1); three edges that point from a place to a group of organisms (ES-C2); the README that is said to hold the positions and holds only `estate.md` (ES-C3); 28 `type-*` folders named, 26 on disk (ES-C4); and the known contradiction of a new estate per change against persistent identity in text, content, group and organization, read in the research as a question of which facts are identity-bearing and which references follow a succession.

### Proposed Next Steps (research)
1. Owner rules on ES.1, ES.2 and ES.3; they decide most of the other answers and the definition.
2. Run the boundary suite as a graph per case; the research replays it as a table (finding 7) and answers the `type-room` remark: no new folder.
3. Draft the estate definition from the positions and ES.1, then replace the housing-estate sentence (ES.8).
4. Prototype `territorial-policy` as the first optional estate pluggable (the earlier Next Step 4), after the rule domain defines `condition_is`.
5. Define `situated_at` and retire the three person-like edges, after ES.6 and the survey's Q2 are reconciled.
6. Extract the certificate concept as its own cross-domain design (the earlier Next Step 3).
7. Apply the survey's estate tasks (links, the stale 28, `type-*` Placement) once ES.7 is answered.

## Related Artifacts
- [`estate.research.001.md`](estate.research.001.md) — the research behind the section above (Update when the owner answers)



- [`README.md`](README.md) — graduated positions (Update when decisions change)
- [`edges/estate`](edges/estate/README.md), [`edges/neighborhood`](edges/neighborhood/README.md), [`edges-loop/type-building`](edges-loop/type-building/README.md) — edge-level questions (Review during suite)
- [`../../identity/object/edges-loop/movable`](../object/edges-loop/movable/README.md) — movable-vs-estate rule conflict (Update during suite)
- [`../../economics/product/product.handoff.md`](../../economics/product/product.handoff.md) — co-developed Product boundary
- [`../../rights/law/README.md`](../../rights/law/README.md) — territorial rules / founding law side

## Notes
- The source conversation (2026-08-05..09) is retired; everything durable graduated here or into the artifacts above.
- A missing `type-room` edge was noticed while annotating the suite (case 3).
- 2026-10-03: three `.kh` files converted (`protocol/dt-uuid.kh`, `protocol/model.kh`, `edges-loop/type-warehouse/protocol/dt-uuid.kh`); all three `accept` from the Khayyam frontend (`frontend_check.ts`) against a resolved root. No Go clue block was touched. Nothing outside `modules/identity/estate` was edited; `git` was not run.
- 2026-10-03: `edges-loop/type-warehouse/edges/product/product.md` holds no declarations, so the warehouse loop's product endpoint converted to nothing. Its `ManagerDecision` / `AllowedToEnter` labels remain bare labels with no who-may-set semantics, which its own document rules are not ratified.
