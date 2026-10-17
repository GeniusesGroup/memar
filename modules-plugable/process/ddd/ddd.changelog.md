# Domain-Driven Design Changelog

## Changelog

### Initial draft deepened — phrase/acronym split, *driven*, conformance, canopy critique
- Time: 2026-09-16T15:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — requested; clarified stance (three ordinary words; filesystem parallel; not Evans endorsement; no DDD state in documentation.handoff)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5 via [Cursor](../../../../CONTRIBUTORS.md#cursor)) — claimed, argued (Terminology Business-Term consumption; *driven* via Concept-First; membership criterion; multiple-models / identity / stakeholder-vocabulary critiques; placement and obligation)
  - [ChatGPT](../../../../CONTRIBUTORS.md#chatgpt) (GPT-5.6-terra via [Cursor](../../../../CONTRIBUTORS.md#cursor)) — claimed, argued (conformance rule that earns protocol placement; mapping false-friends; soften undefined≠forbidden; fourth commitment overclaim)
  - Cursor/Composer — drafted, integrated

#### What changed
- Created `ddd.md` (Title: Domain-Driven Design) as Memar's position: phrase vs acronym (consumes Terminology's Business Term listing of DDD and OOP Warning parallel), *driven* defined via Concept-First / Tool-First and five competing drivers, conformance rule when the name is invoked (justify implementation from the current model; revise the model explicitly or reject the commitment), membership criterion for the four gathered commitments, deepened canopy critique (aggregate-root, data-identity criterion, multiple models, stakeholder vocabulary, intrinsic labels, mechanism catalogs), mapping table split into correspondence / refusal / absence with false-friend corrections, Scope derived from *domain* as unreferenced general meaning.
- Stance patterned on filesystem; filesystem parallel stated as method, not identical membership rationale. No practice companion in v1.
- Created paired handoff and this changelog. No entry in `documentation.handoff.md` (owner: that file is documentation-method only).

#### Considered and not done
- **Banning the name or treating the document as Evans endorsement (rejected)**: three ordinary words; presence ≠ blue-book endorsement. (Omid Hekayati.)
- **Parking open state in documentation.handoff (rejected)**: documentation method only. (Omid Hekayati.)
- **Inventing homes for bounded context, domain service, repository, factory, strategic/tactical (rejected)**: absence reported. (Both critiques.)
- **Equating Memar concepts with circulated canopy terms in the mapping table (rejected)**: table now marks partial / refusal / not-a-mapping. (GPT-5.6-terra.)
- **A ddd.practice.md in v1 (rejected)**: compose existing practices; extract only if label-substitution outgrows a paragraph. (Both critiques.)

#### Deliberation
- First-round sub-agent briefs were over-capped; a second full-depth round (Claude Opus-5, GPT-5.6-terra) supplied the Terminology consumption, *driven* definition, conformance rule, and mapping corrections integrated here (Cursor/Composer — ran; owner — asked for the deeper pass).

---

### Bounded context: no Definition, and no coinage in live prose
- Time: 2026-10-04T21:26:49Z
- Type: Clarified
- Propagates to:
  - [type.md](../../../type.md): Done — both load-bearing sentences in *Type Identity* now read "within a context"; no claim changed.
- Contributors:
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The **Bounded context.** row under *Mapping: Circulated Terms and Memar Homes* now states why the absence is not settled by default: the word is a Business-layer coinage, which [Terminology → The Default Meaning of an Unreferenced Term](../../../terminology.md#the-default-meaning-of-an-unreferenced-term) excludes from the ordinary meaning it would otherwise carry, so the term is neither governed nor safely unresolved. Memar prose states the region in ordinary words, as *Type Identity* already does, and what Memar holds about multiple models of one reality stays where the Canopy critique states it.
- `type.md` → *Type Identity*: the two sentences that scoped nominal identity now read "within a context" and "in the same context". No claim changes — that section's closing sentence and its *Contextual scoping* paragraph already state the rule in the ordinary word.
- `ddd.handoff.md` no longer carries the entry "Bounded context in live Memar prose", nor the Anticipated Work bullet that anticipated retargeting the row once the term was defined or replaced.

#### Considered and not done
- **Defining Bounded context in Memar (rejected)**: this document already records no Memar Definition, and taking the word would settle by definition a design space [Modeling](../../../modeling.md) has not finished exploring.
- **Substituting Scope or Conceptual Boundaries for the coinage (rejected)**: neither is this term, and both are realization-level boundaries; naming one inside a model-level sentence narrows the claim rather than stating it.

---

### Conformance rule restated as a naming the model supplies rather than an adequacy a party judges
- Time: 2026-10-05T17:24:41Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The opening sentence of [What This Protocol Governs](./ddd.md#what-this-protocol-governs) no longer makes conformance turn on an implementation commitment being "explained from that current model." Conformance is now that each commitment either names the model concern it realizes or is returned to modeling as a candidate that may revise it.
- The paragraph gains one sentence saying that whether such a naming is adequate is not this protocol's question and that where two readings of the model disagree, the disagreement is the finding.
- The following sentence's test is now "cannot be traced to the model" rather than "conflicts with, or cannot be explained by, the model", so that it matches the rule above it.

#### Deliberation
- The edit was proposed in this session's earlier read-only sweep of `docs/` against the ruling and applied once it landed here. The sweep's reasoning is the record's: a document that places itself in `protocols/` and states a conformance rule no procedure can settle is a document the ruling excludes, and the sentence was that exclusion in this document's own words (Space Bunny Alpha).
- What the replacement does not claim is that adequacy of an explanation became mechanical. It moved the sufficiency question out of the conformance rule and into the finding, leaving the discipline of the four gathered commitments untouched (Space Bunny Alpha).

#### Considered and not done
- **Rewriting the four gathered commitments as checkable requirements (rejected)**: the document gathers commitments from Modeling and Terminology rather than restating them, and restating them as requirements here would duplicate rules those documents own and would put this document in the business of deciding whether a model is good — the judgment it exists to keep out.
- **Removing the conformance topic and demoting the document out of `protocols/` (rejected)**: the placement question is open in `ddd.handoff.md` and is not this entry's to decide; the conformance rule was made decidable instead, which is what the folder membership criterion now asks for.

---

### Moved to `docs/modules/lib/process/`, and the folder-membership question closed
- Time: 2026-10-07T14:07:33Z
- Type: Moved
- Cited:
  - [Lib → Membership criterion](../README.md#membership-criterion) - Premise: `docs/protocols/` became `docs/modules/`, and positions on surfaces whose authority is outside Memar are gathered under `lib/`.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) — drafted, applied

#### What changed
- The document, this changelog, and its handoff moved from `docs/protocols/` to `docs/modules/lib/process/`; every relative link was re-derived for the new depth.
- [Memar's Stance on the Name](./ddd.md#memars-stance-on-the-name): the paragraph that placed the document now names `lib/`, the authority test that places it there, that it has no realization under `modules/lib/`, and that it sits under `process/` because its governed subject is development as a process.
- `ddd.handoff.md` no longer carries "Protocols folder membership criterion": the [lib criterion](../README.md#membership-criterion) admits a circulated design name by name, so whether such rules ride under "a rule set any language or stack can realize" is no longer the question that places this document.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:47:00Z
- Type: Changed
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to `ddd.md`, `ddd.handoff.md`, and this changelog against HEAD: the relative links re-derived for the move to `docs/modules/lib/process/`, the placement paragraph of *Memar's Stance on the Name*, the restated conformance rule in *What This Protocol Governs*, the *Bounded context* row's added reasoning, and the three entries above with the two handoff questions they close. The links resolve (`memar content check`); each removed handoff entry and the removed Anticipated Work bullet is recorded in the entry that closes it; the conformance rewording matches its entry; the *Type Identity* edit the *Bounded context* entry names is in `type.md`, outside this review.
- `ddd.md` → *Methodology*: "per this folder's citation rule" named a rule that lived in the former `protocols/README.md` and is not in `lib/README.md`; it now points to the citation direction in [Modules](../../README.md), which states it.

#### Considered and not done
- **Rewording "Business-layer coinage" in the *Bounded context* row (not done)**: Terminology classifies the acronym DDD as a Business Term but does not list *bounded context* itself, so the layer is this document's inference from the canopy; it is stated as that inference and the conclusion (state the region in ordinary words) does not depend on it.
