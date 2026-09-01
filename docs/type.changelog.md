# Type Changelog

## Changelog

The seven entries below are migrated from `type.md`'s former `## Change Rationale` section. They were developed across research sessions between the document's Start Date (2026-07-19) and its first commit (2026-07-20); individual timestamps were never recorded, so each carries `Time: unknown` and only their relative order is reliable. Contributor attribution follows the surviving records — the former front-matter `Contributors` field plus each revision's own description — which pinned some rounds to specific reviewers and left the applier unrecorded; where history did not name who applied a change, no applier is invented here. The former front-matter `Citations` list is carried on the entry that added it (fourth revision, below); the two citations the base document's own readers still need — its dependency on Modeling and its pointers to the Khayyam companion documents — now live as ordinary links in the base document's body instead.

### Initial draft
- Time: unknown (historical import)
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued: authored the initial reflections on Type as a semantic entity and its relationship with Capsule and Abstraction; directed the philosophical framing of Type as an independent concept considered before its manifestation in Khayyam.

#### Summary
Established the foundational concepts of the document: Type as a Semantic Entity, Type and Modeling, Capsule and Abstraction as realizations of Type, Type and Rules, and Type and Relations.

---

### Restructuring into the document template, with cross-language research
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — researched, rewrote: conducted the cross-language and type-theoretic research; restructured the document to follow the then-current template.

#### Summary
Restructured the document into the formal template. Added Type Identity, Type vs Implementation Type, the rule categories, Capsule/Abstraction bridge analysis, and unresolved questions based on cross-language research.

---

### Primitive types removed; Method and Scope added as categories
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: identified Method as a type category and the absence of primitive types in Khayyam; corrected assumptions about primitive types; emphasized the independent-concept-first structure.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote: applied the corrections across multiple revision iterations.

#### Summary
Corrected structural errors based on review feedback: removed Primitive Types (Khayyam has none), added Method as a Type category (`mt`), added Scope as a Type category (`sc`), repositioned the definition of Type as an independent concept before its manifestation in Khayyam, reduced overall length by consolidating repetitive comparative analysis, and aligned the category model with Khayyam's actual four-subtype structure (`cp`, `mt`, `ab`, `sc`).

---

### Alignment with the companion documents
- Time: unknown (historical import)
- Type: Changed
- Cited:
  - [Modeling](./modeling.md) — Depends_on: Type is the result of correct modeling; the concept of Type cannot be understood independently of the modeling process that identifies what should exist as a Type, and Modeling establishes that abstractions are justified by independent responsibilities, not by data.
  - [Encapsulation in Khayyam](./khayyam-encapsulation.md) — Reference: specifies how Capsule and Method manifest in Khayyam — Sovereign Encapsulation, method invocation rules, and the rejection of tuples and consumer-side mutability keywords.
  - [Abstraction in Khayyam](./khayyam-abstraction.md) — Reference: specifies pure contracts, implicit structural satisfaction, rejection of default implementations, and abstraction composition.
  - [Inheritance in Khayyam](./khayyam-inheritance.md) — Reference: inheritance is a relationship between abstractions, not between capsules — behavior transfer rejected, abstraction extension supported.
  - [Polymorphism in Khayyam](./khayyam-polymorphism.md) — Reference: classifies the polymorphism forms Khayyam supports through abstraction conformance — inclusion, parametric, and ad-hoc — and the rejection of generic syntax.
  - [Khayyam](./khayyam.md) — Reference: documents the recurring principles (Behavior Over Type Identity, Domain Modeling, Syntactic Atomicity) that the Type concept in Khayyam instantiates, and is the canonical specification of Khayyam's type subtypes and their syntax.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote: incorporated the companion-document findings into the document.

#### Summary
Incorporated findings from the companion documents (Encapsulation, Abstraction, Inheritance, Polymorphism, Modeling). Resolved the Type Identity open question about structural satisfaction vs. nominal identity by referencing the Abstraction document's treatment of implicit structural satisfaction and accidental satisfaction risk. Added the relationship between inheritance and Type categories (inheritance between Abstractions, not Capsules). Added the Modeling document's "Concept Existence vs. Model Existence" principle to the decision framework. Refined the Methodology section to reflect the actual research approach.

---

### Critical-review round: exclusive boundary, hierarchy position, and the weakened bridge claim
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — reviewed, argued: critical review whose findings this revision applied.
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed: flagged the Method-as-Type argument weakness, the Scope justification gap, the Type-definition exclusivity concern, and the DDD reference overhead (recorded in the former Contributors field; the surviving history does not tie this review to a single numbered pass).
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed: flagged the Method-as-Type argument weakness, the Scope-as-Type justification gap, the Type-definition exclusivity risk, the DDD reference overhead, the premature bridging claim, and the Type-hierarchy resolution (recorded against the preceding revision's state; the surviving history does not tie this review to a single numbered pass).

#### Summary
Applied critical review from ChatGPT (GPT-5.5): (1) removed all references to DDD and Aggregate Root — these belong in companion documents, not in the Type definition; (2) added "What Is Not a Type" to establish the exclusive boundary of the definition, addressing the risk that an overly inclusive definition dilutes the concept; (3) moved the Type-hierarchy question from Unresolved to an official position — "Type Categories Are Not a Hierarchy," categories connected through semantic relationships rather than taxonomic classification; (4) strengthened the Scope category as a "semantic boundary" defining visibility, ownership, composition, and isolation, not merely a syntactic block; (5) improved the Method-as-Type argument — Methods are Types because they are the fundamental semantic building blocks through which higher-level concepts (rules, vouchers, policies) are expressed, not merely because they have identity and contract; (6) weakened the bridging claim to "currently the primary mechanism" connecting Capsules and Abstractions rather than the definitive bridge; (7) clarified Method lifecycle as definition, composition, specialization, and execution — not runtime creation/destruction; (8) added the conservative-expansion principle, avoiding the OOP-style overloading that rendered "Object" meaningless; (9) recorded Method-as-Type as an unresolved question, well-motivated but not yet validated through implementation; (10) removed the "Beyond DDD" subsection from Type and Modeling.

---

### Consistency fixes: relations table, Scope identity, and de-duplication
- Time: unknown (historical import)
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, argued: critical review, cross-checked against `khayyam.md`.

#### Summary
Applied critical review from Claude, cross-checked against `khayyam.md`: (1) replaced the parent-child tree diagram under "The Relationships Between Categories" with a relation table, since the tree's visual shape contradicted the adjacent "Type Categories Are Not a Hierarchy" claim; (2) resolved a direct contradiction in the Scope section — the claim that a Scope's identity derives from its containing Method conflicted with the independent-identity criterion; containment within a method body is now framed as a syntactic placement constraint, distinct from Scope's independent semantic identity; (3) reframed "Type and Relations": a Relation presupposes the Types it connects and therefore operates one layer above this document's concern, deferring first-class-Relation questions (endpoint ownership, directionality, arity) to a future companion document, and "Manifestation in Khayyam" no longer lists first-class relations among realized principles, since Khayyam does not currently manifest them; (4) strengthened the Method-as-Type argument with the distinguishing property — independent, referenceable existence (signature, cross-file import, receiver-independent attachment, composition) — closing a circularity gap where the prior argument could equally apply to any executable construct; (5) removed duplication between "How to identify a Type" and "What Is Not a Type," the former now pointing to the latter for the negative-criteria catalog.

---

### Placement-based Scope justification withdrawn; identification framework generalized
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — reviewed, argued: second critical-review round, cross-examined and refined through discussion.

#### Summary
Applied a second round of critical review from ChatGPT (GPT-5.5): (1) removed the placement-based justification for Scope entirely rather than merely softening it — the claim that Scope "must" live inside a Method is documented as Khayyam's current syntax/usage pattern (a language-layer concern, deferred to `khayyam.md`), not a defining property; (2) added "A note on independent identity" generalizing the fix beyond Scope: independent identity is a claim about meaning, not about existing free of any containing context — a parameter has identity distinct from its Method despite being confined to that Method's signature; (3) added "Why Only Four Categories?" — a Type category is justified only by a fundamental semantic role irreducible to specialization, composition, or usage pattern of an existing category; Rule, Relation, Protocol, Workflow, and Policy depend on Types without justifying distinct categories; (4) added "Type Categories vs Language Keywords," a mapping showing common keywords elsewhere (`struct`/`class`/`record`, `interface`/`trait`, `function`/`procedure`, `namespace`/`module`/`package`) as typically realizations of Capsule, Abstraction, Method, or Scope — a dedicated keyword elsewhere does not imply a distinct foundational concept; (5) added "Type Beyond Programming Languages" to the Introduction — Type is not introduced by programming languages; Khayyam's prominence here reflects its role as the first concrete manifestation of these principles, not a claim that Type originates in language.

---

### Migration to the Explanation-facet template with a paired changelog
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked that this document be upgraded to the current documentation methodology, moving provenance into a paired changelog file.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — rewrote: performed the migration described below.

#### Summary
This document is now structured per `documentation-explanation.md` with no provenance in its front matter or body: the former `Applied to`, `Citations`, and `Contributors` front-matter fields and the `## Change Rationale` section are migrated entirely into this file (entries above). Two in-body sentences that referenced the removed `Citations` field were reworded (Methodology; "Manifestation in Khayyam"), and plain-text mentions of the documents the reader genuinely needs while reading — `modeling.md` (in "Type Categories Are Not a Hierarchy" and "Type and Modeling"), `terminology.md`, and the Khayyam companion documents — became ordinary hyperlinks, per the rule that reader-needed sources link directly in the body while argumentative provenance lives only here.

---

### Stateless Types topic; dissolution of their source document
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Propagates to:
  - modeling.md: Done — the classification gray zones (incidental metadata; temporal graduation) added to its loop-edge discussion; see modeling.changelog.md.
  - type.practice.md: Done — created as this document's Practice counterpart, absorbing the operational layer of the same source; its record is merged into this ledger.
  - error.md: Done — nine references repointed here from the dissolved document; see error.changelog.md.
  - immutable_infrastructure.md: Done — the compatibility-and-logical-independence analysis now lives there as "Relationship to Type-Level Identity", carrying the provisional-content caveat forward; see immutable_infrastructure.changelog.md. The document's dedicated session may still revise the section against its final formulations.
  - Future Khayyam tooling documents: Pending — preserved decisions with no current home: covariant returns follow from abstraction conformance (the Error-case statement lives in error.md); code generators emit one type per static concept, 1:1 with their input definitions; cross-language mapping preserves identity only because identity was never stored as data; the authoritative enforcement checkpoint is the generator-input layer rather than output-source heuristics; exhaustiveness is a real, unresolved need assigned to linter/compiler tooling without new syntax — candidate mechanisms to evaluate include code-generator metadata, whole-program analysis, and an explicit "closed contract" declared on the abstraction, with Kotlin sealed classes and Swift closed hierarchies as prior art achieving it over compiler-known closed sets of types.
  - Future ADT document: Pending — whether `IsEmpty`/`IsNil`/`IsNull` semantics make sense for stateless Types at all (methods inherited from `ADT`); error.md tracks the Error-specific instance and defers to the dedicated ADT session.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: pre-facet micro-documents predate Memar's documentation principles; the end state is strong Explanation documents plus sufficient Practice documents, with citations pointing at Type and Modeling generally so downstream work inherits principles instead of a private vocabulary. Reviewed the lens analysis that motivated dissolution.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — drafted, applied: authored the new topic from the source's principle core; performed the dissolution and cross-document redistribution.

#### Summary
Added "Stateless Types" under Type vs Implementation Type, opening with the governing principle — identity belongs to the type system, answerable from the Type alone at compile time, never from runtime data — followed by the three-role decomposition table (Identity → type system/compile time; Behavior → methods; Data → fields/runtime), the MUST that stateless concepts be carried as their own named entities, the ascent-problem framing of data-simulated identity, boundary clauses against over-splitting and structural reasoning and family-resemblance-as-qualification, and a Drawbacks note recording the accepted proliferation/API-surface trade-off.

The topic absorbs document 495421, "Static Concepts Must Be Types", now dissolved and deleted together with its changelog file. Its principle is a corollary of nominal identity plus the ascent problem, so it survives as a focused topic here rather than an independent document. Heritage record consolidated from that artifact's retired changelog: originating design decision production-validated for years in memar-go; first committed 2026-07-08; drafted across six recorded revisions on 2026-07-08/09 — Super Z (GLM) drafting, ChatGPT (GPT-5.5) reframing the rationale around Concept-vs-Data and clarifying MUST/SHOULD criteria, Claude establishing Immutable Infrastructure's logical independence and deferring exhaustiveness to tooling; Go-specific analysis split to a memar-go companion document on 2026-07-09; migrated to the Explanation-facet template earlier today; dissolved hours later when a layer-lens review assigned roughly half its content to Modeling (classification) and Khayyam tooling (enforcement, codegen, cross-language). The redistribution above is exhaustive; nothing of value was discarded, and the classification thread continues in modeling.md. A second completion pass over the source immediately before final deletion closed the last gaps this entry now carries: the "only identity mechanism left" justification inside the MUST, the conceptual-shift drawback, the Rust/Swift enum trade-off and the industry-drift prior-art observation, the family-member graduation clause (recorded in type.practice.md), and the Pending scope notes for the future tooling documents above. A third relocation, prompted by review, moved the Immutable Infrastructure compatibility analysis out of this ledger into immutable_infrastructure.md itself — its proper explanatory home — leaving this ledger a pointer rather than a parking place for substantive prose.

---

### Rules-and-invariants framing absorbed; relations stub dissolved as redundant
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Propagates to:
  - modeling.changelog.md: Done — the companion stub `type-concepts_vs_data.md` was absorbed into modeling.md in the same pass (its subject matter is modeling-layer); see that file's entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: review and merge the small type-series companions into the strong documents.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — reviewed, applied.

#### Summary
Two more pre-facet stubs dissolved after lens review. `type-rules_and_invariants.md` contributed two framings "Type and Rules" now states up front: a rule exists at the modeling level while implementation code merely executes it (the checking code is one realization, not the rule), and rule ownership follows the constrained concept — belonging to the Type or Relation that governs it, with an explicit cross-link to Modeling's constraint-ownership principle. `type-relations.md` added nothing: its promotion criterion, graph perspective, Ownership example, and simple-association contrast were all already carried by "Type and Relations" — and its one blanket claim ("Edges are Types") was rejected as contradicting Modeling's edge taxonomy, under which shortcut edges and loop-edge labels are precisely the edges that do not become independent concepts.

---

### Type Metadata topic added; type-metadata stub absorbed
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed, argued: no new declaration keywords for Type metadata; needs are carried by the Type's own constructs and companion artifacts. Refined the framing in review: access expectations span behavior invocation as much as state; multilingual identity is each Type's single-source-of-truth duty (propagated to other languages via generated output), never a scattered-files accommodation; and this foundational document must not reference downstream specifications such as Khayyam, which is shaped by the Type definition, not the reverse.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — drafted, applied.

#### Summary
Added "Type Metadata" as an Explanation topic, sibling to "Type Categories vs Language Keywords", extending the anti-keyword philosophy from categories to metadata. Three families, three carrying answers: **access** — for state and for behavior invocation alike — handled by encapsulation by construction plus methods governing their own invocation levels, making keywords like `private` surface-restatements that imply openness were the default; **implementation intent** — carried by ordinary first-class constructs (an intent-declaring Abstraction composed into the definition, or a plainly named Method), since such requirements are circumstance-dependent and numerous, syntax is closed and shared, keyword approaches tax every reader (the coloring cost), and precedent shows ceremony without stronger guarantees; **human-facing identity** — localized names, labels, documentation, and failure descriptions held in companion artifacts beside the definition as part of the Type's single source of truth, propagated to downstream languages through generated output, never dispersed into disconnected translation files. Absorbs dissolved stub ID 000018, whose Status had been mis-recorded as Proposed — corrected here: Memar documents remain Draft; nothing in the framework is near finalization. The stub's concrete file-naming realization was deliberately not carried: it belongs to downstream specifications, pending their own validation. A completion pass then restored the stub's fuller texture as three `####` subsections: the four-place fragmentation pathology (behavior, re-expressed validation, lookup-keyed display strings) behind the single-source-of-truth refusal; machine-queryable first-class companion artifacts replacing parallel mappings and string-keyed lookups (with the annotation-based-localization distinction — external resources resolved by lookup vs. first-class parts of the definition); the regenerate-not-re-translate rule for added implementation languages; and the accepted translator-workflow cost with its tooling mitigation. A review pass then removed an unintended exhaustivity reading: the intro now states the three families are recorded because they recur, not because they complete the set — every family, recorded or future, receives the same treatment (carrier chosen between first-class constructs and companion artifacts, never syntax), and the closing paragraph generalizes the question from "what keyword?" to "which explicit carrier?".

---

### Explicit Behavior Ownership absorbed (document 495466 dissolved)
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Propagates to:
  - type.practice.md: Done — operational section added ("Behavior ownership": the three local questions, delegation visibility rules, no-defaults, codegen transparency, runtime-injection prohibition, macro-boundary test, decision flowchart and delegation-sequence diagrams).
  - khayyam-polymorphism.md: Done — familiarity link and the document-495466 reference repointed here.
  - khayyam-polymorphism.changelog.md: Done — Cited URI repointed.
  - khayyam-inheritance.md: Done — its front-matter citation URI was already broken (`./explicit_behavior_ownership.md`, missing the `type-` prefix); now points here.
  - protocol.md: Done — two mentions linked (the split-history note annotated as absorbed; the Unresolved-questions EBO reference linked).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, directed: core EBO principle; the inheritance-concept critique across its legal and genetic home domains and the directive that the inheritance taxonomy has no valid subject; the extension-not-inheritance terminology for abstraction relationships. Present across the document's entire life — from authoring the principle through directing this dissolution into type.md without any summarization, including routing the operational-residue check toward practice.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted, argued: initial draft of the original EBO material; created the ownership graph models and mermaid diagrams; produced the formal two-condition EBO definition.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM) — rewrote, enriched: split the original monolithic Protocol document into three focused documents; carried working-notes content in (Ownership Discovery Cost, Death of Abstraction, AI-era cost model reconsideration, Boilerplate-vs-Understanding Cost, Trade-Off Reconsideration, the Error Example, the Behavior Owner hypothesis, macros as compile-time execution, and the Social Inheritance Analogy relocated from khayyam-inheritance as a general design-principle argument); restructured to template; authored the independent legal/genetic inheritance critique; enhanced the AI-era argument (explicit code as structural advantage) and added the cognitive-finiteness argument; strengthened enforcement-gap analysis with Java/C# convention evidence; reframed the macro boundary around human cognitive accessibility; corrected protocol-extension carve-outs throughout.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — reviewed, applied: performed the dissolution into type.md with zero-loss redistribution (Explanation topic plus practice section), reference repointing across polymorphism/inheritance/protocol, and this record.

#### Summary
Added "Explicit Behavior Ownership" as a major Explanation topic (~150 lines before its Discussion bundle), preserving the dissolved document in full: the Single Visible Ownership principle with its two-condition formal rule and the three always-local questions (where defined / why available / who owns); delegation-as-visibility semantics with the acyclic single-path ownership graph; the seven-mechanism hidden-behavior catalog with the meta-observation that debates are really about ownership/visibility/discoverability; the complete legal-and-genetic critique of the inherited metaphor (hereditas, farāʾiḍ, genotype/phenotype) concluding the taxonomy-has-no-subject position and the extension-not-inheritance terminology; the death-of-abstraction pattern with the is_retryable ownership analysis and the behavior-owner hypothesis; the generics topic carrying all four paragraphs including the generics-as-symptom argument and the domain-specific-capsule answer; the full economics chain (write-once/read-many, opportunity cost and cognitive finiteness, the AI-era collapse of the trade-off, boilerplate as AI-legibility mechanism with the variable-names analogy); both mermaid ownership-graph figures plus tooling implications; and a topic-level Discussion bundle carrying all four Drawbacks, five Rationale-and-alternatives entries, seven Prior-art items with their common-thread observation, five Unresolved questions, and five Future possibilities. One structural improvement: the former Dependency-on-Modeling section became an ownership-flow paragraph inside "Type and Modeling," where it belongs directionally. Heritage notes: the document itself was born by splitting the monolithic Protocol document, unifying four earlier per-mechanism rejection documents; the reviewer maxim "protocols and explicit implementations reduce cognitive load" is preserved by this record. Citations dispositioned: Protocol and Modeling dependencies are satisfied by body links; the Type self-dependency dissolved with absorption; the khayyam-polymorphism Applied_in relation survives as polymorphism's inbound links, repointed. Status correction recorded per current policy: the dissolved document said Proposed — everything remains Draft.

---

### Creation, absorbing the operational content of "Static Concepts Must Be Types"
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Cited:
  - [Type](./type.md) — Depends_on: this practice operationalizes that document's principles (nominal identity, stateless Types, category model) as steps; every rule here derives from it.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: directed that pre-facet micro-documents be dissolved into strong Explanation documents plus sufficient Practice documents, so an agent needing only the how reads one lean file without inheriting false assumptions from argumentative history.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted: composed this procedure from the retired document's operational content and type.md's principles.

#### Summary
Created `type.practice.md` per `documentation-practice.md`'s Practice-facet schema (two-field front matter, imperative body). Absorbed the operational layer of the dissolved *Static Concepts Must Be Types* document (495421): the Type-qualification checklist, the category-choice table, the static-concept mapping rules with their detection test and gray zones, the multi-outcome abstraction-return pattern with its dispatch-vs-identification distinction, and the `Err` naming convention. Deliberately excluded everything argumentative (rejected alternatives, prior art, rationale) — those live in type.md and in that artifact's consolidated heritage record under type.changelog.md — and routed concept-existence questions to modeling practice, since classification was never a type-layer decision. A completion audit added two further clauses from the source: family-member graduation (a member acquiring genuine per-instance data becomes a data carrier while static members stay distinct) and the note that other static-concept families record their own naming conventions. A third pass, cross-checking an external review's gap list, restored the framework's review maxim ("polymorphism is about code reuse, not about teaching the compiler how to do its job") and the interim manual-completeness-discipline note, both of which had survived nowhere verbatim after dissolution. The same pass surfaced the exhaustiveness mechanism candidates (code-generator metadata; whole-program analysis; Kotlin sealed classes and Swift closed hierarchies as prior art over compiler-known closed sets of Types) into step 4 itself, so they no longer live only in type.changelog.md's Pending ledger.

---

### Type Identity stub dissolved
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Propagates to:
  - type.practice.md: Done — the stub's sole non-redundant asset, the apartment illustration (color differences leave one Type; an ownership relation may itself be a Type because it carries independent meaning), absorbed into the qualification step.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: review and merge the small type-series companions into the strong documents.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied.

#### Summary
Dissolved `type-identity.md`, a 42-line pre-facet stub, after a lens review found every claim already carried by a deeper home: identity-as-modeling-decision → "Type and Modeling" here plus Modeling's justification criteria; the identity-sources list (domain meaning, lifecycle, behavior ownership, relationships, rules, external recognition) → the qualification checklist ("external recognition" being this document's already-stated "domain participants recognize, name, and reason about"); attributes-describe-vs-identity-defines-existence → "What Is Not a Type" plus Modeling's Attribute-or-Edge Test; language-as-expression-not-source → "Type Beyond Programming Languages" and "Type vs Implementation Type". Its title also collided with this document's own deeper "Type Identity" section, so it could never have remained standalone without confusion. The conventions document's mention of the filename is a naming-pattern example, not a content reference, and needed no change.

---

### Absorption of the individual type-companion documents
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: dissolve the single-topic companions into the strong documents and this practice file, with no summarization loss. Supplied the metadata framings (access expectations span behavior invocation as much as state; multilingual identity is each Type's single-source-of-truth duty).
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied.

#### Summary

**From `type-identity.md`** (42-line stub): the apartment illustration absorbed into the qualification step — color differences leave one Type; an ownership relation may itself be a Type because it carries independent meaning. Everything else already lived in deeper homes (type.md's Type Identity / What Is Not a Type / Beyond Programming Languages; modeling.md's justification criteria), so nothing further was imported.

**From `type-metadata.md`** (ID 000018): new "Carrying Type metadata" section — construct-first answers for access and intent signals (never surface keywords); one companion artifact per required language beside the Type's definition, all sharing a single base name qualified by the target language (e.g. `TypeName-detail.en` / `TypeName-detail.fa`); localized names, labels, documentation, and failure descriptions live there, never inline or in external translation maps; regenerate-not-re-translate when an implementation language is added; translator-edits-without-developer-round-trips edge case; plus a routing rule for any unlisted metadata family (carrier by audience: tools/logic → constructs, humans/volume → companion artifacts — then record the decision).

**From `type-explicit_behavior_ownership.md`** (ID 495466): new "Behavior ownership" operational section — the three always-local questions (where defined / why available / who owns); delegation written as a visible call so what/where/why read in place, navigation reserved for depth; never default-implement — generate explicit methods from the single source instead; generated code must land in readable, auditable source files, never intermediates; multiple delegation targets allowed, each explicit; runtime injection (dynamic proxies, reflection-added methods) prohibited; the macro/generation boundary tested by human cognitive accessibility; and two relocated operational diagrams — the EBO decision flowchart and the Processor→Validator delegation sequence.

`type-rules_and_invariants`, `type-relations`, and `type-concepts_vs_data` were reviewed in the same series but left no practice-layer residue: their why-level content went to type.md and modeling.md respectively (see those changelogs).
