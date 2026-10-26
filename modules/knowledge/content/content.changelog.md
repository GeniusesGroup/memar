# Content Changelog

## Changelog

### Initial revision
- Time: 2026-07-27T00:00:00Z
- Type: Added
- Cited:
  - [Documentation — Explanation](../../../modules-plugable/knowledge/documentation/explanation/explanation.md) — Depends_on: this document follows the Explanation facet structure (Abstract, Introduction, Explanation, Results, Discussion).
  - [Modeling](../../../docs/modeling.md) — Depends_on: builds on foundational principles — Behavior Before Structure, Code vs Rule, graph-based conceptual modeling, Discovery Before Design.
  - [Terminology](../../../docs/terminology.md) — Depends_on: definitions in this document must not contradict established project terminology conventions.
  - [HTML5 Specification](https://html.spec.whatwg.org/) — Reference: observational corpus for discovery — one of several existing languages studied, not an architectural authority.
  - [ARIA Specification](https://www.w3.org/TR/wai-aria/) — Reference: observational corpus — demonstrates gaps HTML alone does not cover, particularly around state and role semantics.
  - Related Work Survey (AI-generated research; source file deleted 2026-09-23 after its final transfer audit) — Reference: background survey of prior art (RDF, RDFa, JSON-LD, Topic Maps, XForms, etc.). Treat as exploratory research, not architectural authority — see [Documentation — Research → Relationship to the Other Facets](../../../modules-plugable/knowledge/documentation/research/research.md#relationship-to-the-other-facets) for the distinction between research findings and adopted understanding.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, reviewed: original concept formulation; 10+ years of iterative idea development; Design Languages project (prior art/prototype); critical review and direction-setting across all discovery sessions.
  - [Claude](../../../CONTRIBUTORS.md#claude) (claude-sonnet-5) — argued, rewrote: process critique; Concept/Implementation boundary analysis; Composition vs Aggregate distinction; Addressability and Reference-as-edge critique; document synthesis.
  - [ChatGPT](../../../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — claimed, argued: early Semantic Interface Architecture framing; Reference-as-edge discovery; Lexical Token vs Sense proposal; Authoring Model vs Syntax distinction.
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM 5.0V) — drafted: Related Work Survey and HTML/ARIA element analysis (research, not authoritative).

#### Summary
First revision of this document: a single layered Explanation-facet document defining Content as a conceptual model, covering the concerns discovered across a decade of iterative development and multiple discovery sessions — Semantic (definition and scope), Reference-as-relation, Lexical Token vs. Sense, Addressability, Composition (Aggregate vs. Presentation), Layout, Theme, Event, Type Reference, multi-instance/runtime identity, the Authoring Syntax vs. Semantic Graph split, "Khayyam-manner" language criteria, and the open case of structural notation within an Authoring Syntax itself.

The document's scope and framing changed substantially across the discovery process that produced it; that evolution is recorded here so a future reader is not confused by any apparent contradiction between earlier working assumptions (visible in prior chat logs and interim drafts) and the final structure:

1. **From a CSS-avoidance idea to a full Content model.** The originating idea (write semantic HTML, let a Design Language render it) was narrow and GUI-centric. Discovery broadened it first to include non-GUI modalities (VUI, CLI, Braille), then to question whether HTML itself was an appropriate foundation at all, and ultimately to a model independent of any specific markup language.
2. **From "extend HTML" to "HTML as corpus, not authority."** Early research catalogued HTML/ARIA elements looking for gaps to patch. This was explicitly abandoned as a *starting point* — though the research itself remains valuable as observational evidence — once it became clear that cataloguing existing tags anchors thinking to HTML's own historical accidents.
3. **From a two-file structure (`semantic.md` + `semantic-catalog.md`) to a single layered document (`content.md`).** An interim proposal to keep principles and a raw discovery catalog in two separate files was reconsidered and reversed: the catalog was kept outside this document as exploratory, non-authoritative material, while this document itself was widened — not narrowed — into a single document covering Content's full set of discovered concerns at a layered level of abstraction, rather than being split across multiple interdependent architecture files.
4. **A scope-narrowing decision was made, then explicitly reversed.** At one point during discovery, the working conclusion was that this document's scope should be limited strictly to unstructured-content semantics (Reference, Token/Sense, Addressability), with Composition, Layout, Theme, and Event entirely out of scope — on the grounds that those concerns belonged to Khayyam. This narrowing was later explicitly rejected: silence about a real, related concern is not architecturally neutral, and a future reader encountering these concerns with no guidance here would default to unexamined ecosystem assumptions. The final structure instead defines *what each concern means* here, while consistently delegating *how it is mechanically implemented* to host languages and consumer projects — the "Concept vs. Implementation Mechanism" split formalized in Foundational Principles and applied throughout.
5. **From "Domain Aggregate" language to concern-agnostic terminology.** The word "Domain," borrowed early from DDD-adjacent thinking, was deliberately avoided in favor of more precise, non-imported terminology, consistent with the project's general stance (documented in [framework.md](../../../docs/framework.md)) against treating industry terminology as authoritative without independent redefinition.
6. **From treating Composition as a single concept to distinguishing Aggregate Composition from Presentation Composition.** This distinction emerged specifically from testing an early, overly broad claim ("Composition is just Aggregate, formed at higher layers") against a concrete legacy example, where it clearly failed — presentation-only nodes (action buttons in an invoice row) have no domain counterpart at all.
7. **The Authoring→Graph→Renderer diagram was corrected after review.** An early draft described the Graph→Output relationship as "compiles to," implying a single deterministic output. This was corrected to a two-relationship model: Authoring compiles *to* the Graph (single target), while the Graph is independently *reached by* multiple, simultaneous Renderers (fan-out) — a distinction that directly explains why the Theme/Layout/multi-modal layer exists at all, rather than leaving it implicit. The same conflation had briefly appeared in the document's own drafting and was removed as part of this correction.
8. **The Theme/Layout boundary and the possibility of user-authored Composition were added as an explicit open question ("Where Theme's Authority Ends"), not resolved.** Earlier drafts treated Layout and Theme as adjacent but did not record the deeper uncertainty about where one's authority ends and the other's begins, nor the more radical possibility (raised via the Android Launcher analogy) that user-facing customization freedom might extend beyond styling into Composition itself.
9. **The structural-notation-within-Authoring-Syntax topic was added as a newly surfaced, high-priority open question**, arising only after the rest of the document had substantially settled, from noticing that this project's own Markdown+YAML-front-matter documentation convention exhibits the same "two competing places for the same information" pattern the document argues against elsewhere (the RDFa-vs-JSON-LD case) — this time inside the very format used to write this document.

---

### Migrated to the current documentation structure
- Time: 2026-09-05T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested: conversion to the current facet-based documentation structure.
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote: front-matter slimming, provenance migration, heading and cross-reference normalization, Discussion-pattern restructuring.

#### Summary
Brought `content.md` in line with the current Explanation-facet specification:

- Front matter reduced to identity fields (`Title`, `Status`, `Start Date`, `ID`); the former `Citations`, `Contributors`, and `Applied to` fields moved into the Initial revision entry above (`Applied to` was empty — nothing to propagate).
- The `## Change Rationale` top-level section removed from the base document; its Evolution Summary is preserved in the Initial revision entry above. Its Known Limitations and Planned Revisions subsections were dropped rather than migrated, as every item in them restated content already present in the base document's Drawbacks, per-topic Unresolved questions, and Future possibilities.
- Numbered section headings (`### 1. …` … `### 15. …`) replaced with descriptive, unnumbered topic headings; `### 9.1` and `#### 15.1` became unnumbered subsections of their parent topics.
- All plain-text internal cross-references ("Section 4", "Section 13", the malformed "(Section, Introduction)") converted to real hyperlinks per the Internal Cross-References convention.
- Inline bold "Open Question" paragraphs restructured into topic-level `#### Discussion` → `##### Unresolved questions` bundles; the document-wide Unresolved questions list was distributed to the owning topics, keeping only the cross-cutting media-addressing question document-wide.
- Stale `/research/` paths corrected to the actual research directory, as relative references.

---

### Second migration wave: Discussion retired; open work moved to the new paired handoff
- Time: 2026-09-11T08:11:30Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](../../../modules-plugable/knowledge/documentation/explanation/explanation.md) — Depends_on: the three-section skeleton and the Relevance-discipline routing this migration applies are defined by the Explanation facet's governing specification.
  - [Documentation — Handoff](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) — Depends_on: the Open Questions / Anticipated Work record created by this migration follows the Handoff facet's specification.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - directed
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM 5.3) - applied

#### What changed
- All ten topic-level `#### Discussion` / `##### Unresolved questions` wrappers were dissolved; their questions (ten topic-level, plus the document-wide cross-cutting media question) moved to the newly created [content.handoff.md](./content.handoff.md) as Open Questions, per the Relevance-discipline routing — open questions are working state, not current design.
- The document-level `## Discussion` section was retired: its Drawbacks record and Prior-art surveys are preserved in this entry below; its Rationale-and-alternatives items are recorded under Considered and not done; its Future possibilities became the handoff's Anticipated Work. The `---` separator preceding the section went with it.
- This was the last remaining second-wave document besides polymorphism, abstraction-implements, giti, and lexer (see [documentation-explanation.handoff.md](../../../modules-plugable/knowledge/documentation/explanation/explanation.handoff.md)); the earlier hesitation about appending to this file is resolved by the owner's direction to run this migration in the same round — the remediation item for the Initial revision entry above (see [documentation-changelog.handoff.md](../../../modules-plugable/knowledge/documentation/changelog/changelog.handoff.md)) remains open and this entry does not touch that entry.

#### Considered and not done (migrated from the retired document-level Rationale and alternatives)
- **Extending RDFa/Microdata in place (rejected)**: embedding structured metadata as attributes inside content tags reproduces, by construction, the exact dual-source/scattered-metadata problem the Type Reference and Authoring Syntax vs. Semantic Graph topics were built to eliminate — regardless of how syntactically convenient any single attribute looks in isolation.
- **Adopting JSON-LD (a single separate metadata block) as the standard target format (rejected)**: a separate block is still a second, independently-maintained source of truth alongside the content itself, and the industry's own migration toward JSON-LD was driven by tooling convenience rather than resolving that duality — it merely relocated where the duplication lives. The Compiler-mediated model treats *any* such target (inline attributes, a separate JSON-LD block, or something else) purely as a generated output, never a hand-maintained source.
- **Adopting schema.org (or any other external vocabulary) as the default Type vocabulary (rejected)**: doing so would import that vocabulary's own modeling choices — which may not agree with this project's own modeling discipline (the `Password`-as-connection-token example) — directly into the architecture's foundation, and external vocabularies are demonstrably subject to unilateral change or deprecation on a timeline outside this project's control (the 2026 schema.org/FAQ-richresult case study). Only the reference *mechanism* is standardized; vocabularies remain external and optional.
- **Simply extending HTML's element/attribute vocabulary (rejected; the original approach of the early research)**: HTML's ~30 years of gradual, historically-motivated accretion means many of its elements are compositions of more fundamental concepts rather than fundamental concepts themselves (e.g., `h1`–`h6` as `Text` + an `Importance` level, rather than six independent concepts) — extending such a vocabulary risks perpetuating its historical accidents rather than correcting them.

#### Related work (from the retired Prior art)
- A detailed survey of prior art (HTML, ARIA, RDF, RDFa, JSON-LD, Topic Maps, Semantic Web stack, Hypermedia/REST, Microformats, Microdata, OWL, SKOS, XForms, UML, HCI pattern languages, Web Components, Design Tokens, VUI grammars, Accessibility Tree) was recorded in an AI-generated related-work survey (source file deleted 2026-09-23 after its final transfer audit; substance and caveats preserved here). That survey **carries no architectural authority** — see [Documentation — Research → Relationship to the Other Facets](../../../modules-plugable/knowledge/documentation/research/research.md#relationship-to-the-other-facets) for the distinction between research findings and adopted understanding; one entry in that survey (CKML) could not be independently verified and should be treated as unconfirmed pending primary-source review, not as an established finding.
- **XForms'** model/view separation via `<xforms:bind>` is the closest existing precedent to the Authoring Model / Semantic Graph split, though XForms never achieved broad adoption and offers no general-purpose (non-form) interface vocabulary.
- **Hypermedia/REST's** link-relation model (`rel="edit"`, `rel="cancel"`) is the closest existing precedent for expressing behavioral/action intent through typed relations rather than dedicated element types — directly relevant to the Reference-as-relation position.

#### Drawbacks (from the retired body Discussion)
- **Analytical cost.** Correctly separating Semantic, Composition, Layout, Theme, and Event — rather than reaching for a familiar mixed-syntax shortcut — requires deliberate, sustained analytical effort per concern. Teams without the discovery process behind this document may find the separations arbitrary or over-engineered until they encounter the specific failure modes (dual-source metadata, singleton widgets, scattered aggregate math) that motivated each one.
- **No implementation yet exists to validate these concepts against real, large-scale use.** Every concept above is discovery-stage; none has been stress-tested against a production system built specifically to this model.
- **Authoring tooling does not yet exist.** No editor support, validation, or auto-completion currently exists for any Authoring Model described in [Authoring Syntax vs. Semantic Graph](./content.md#authoring-syntax-vs-semantic-graph) — such tooling must be built, not assumed.
- **Risk of scope creep is structurally real, not hypothetical.** This document's own scope expanded substantially over the course of discovery (from a narrow CSS-avoidance idea, to a "Semantic Interface Architecture," to the full Content model covering Composition/Layout/Theme/Event). Each concern's "Implementation note" boundary exists specifically to contain this tendency going forward, but the boundary requires active maintenance — future contributors must resist re-absorbing implementation mechanics into this document once they exist elsewhere.
- **This document's own authoring format has not yet been checked against its own principles.** [Structural Notation Within an Authoring Syntax Itself](./content.md#structural-notation-within-an-authoring-syntax-itself) identifies that the document's own Markdown+front-matter convention may itself violate the inline-vs-external distinction this document argues for elsewhere — a self-consistency gap that is acknowledged, not fixed, here.

---

### Research sources deleted after final transfer audit
- Time: 2026-09-23T14:20:00Z
- Type: Removed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Mimo](../../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — audited, applied

#### What changed
- Both content-side research files — the Semantic Interface Architecture research document and the related-work survey — were audited against `content.md`, this changelog, and the paired handoff, then deleted along with the rest of the research directory. `content.md` no longer points at the research directory, and every path into it was removed from this file, with the report and survey names kept here in prose.
- The handoff's anticipated work "Independent verification of the AI-generated prior-art survey" was dropped with its source: the CKML entry can no longer be verified against the survey file, and the CKML-unconfirmed caveat in the Related work entry above stands as the standing record.
- Dispositions confirmed as already recorded before deletion: the HTML-extension approach, the element/attribute catalog, and the taxonomy proposals were deliberately abandoned as a starting point (body Motivation; Considered and not done above); numeric claims from the research are excluded by the body's methodology note; the survey as a whole carries no architectural authority.
- The following material received no disposition during the audit and is waived with the sources' deletion — recorded here so the waiver itself is examinable: the Design Language Mapping Matrix's observational findings (cross-design-system convergence on Primary vs Secondary distinction, destructive-action special-casing, universal FAB/Card, and dark-mode/RTL/responsive/motion/accessibility as cross-cutting concerns, across Material, Fluent, Carbon, and Ant); five related-work Decision-Log positions (Topic Maps associations-with-roles as relation-vocabulary input; UML state machines as the formal foundation for behavioral intent — the body's Event section went instead with the Observable/Dispatchable direction; HCI pattern languages as a future interface-concept-inventory source; Microformats' convention-over-specification; SKOS as a future taxonomy template); the research-internal rationale for skipping OWL (too expressive; wrong abstraction level); two research next-steps (a multi-renderer design-system integration proof; an HCI pattern inventory); and API/programmatic rendering as a named modality (the body names GUI, VUI, CLI, and Braille consumers but not API).

---

### Waiver examination — dispositions for the deleted-research findings
- Time: 2026-09-23T15:30:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Mimo](../../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — examined, dispositioned, applied

#### What changed
- Every finding waived by this file's research-deletion entry received an explicit disposition — each verdict on merits, so no waiver stands bare:
  - **Adopted into the body (1):** API/programmatic rendering as a named renderer modality — added to the Renderer enumeration in [Authoring Syntax vs. Semantic Graph](./content.md#authoring-syntax-vs-semantic-graph), matching the non-human consumers the Abstract already names (search engines, AI agents).
  - **Enriched into the handoff (2 State additions):** Topic Maps' associations-with-roles → the Reference navigate/embed/execute question, where relation-role vocabulary would land; the multi-renderer design-system integration proof → the Cross-modal rendering experiments anticipated work, as its design-system-level variant.
  - **Waivers upheld with reason:** the Design Language Mapping Matrix's observational findings — the summary survives in the deletion entry above; promoting a summary of a deleted matrix into a body claim would rest the claim on its own changelog, so re-derive from live design systems if the convergence ever becomes load-bearing; Microformats' convention-over-specification and SKOS as a taxonomy template — design inputs with no live claim to attach to; and HCI pattern languages plus the HCI-inventory next-step — leads recorded above; any such work starts from live sources, not the deleted survey.

#### Considered and not done
- UML state machines as the formal foundation for behavioral intent — rejected: the body's Event direction went to Observable/Dispatchable instead.
- OWL as an expressiveness layer — skipped: too expressive, wrong abstraction level.

---

### What a host's own mechanism costs a realization
- Time: 2026-09-28T09:56:00Z
- Type: Added
- Propagates to:
  - modules/khayyam/display/display.handoff.md: Done — the same four constraints, each with the code it was read out of, and the standing item that they are why the realization is an adapter
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — recorded

#### What changed
- The Theme / Role-to-Rendering Mapping topic gains [What a Host's Own Mechanism Costs a Realization](./content.md#what-a-hosts-own-mechanism-costs-a-realization): four constraints a host imposes on a realization, each stated as that host's behaviour and as what it costs us, read out of one host's own source (the editor this project's Khayyam display contract is realized in) — the field-by-field merge of grammar and semantic tokens and the discard of a token no style resolves; a token type that may not carry a separator, with the type hierarchy it is matched against; a `[name]` key in a colour customization being a theme key rather than a language key; and a setting whose default defers the decision whether semantic highlighting is computed at all to the theme.
- The consequence is stated once in the same subsection: the display contract is renderer-independent, every renderer is a realization of it, and where a host's mechanism is incomplete the translation belongs in the host's own files rather than in what the contract says — the toolchain's own documents already carry that as a decision, and this document now points at them.
- No code, contract, theme, grammar, or toolchain file was changed, and no light/dark strategy for the editor was settled; the constraints are recorded as constraints, not as a design for one realization.

#### Considered and not done
- Generalising the four constraints into a claim about hosts in general — rejected: each is a fact about one host's implementation, and the architecture-level statement is the adapter position, not a taxonomy of hosts.
- Settling the editor's light/dark strategy in this document — not taken: it is the owner's open decision about one realization, and an architecture document that settled it would make the contract a property of that host again.

---

### A rendering is checked by eye, and names the reader it is for
- Time: 2026-10-04T03:49:54Z
- Type: Changed
- Cited:
  - [Knowledge Research 001](../knowledge.research.001.md) — **Evidence**: the inquiry that weighed the four proposals behind this change, settled that the diagram proposal is a carrier-versus-rendering distinction this document already draws, and was then amended within the session that produced it, by the owner's authority, to carry the findings below. It reached `Complete` and no finding of it was revised.
  - [Karpathy on consuming model output](https://x.com/karpathy/status/2105819303471976479) — **Evidence**: the occasion for the question, and nothing more. What the post offers is its author's own practice and preference (a self-assessment, not a claim about observable behaviour), so it is admitted as the claim being weighed rather than as support for the conclusion; the conclusion rests on the notation already examined in this section.
- Propagates to:
  - [knowledge.md](../knowledge.md): Done — the same distinction arrives there as what a document owes its reader, scaled by what the reader's misreading costs.
  - [knowledge.research.001.md](../knowledge.research.001.md): Complete — its [Findings](../knowledge.research.001.md#findings) carry this entry's reasoning, and its [Related Artifacts](../knowledge.research.001.md#related-artifacts) section records what landed here.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — directed, decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — drafted

#### What changed
- [Concrete Evidence: Tree/Graph Notation in This Very Document](./content.md#concrete-evidence-treegraph-notation-in-this-very-document) gains a second consequence beside the one it already drew from non-visual consumption, and the second is about checking rather than reading. Readability and checkability come apart: a sentence that misstates a relationship is checked by reading it against what its writer meant, while a diagram that misplaces an edge is checked by looking at the diagram, and the eye supplies the very structure whose correctness is in question. A diagram is therefore a claim of lower inspectability than the prose stating the same claim, and the asymmetry holds for every consumer alike, because each trusts the rendering it can see.
- The consequence is sharper for a diagram a model generated: it holds the generator's reading of the subject and the generator's rendering of that reading in one artifact, and gives its reader no cue about which of the two to check. What makes a diagram worth producing — that a shape is grasped faster than a sentence is read — is therefore the same property that makes it unsafe to govern by.
- The section now states what follows, which it previously only set up. A generated diagram is a comparator rather than a substitute: it earns trust where it disagrees with a reading the reader already holds, because a disagreement is the one thing a rendering can show that prose cannot, and locating the difference is what sends the reader back to the subject. Where it agrees it tests nothing — a reader with a reading gets it confirmed rather than examined, and a reader without one is handed the generator's reading of the subject while believing it the subject's.
- It also says what makes such a rendering legitimate rather than malformed: it names its reader. A Facet is defined by the reader's relationship to its content, and a rendering admits the same classification — an artifact produced so that a person can see at a glance whether a plan took the right path is well-formed in the human-oversight class, and becomes malformed at the moment some later reader is expected to recover the model from it, which is the promotion recorded above seen from the receiving side. A notation chosen because a human eye reads it quickly is not thereby a notation a token stream reads at all: that is a property of the artifact's declared reader, not a defect in the artifact.
- The affirmative half is therefore stated rather than implied. Such a rendering is worth producing and worth reading, and a Renderer may draw one; what it may never become is the material a later reader is given, because a rendering promoted into the record is a second source of the model rather than a clearer statement of it, and the promotion is silent — promoted text reads like the project's own knowledge from the position where the project's own knowledge sits.
- The section's closing sentence is corrected to match: it previously described the whole section as recorded evidence, which stopped being true once the section states a consequence.

#### Considered and not done
- **A rule setting a tolerance for a partly-reliable aid**: not taken, and the section's argument is a classification rather than a tolerance. The objection answered here held that an aid helping ninety percent of the time with a ten percent error rate is worth using; nothing in the section disputes that, and nothing in it depends on it. What the section distinguishes is not how often a rendering is right but what a reader does with it — an aid a reader actively compares tests something, while a check a reader trusts silently reports — and a tolerance figure would say nothing about which of the two a given artifact is, while a number without an inspectable method is a qualitative judgment ([Content → Methodology](./content.md#methodology)).
- **A rule enumerating which notations a governing document may use, and a rule requiring every generated diagram to ship beside the prose it was drawn from**: neither taken. [Documentation → Written surface](../../../modules-plugable/knowledge/documentation/documentation.md#written-surface) states the first, and restating it here would be the redundant restatement [Documentation → Content Rule](../../../modules-plugable/knowledge/documentation/documentation.md#content-rule-no-fabricated-or-redundant-provenance) forbids; the second is a rule about a class of artifact the record does not admit, and stating it would imply the record admits them.
- **A rule stating that a comprehension aid must never be promoted into the record**: not added as its own rule. [UI Projection ≠ Domain Model](../knowledge.md#ui-projection--domain-model) already names a projection becoming the source of truth as the error, and [Knowledge → Write for the Structure of the Subject](../knowledge.md#write-for-the-structure-of-the-subject-not-for-todays-reader-limits) now states what the record owes a reader; a third statement of the prohibition would be the redundant restatement that section forbids.
- **A statement in [Cognition](../../../docs/cognition.md) about the capacity of a medium to carry meaning**: not taken. Cognition already holds that the medium shapes the exchange without defining it and that a text interface compresses bandwidth and flattens thinking material into prose; what it lacked was not the observation but its application to renderings, which is what this entry supplies.
- **Recording the recommendation that diagrams be requested from a model as a rejected option, and opening a second research for this exchange**: neither done. A negative finding has its home in a Research record, and that record exists and is cited here; the exchange added consequences and a classification to findings it had already reached without altering a conclusion or leaving a question open, so its own questions stand.
- **The practice as a Practice document**: not taken. The practice in question — asking for a diagram beside a plan to see whether the plan's path is right — is a way of working inside a session, and the record already states its standing: [Modeling → Graphs Are Not Documentation Artifacts](../../../docs/modeling.md#graphs-are-not-documentation-artifacts) gives a graph the status of a working tool rather than a deliverable. Naming it again in a Practice would duplicate that.
- **The objection that a chain of delegated stages leaves nobody who chose**: out of scope here, and not recorded in this section. It concerns who may decide rather than how meaning is carried, and it was examined against [Agency → Agency and Knowledge Management](../../../docs/agency.md#agency-and-knowledge-management), [Cognition → Discourse Norms](../../../docs/cognition.md#discourse-norms-derived-from-this-model), and [Modeling → Expected Output of a Modeling Chat](../../../docs/modeling.md#expected-output-of-a-modeling-chat), each of which already states the rule such a chain would violate.

---

### Restate the relation of a source recorded before the standing rule
- Time: 2026-10-04T13:27:43Z
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - claimed, argued, applied

#### What changed
No entry above is edited. This entry states the relation one of them recorded, under [Documentation → Citations → Source standing](../../../modules-plugable/knowledge/documentation/documentation.md#citations) as that rule now reads.
- The social-media post cited in *A rendering is checked by eye, and names the reader it is for* is recorded with the `Reference` relation, not `Evidence`. A post of that kind is admitted as the claim being weighed and as the occasion for the question, which is what that entry already said in its own words; the conclusion rests on the notation examined in the section itself, and the entry said so too.

#### Considered and not done
- Relabelling the entry in place was rejected (Space Bunny Alpha — argued). A changelog is append-only, and an entry rewritten after the fact cannot be distinguished from one that was written that way; restating the relation here keeps the earlier text intact and the correction visible.
- Removing the post from the record was rejected (Space Bunny Alpha — argued). Recording where a question came from is legitimate and the entry records it honestly; what was wrong was the relation, not the record.

#### Deliberation
The rule added in [Documentation → Citations](../../../modules-plugable/knowledge/documentation/documentation.md#citations) was applied against the whole doc set rather than only against the session that wrote it, and this citation was among the four it does not accept (Space Bunny Alpha — argued). An entry of an earlier chat cannot be rewritten, so the correction is recorded here (Omid Hekayati — decided).

---

### Two handoff questions closed by answers the base document already carries
- Time: 2026-10-04T18:17:38Z
- Type: Fixed
- Propagates to:
  - content.handoff.md: Done — the Lexical Token uniqueness-scope and Addressable Entity a-priori-test entries were deleted, each answered by `content.md` (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- The handoff's open question "What scope does Lexical Token uniqueness actually take?" is removed. [Content → Lexical Token vs. Sense — Handling Ambiguity](./content.md#lexical-token-vs-sense--handling-ambiguity) already answers it: a given string "is treated as a single, globally unique **Lexical Token**", with multiple parties attaching relations to that one token rather than each document holding its own. The question's own parenthetical — uniqueness global across a system as the working decision — is the position the body states, and no finer-grained scoping rule is proposed there, so nothing the body left open is lost by the removal.
- The handoff's open question "Does the Addressable Entity principle admit an a-priori test?" is removed. [Content → Addressability](./content.md#addressability) already answers it: "This principle is honestly circular and this document does not resolve the circularity," and it names the direction taken instead — asking "what units are *naturally* independently referenced within a given medium's own conventions," "an observable, empirical question rather than a predictive one." The recorded position is that no a-priori test exists, so the question was never open in the sense the handoff implied.
- [content.md](./content.md) is unchanged: both answers were already in its body, and the graduation is a matter of the handoff stopping restating them.

#### Considered and not done
- Editing `content.md` to state the two answers more sharply, or to add the empirical-framing question as work worth pursuing — not taken. The body already says the circularity is unresolved and names the empirical framing as future work; a sharper restatement would be the redundant restatement [Documentation → Content Rule](../../../modules-plugable/knowledge/documentation/documentation.md#content-rule-no-fabricated-or-redundant-provenance) forbids.
- Carrying the empirical-framing direction over into the handoff's Anticipated Work — not taken. The body holds it as a framing worth pursuing in future work, not as committed anticipated work, and inventing a handoff entry for it would schedule work nobody committed to.
- Marking the two entries Answered rather than deleting them — not taken. A handoff records where a discussion stands, and a resolved question is state the base document now carries; leaving a resolved question here duplicates the answer and guarantees drift.

---

### The Reference edge carries no consumer's choice
- Time: 2026-10-04T21:40:00Z
- Type: Changed
- Cited:
  - [Content](./content.md) - Consumed claim: the Reference topic's own statement that a renderer decides per modality how to expose an Affordance, and that navigation is not intrinsic to a Reference.
- Propagates to:
  - content.handoff.md: Done - the navigate/embed/execute open question is removed; its answer is the body's.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Reference as a Relation, Not a Property](./content.md#reference-as-a-relation-not-a-property) states that navigating, embedding, and executing are one consumer decision rather than three kinds of edge, and that no field on the edge names which applies: such a field would record a consumer's choice in the Semantic layer, which the [Foundational Principles](./content.md#foundational-principles) forbid. What a consumer does with an Affordance is therefore stated by that consumer, in its own terms.
- The handoff's open question "Are navigate/embed/execute properties of the Reference edge, or consumer-determined?" is removed. The topic already excluded navigation and named the renderer as the decider; what it did not do was exclude the field the question named or generalize from navigation to the family, and the new paragraph does both.
- The handoff's Timeline question is narrowed rather than removed. One Content participating in many Timelines follows from relations the body already states — neither Composition membership nor arrangement is a property of a node — so that part is settled and recorded as settled. What stays open is the cross-Composition case: whether a Timeline spanning separate Compositions is an arrangement at all, which turns on whether `contains` and `refers-to` are one primitive family, and on the body's own deferral of any shared arrangement vocabulary to the dedicated Layout/Theme document. Its `Next:` line is unchanged, and `content.md` gains nothing for it.

#### Considered and not done
- Topic Maps' associations-with-roles as relation-role vocabulary carried on the edge - rejected: it names the consumer's choice in the Semantic layer, and the survey that raised it was deleted with its disposition already recorded in this file.
- Deleting the handoff entry and editing the body not at all - considered: the body's rule covers navigation alone, and the `mode` field the question names is excluded nowhere, so the generalization is a real addition rather than a restatement.
- Stating that Timeline is not a distinct concern of Content - not taken: the body's arrangement claim is scoped to siblings within a Composition and marked tentative, and the case a Timeline raises is cross-Composition, so the exclusion would rest on the very question the narrowed handoff entry keeps open.
- Waiting for the cross-modal rendering experiments before closing the navigate/embed/execute question - not taken: the answer does not vary by modality, since the renderer already decides per modality, so the experiments remain under the handoff's Anticipated Work.

---

### Composition's edge kind and media coverage settled from principles already held

- Time: 2026-10-05T10:12:46Z
- Type: Changed
- Propagates to:
  - content.handoff.md: Partial - two entries left Open Questions, and the *Can one Content participate in multiple Timelines* entry still names the `contains`/`refers-to` question as its blocker, which this change discharges; that entry is not resolved and the stale clause was left in place rather than repaired under this change.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- [Composition](./content.md#composition) now states that `contains` and `refers-to` are the same kind of edge playing different roles - both are ordinary edges, and what separates them is what the edge asserts, since a reference is a pointer the referencing node depends on but does not own while ownership binds the referenced node's lifecycle to the owning one - so ownership needs no primitive of its own and adds obligations rather than a different kind of edge.
- [Addressability](./content.md#addressability) now states that untyped media are covered by the Addressability primitive already shared between unstructured content and Composition rather than by a primitive of their own: an image region or a video time range that needs to carry an independent relation becomes an independently addressable entity, and meaning attaches to it as Reference edges exactly as it does to a span of free text.

#### Considered and not done
- **Deriving the edge-kind distinction from this document's own Composition section (rejected)**: that section states the aggregate/presentation split, warns that collapsing the two graphs is an observed failure mode, and defers concrete mechanics to the host language's type/capsule system. It says nothing about edge kinds, so the answer had to come from the edge taxonomy that already names reference and ownership/composition as two roles of one ordinary edge, and that taxonomy is what the body now points at.
- **Treating the media entry as already answered by the Abstract's mention of untyped media (rejected)**: the Abstract places media where the Semantic and Addressability topics concentrate their weight, but it does not say they need no primitive of their own, and the Addressability topic still poses region-and-timestamp addressability as an open question. What is now settled is the coverage of media, not which units inside a medium deserve an address, which the Addressability topic's own acknowledged circularity continues to govern.

---

### The Timeline handoff entry's dependency on the `contains`/`refers-to` question dropped
- Time: 2026-10-05T10:56:50Z
- Type: Fixed
- Cited:
  - [Content → Composition](./content.md#composition) — Depends_on: the settled position that discharges the stale dependency — `contains` and `refers-to` are the same kind of edge playing different roles, and ownership adds obligations rather than a primitive of its own.
- Propagates to:
  - [Content Handoff → Can one Content participate in multiple Timelines, and is Timeline a distinct concern?](./content.handoff.md#can-one-content-participate-in-multiple-timelines-and-is-timeline-a-distinct-concern): Done — the entry's residue is the cross-Composition case and the Layout/Theme deferral already named beside it; the entry stays open and its question is unchanged.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- [Content Handoff → Can one Content participate in multiple Timelines, and is Timeline a distinct concern?](./content.handoff.md#can-one-content-participate-in-multiple-timelines-and-is-timeline-a-distinct-concern): the clause naming "the still-unsettled question above about whether `contains` and `refers-to` are one primitive family" as what the cross-Composition case depends on is removed. That question is answered — [Content → Composition](./content.md#composition) states that `contains` and `refers-to` are the same kind of edge playing different roles, and that ownership adds obligations rather than a different kind of edge — so naming it as an open dependency left the entry waiting on something the record no longer holds open.
- Nothing else in that entry changed. Its question stands, the part recorded as settled stays recorded as settled, its `Next:` line is untouched, and what remains open is the cross-Composition case — whether a Timeline spanning separate Compositions is an arrangement at all — together with the body's own deferral of any shared arrangement vocabulary to the dedicated Layout/Theme document.

---

### Unstructured content is a category, not an exemption
- Time: 2026-10-05T17:15:06Z
- Type: Changed
- Cited:
  - [Type → Abstract](../../../docs/type.md#abstract) — Evidence: "every semantic entity is a Type: a semantic entity that has no Type is not an entity this framework can state", which is what the untyped-media wording contradicted
  - [Type → Type Beyond Programming Languages](../../../docs/type.md#type-beyond-programming-languages) — Evidence: no system exists whose semantic entities have no Type, so "outside any type system's reach" had to become "carries no predefined field"
  - [Type → Type vs Implementation Type](../../../docs/type.md#type-vs-implementation-type) — Evidence: "their Types exist, as any system's do", which is the sentence the dynamic-language paragraph now rests on
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The Abstract's central discovery now reads that what a type system does not reach is content that carries no predefined field to hold its meaning, so the category name `unstructured content` survives as a category of content — free text and media — and the sentence says they are Types like everything else and become independently addressable entities, with meaning attaching as Reference edges rather than as a schema they would have had to be shaped to carry. The document's own point is unchanged in substance: what these fragments lack is a field, and addressability is what replaces it.
- The *Addressability* paragraph that began "Untyped media are covered by this same primitive" now begins "Unstructured media are covered by this same primitive", which removes the typing claim from that paragraph without touching its reasoning — an image region or a video time range that must carry an independent relation still becomes an independently addressable entity with Reference edges attaching to it.
- The *Khayyam-manner* topic now states what the friction names: a dynamic-typed language approximates the class this document prefers rather than stating it, because its Types exist, as any system's do, and none of them is written in its source. The two properties the document does not give up — no unwrapped primitives, absolute encapsulation — are untouched.

#### Considered and not done
- The paragraph about not abandoning typing discipline "in favor of an untyped markup language" was left alone. There `untyped` describes an authoring language that would carry semantics without Types, which is a different claim from the one this entry removes.
- The unresolved question about the boundary between structural delimitation and embedded semantic tagging was not reopened. It asks about authoring syntax, and no sentence changed here bears on what an authoring format may carry.
- The document's own recommendation against adopting an unconstrained vocabulary of tags was not touched, and no new primitive was introduced for unstructured content: the category keeps the primitive it already had, Addressability.

#### Deliberation
The tension was not the category but the exemption. Read against a document declaring that every semantic entity is a Type, the Abstract's "genuinely outside any type system's reach" established a standing untyped remainder inside a system, which is the one shape the ruling cannot admit. The first sentence drafted for the fix — that free text and media are Types and meaning attaches to them as Reference edges "exactly as a typed structure's does" — was rejected before it was written, because that comparison would have dissolved the document's own reason for treating these fragments separately (Space Bunny Alpha — argued, drafted). The adopted wording keeps both halves the owner required: no predefined field is why addressability is needed rather than a schema, and Typehood is stated as a fact about the entities rather than as an exemption from it (Omid Hekayati — decided).

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:00Z
- Type: Changed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to `content.md`, `content.handoff.md` and this file against HEAD. The settled handoff questions (navigate/embed/execute, Lexical Token uniqueness, Addressable Entity a-priori test, Composition `contains`, media coverage) each have their answer in `content.md` and an entry above; the Timeline entry's narrowing, the Abstract and Khayyam-manner rewording, and the `../modules/khayyam` to `../bundles/khayyam` link repairs hold, and `memar content check` reports no problem.
- `content.handoff.md`, the *Can one Content participate in multiple Timelines* entry: removed the clause "originally moved 2026-09-11 from the Layout topic's retired Discussion wrapper". The committed entry records the knowledge-management session as its origin and nothing ties it to the Layout wrapper (that wrapper's question is the separate arrangement-primitive entry), so the clause was provenance the project does not record.
- Removed the uncommitted entry "An anticipated-work entry about a command left this handoff, unrecorded here" (dated 2026-10-06T00:00:00Z). HEAD holds no *A content-grouped documentation command* entry in `content.handoff.md` or `documentation.changelog.md`, so the entry recorded a state no reader ever saw, which [Documentation Changelog → Trivial changes](../../../modules-plugable/knowledge/documentation/changelog/changelog.md#trivial-changes) says gets no entry.
- The one-word change in the 2026-10-04T13:27:43Z entry's contributor line ("space-bunny-free" to "space-bunny") was left: it matches the label every other entry uses.

---

### The document moves to `modules/knowledge/content/`
- Time: 2026-10-17T10:41:00Z
- Type: Changed
- Cited:
  - [Modules → What does not belong here](../../README.md#what-does-not-belong-here) — `Depends_on`: a concept document that needs code leaves `docs/`
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — applied

#### What changed
- `docs/content.md`, `content.changelog.md` and `content.handoff.md` moved to this module under the `knowledge/` category, beside `documentation/`, which stands directly under the category and no longer under content. Links to the three documents were rewritten and nothing else in them changed.
- Occasion: the owner's ruling of 2026-10-17 that content belongs with knowledge and not among the base documents.

---

### Front-matter example corrected
- Time: 2026-10-17T16:00:00Z
- Type: Corrected
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-17)
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- The example lists the fields documents carry (Title, Status, Start Date, ID), not Citations and Contributors, which moved to the changelog.
- Why: task 20261016-T095101Z-22960 found the text contradicted the documents and types in use; the owner approved the correction on 2026-10-17.

---

### Organization's content-domain text carried into this module after the merge
- Time: 2026-10-19T11:00:00Z
- Type: Changed
- Cited:
  - [Handoff → Decisions](../../../modules-plugable/knowledge/documentation/handoff/handoff.md#decisions) - `Depends_on`: a decision stays in a handoff while no governing document carries it, which is why the organization's decisions are kept there and not written into this document
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — directed (2026-10-19)
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — carried the text by hand

#### What changed
- The merge of 2026-10-19 (merge commit ceba0177) kept this module's files where the organization repository had a file at the same path, so the organization's text for `content.md`, `content.handoff.md`, `content.changelog.md` and `README.md` existed only at commit 19834121. Each was read whole beside this module's version; the result is one model per file.
- `content.handoff.md`: the organization's handoff is merged into this one. Carried: Topic & Purpose (merged into one paragraph naming both readings of Content), Status, every Decisions bullet under its original heading (Content & Timeline; Relations & edge vocabulary; Versioning; Code as Content; GUI projection requirements; Concurrency), the two decision groups the organization had parked under a second `Decisions` heading (The org's own document model; Knowledge capture, channels & migration) as headings under Decisions, the Open Questions list (its items 1, 3, 4, 7 and 8 and the concurrency note) as one entry each beside this handoff's own entries, the whole of "Research 001 questions and next steps", Related Artifacts, Notes and the "Knowledge vs Document / Representation" section. Added: an Open Questions entry on whether the interface-semantics Content and the organization's content domain share one document, since the organization's own handoff already said `content.md` "covers a different" Content. Merged: the organization's open item on Timeline primitivity is added to this handoff's existing entry on Timelines, with a link to the decision.
- Reworded to fit one model, each recorded here: the Open Questions list lost its numbers (the organization's list skipped 2, 5 and 6), so the research's references to "open question 1" became a named entry; the Status line of the two handoffs became one; the sub-heading "Status" under Research 001 became "Standing of the research's proposals" so no heading repeats; research question 1 and Next Step 2 no longer say the definition goes into `content.md`, which stays the interface-semantics model (Tentative; the owner's ruling is the new entry); the second `Decisions` wrapper heading is dropped, its provenance line kept as a sentence under "The org's own document model".
- `content.md`: the organization's text held only its Idea backlog, a section of review-pending ideas ("nothing below is ratified"). This document's method keeps unresolved questions out of the body, so the six ideas and their review questions are carried, whole, as "Idea backlog" under Anticipated Work in the handoff; nothing is added to `content.md`. The one relative link `../../../modules/economics/product/product.md` became `../../economics/product/product.md`, and the link to `modules/management/vocabulary-discipline.handoff.md` was written relative.
- `content.changelog.md`: the organization's record "Research on what the content domain is for, its kernel, and the owner's questions" (2026-10-16T01:00:00Z, added) is carried in this record, not as a second record, because its time precedes entries already here and the ledger is oldest-first: it added `content.research.001.md` (thirteen scenarios, a four-element kernel, five rival models, a mapping of every edge, loop and widget folder, thirty test scenarios, eighteen contradictions, twenty owner questions with defaults) and extended the handoff with the twenty questions and eight Next Steps; it changed nothing in `content.md`, any edge document or any `.kh` file. The organization's changelog heading and title lines are dropped: this ledger has its own.
- `README.md`: identical on both sides (it names `content.md`); not changed.
- `content.research.001.md`: three links `content.md#idea-backlog` now point to `content.handoff.md#idea-backlog`. The handoff headings the research links to are all present again: Decisions, Content & Timeline, Relations & edge vocabulary (content-relevant), Versioning (content identity), Concurrency (offline multi-actor) — merge-conflict / semantic unit, Knowledge capture, channels & migration, The org's own document model, Research 001 questions and next steps (2026-10-15), and the Knowledge vs Document / Representation section. `text.research.001.md`'s link to Versioning (content identity) resolves again with no edit.
- Dropped with reason: nothing of the organization's text, except the headings and numbering named above.
- Why: the merge chose this side so that nothing broke; the organization's thinking on the same concept had been left in history and its documents linked to headings that were gone. Task 20261019-T103318Z-22516.

---

### `memar content find` and `search` read the tasks' records when asked, with `--from`
- Time: 2026-10-19T18:30:00Z
- Type: Added
- Cited:
  - [Handoff → Where a finished task's records are kept](../../../modules-plugable/knowledge/documentation/handoff/handoff.handoff.md#where-a-finished-tasks-records-are-kept) - Evidence: said the corpus "no longer leaves `.agents/tasks/` out", which reached only a checkout holding that folder and never the records branch, where the records are.
  - `docs/comparisons/context-mode.001.md`, sections 1, 6 and 7 - Motivation: Memar keeps its task records and no verb could find anything in them.
- Propagates to:
  - modules-plugable/knowledge/documentation/handoff/handoff.handoff.md: Done - the entry "Where a finished task's records are kept" says what the corpus reaches now and since which session.
  - bundles/memar/memar.handoff.md: Done - the bullet on the kept index says how the sessions' files are kept in the MCP worker.
  - docs/comparisons/context-mode.001.md: Done - its finding was checked again against the fixed verbs on 2026-10-19 by two reviewers that had not drafted it, and the essay now states the state before the fix as history and the state after it as fact.
- Tasks:
  - dev-knowledge:.agents/tasks/20261019-T170853Z-4740/: Closed - the session that made the change.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested, decided (2026-10-19)
  - [Claude](../../../CONTRIBUTORS.md#claude) (claude-opus-5-5 via Claude Code) — implemented, tested

#### What changed
- `memar content find` and `memar content search` take `--from SOURCE`, repeated for several, whose values are declared once in `primitive/corpus_source.py` with what each reads: `documents` (the Markdown files the corpus walked before), `code` (its `.kh` files) and `sessions`. Without the flag they read the documents and the code, as before; nothing else changed in what the default reads or prints.
- `sessions` reads every text file of every session of the project (`services/session_records.py`): the archived records on the records branch, through git's read-only commands in one `ls-tree` and one `cat-file --batch`, so HEAD, index and working tree do not move; and the live task folders, those in the project's tasks folder and those in Memar's own whose plan names the project by its folder, less a session's own `temp/`. A session with a live folder is read from it alone, as `memar git show-task-records` reads it first. On this checkout, 1,537 archived files and the live folders are read and ranked in about three seconds.
- A hit names its origin: `dev-knowledge:.agents/tasks/<id>/<file>` for an archived file, the folder's path for a live one. `find` ranks a session's Markdown by section as it ranks a document, and any other text file as one unit named by its file. Each verb's help says that such a hit is a task's record, never a ruling.
- When a project has no archived records to read — its preferences say `records: off`, it is not a repository's top folder, or its repository has no records branch — the verb says so on standard error rather than answering with silence.
- `search` now takes `--project` / `--project-path`, as `find` already did, since a project's records are on its own branch.
- The form of a session's reference and the read-only git calls on the records branch moved to the shelf below both modules, `.agents/scripts/modules-plugable/computer/git/services/_git_records.py`: the content module may not import the session module, which imports it. `modules-plugable/computer/git/services/branch.py` asks it for the reference and the folder's path; the task verbs behave as before.
- `memar git archive-task-records`'s summary and help say the records are also read by content.
- The MCP tools need no code of their own: `--from` is generated as a list of the three values for `content_find` and `content_search`.
- Tests: `tests/session_records.py`, a scratch repository with a records branch: a term only an archived record holds is found, and not without the filter nor with `documents`; a live folder is read and its `temp/` is not; `records: off`, a repository with no branch and a folder inside another repository are said; the default corpus is unchanged; the help and the MCP schema carry the flag.

#### Considered and not done
- A verb of its own over the records: the owner ruled a filter on `memar content`.
- Reading the records only by their Markdown, as the documents are read: the archive keeps scripts, logs and text notes as well, and four of the 25 archived files that mention "compaction" are `.txt`.
- Making `sessions` part of the default: a hit from a session is a claim, and a reader who did not ask for claims would read them beside the rulings.
- A source for each of the two places, archived and live: one session has one record, read from the place `memar git show-task-records` reads it.
- Reading the sessions in `backlinks`, `obligations` and the other verbs that read the corpus: they answer about the documents' links and ledgers, which a task's records are not.

---

### Checking text: the dispatcher over the domains a node belongs to
- Time: 2026-10-23T17:30:00Z
- Type: Added
- Cited:
  - [Memory Record](../../../modules-plugable/computer/memory/store/record/record.md) - Reference: the port stays blind to encodings
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme; the build tasks are queued after it
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-22/23), ruled the premises it rests on
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted
  - Three sub-agents (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed; their findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- [content.md](content.md) gains the section Checking text: content as the dispatcher, the domains asked (text, an authoring syntax, documentation), a finding, the two moments (when a text node is written, and as a query), the legacy mode of the migration, the label that attaches a domain's check, and the state of the verb until the dispatcher is built. It marks `Owed: content.check-dispatcher`.
- [content.handoff.md](content.handoff.md), [text.handoff.md](../text/text.handoff.md) and [documentation.handoff.md](../../../modules-plugable/knowledge/documentation/documentation.handoff.md) gain the entry that each domain owes its part of the check.

---

### The Python services leave the content module
- Time: 2026-10-24T09:10:00Z
- Type: Changed
- Cited:
  - [Knowledge](../knowledge.md#the-modules-of-this-category) - Reference: where the neighbouring modules stand
- Tasks:
  - main:.agents/tasks/20261018-T133018Z-26648/: Partial - the split by subject; the owner agreed the placements per subject
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-18) and ruled each placement (2026-10-24)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — proposed and applied

#### What changed
- The 35 service files of `services/` are no longer here except `reference.py`, `resolve_path.py` and `path.py`, with the primitives `word`, `section` and `record_key` the task module and the documentation module both draw on. Search, ranking and the corpus went to [Text](../text/text.md); the reading of Markdown to [Markdown](../../../modules-plugable/computer/codec/markdown/markdown.md); the changelog, the questions, the propagations, the normative-references lists and the check to [Documentation](../../../modules-plugable/knowledge/documentation/documentation.md); writing and editing a file to the filesystem module; the context of an act to the `ai` module; the task records to the task module. Each verb keeps its word under `memar content`, by the router's rule of a file named `content_<verb>.py`.
- `memar content check` is now composed: its bytes half is `text/services/text_check.py`, the rest stays in the documentation module's `content_check.py` as the composer.
- No kernel module reaches a pluggable one by an import any more, and the module-graph test passes with no allowance.

#### Considered and not done
- Removing the word `content` from the verbs: it changes every MCP tool name, the skill and `AGENTS.md`, so it is a task of its own (owner, 2026-10-24: a service is an independent identity with a complete name, and the category in front of it is to go).
- Removing `meta`, `section`, `path` and `obligations` as duplicates of `get-meta`, `get-section`, `resolve-path` and `list-undischarged-propagations`: they are a rename in progress by another chat, and the installed launcher still calls `content path`.

---

### Encoding blindness repointed to the memory contract; node and label vocabulary asked of the owner
- Time: 2026-10-24T17:30:00Z
- Type: Changed
- Cited:
  - [Memory](../../computer/memory/memory.md#retention-is-reached-through-one-contract) - Reference: the memory contract's reference to an address, which is all a kernel module takes of retention
- Tasks:
  - main:.agents/tasks/20261024-T160312Z-25344/: Partial - repoints the kernel documents from the record contract to the memory contract's reference to an address; a fresh critique follows
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled on 2026-10-24 that the link is only the reference to an address
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — found the statements and wrote the change

#### What changed
- `content.md`, "When a check runs": that the store stays blind to encodings is stated of the memory contract, which holds bytes under addresses, in place of the `record` contract. `content.handoff.md` gained the Open Question "Does the content domain need nodes, parts and labels, or only addresses?".

#### Considered and not done
- Rewriting the text node, `blob` node and `legacy-unchecked` label wording: they are `record`'s vocabulary and load-bearing for the attachment of the check, so the owner decides.
