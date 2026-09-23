# Type Changelog

## Changelog

The seven entries below are migrated from `type.md`'s former `## Change Rationale` section. They were developed across research sessions between the document's Start Date (2026-07-19) and its first commit (2026-07-20); individual timestamps were never recorded, so each carries `Time: unknown` and only their relative order is reliable. Contributor attribution follows the surviving records — the former front-matter `Contributors` field plus each revision's own description — which pinned some rounds to specific reviewers and left the applier unrecorded; where history did not name who applied a change, no applier is invented here. The former front-matter `Citations` list is carried on the entry that added it (fourth revision, below); the two citations the base document's own readers still need — its dependency on Modeling and its pointers to the Khayyam companion documents — now live as ordinary links in the base document's body instead.

### Initial draft
- Time: unknown (historical import)
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued

#### What changed
- Established the foundational concepts of the document: Type as a Semantic Entity, Type and Modeling, Capsule and Abstraction as realizations of Type, Type and Rules, and Type and Relations.
- Authored the initial reflections on Type as a semantic entity and its relationship with Capsule and Abstraction.
- Directed the philosophical framing of Type as an independent concept considered before its manifestation in Khayyam.

---

### Restructuring into the document template, with cross-language research
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — researched, rewrote

#### What changed
- Restructured the document to follow the then-current formal template.
- Conducted the cross-language and type-theoretic research.
- Added Type Identity, Type vs Implementation Type, the rule categories, Capsule/Abstraction bridge analysis, and unresolved questions based on cross-language research.

---

### Primitive types removed; Method and Scope added as categories
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote

#### What changed
- Corrected structural errors based on review feedback: removed Primitive Types (Khayyam has none), added Method as a Type category (`mt`), added Scope as a Type category (`sc`), repositioned the definition of Type as an independent concept before its manifestation in Khayyam, reduced overall length by consolidating repetitive comparative analysis, and aligned the category model with Khayyam's actual four-subtype structure (`cp`, `mt`, `ab`, `sc`).
- Applied the corrections across multiple revision iterations.

#### Deliberation
- Method was identified as a type category, and the absence of primitive types in Khayyam (Omid Hekayati — argued).
- Assumptions about primitive types were corrected (Omid Hekayati).
- The independent-concept-first structure was emphasized (Omid Hekayati).

---

### Alignment with the companion documents
- Time: unknown (historical import)
- Type: Changed
- Cited:
  - [Modeling](./modeling.md) — Depends_on: Type is the result of correct modeling; the concept of Type cannot be understood independently of the modeling process that identifies what should exist as a Type, and Modeling establishes that abstractions are justified by independent responsibilities, not by data.
  - [Encapsulation in Khayyam](./khayyam/encapsulation.md) — Reference: specifies how Capsule and Method manifest in Khayyam — Sovereign Encapsulation, method invocation rules, and the rejection of tuples and consumer-side mutability keywords.
  - [Abstraction in Khayyam](./khayyam/abstraction.md) — Reference: specifies pure behavioral specifications, implicit structural satisfaction, rejection of default implementations, and abstraction composition.
  - [Inheritance in Khayyam](./khayyam/inheritance.md) — Reference: inheritance is a relationship between abstractions, not between capsules — behavior transfer rejected, abstraction extension supported.
  - [Polymorphism in Khayyam](./khayyam/polymorphism.md) — Reference: classifies the polymorphism forms Khayyam supports through abstraction conformance — inclusion, parametric, and ad-hoc — and the rejection of generic syntax.
  - [Khayyam](./khayyam/khayyam.md) — Reference: documents the recurring principles (Behavior Over Type Identity, Domain Modeling, Syntactic Atomicity) that the Type concept in Khayyam instantiates, and is the canonical specification of Khayyam's type subtypes and their syntax.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2) — rewrote

#### What changed
- Incorporated findings from the companion documents (Encapsulation, Abstraction, Inheritance, Polymorphism, Modeling) into the document.
- Resolved the Type Identity open question about structural satisfaction vs. nominal identity by referencing the Abstraction document's treatment of implicit structural satisfaction and accidental satisfaction risk.
- Added the relationship between inheritance and Type categories (inheritance between Abstractions, not Capsules).
- Added the Modeling document's "Concept Existence vs. Model Existence" principle to the decision framework.
- Refined the Methodology section to reflect the actual research approach.

---

### Critical-review round: exclusive boundary, hierarchy position, and the weakened bridge claim
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — reviewed, argued
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — reviewed
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed

#### What changed
- Applied critical review from ChatGPT (GPT-5.5): (1) removed all references to DDD and Aggregate Root — these belong in companion documents, not in the Type definition; (2) added "What Is Not a Type" to establish the exclusive boundary of the definition, addressing the risk that an overly inclusive definition dilutes the concept; (3) moved the Type-hierarchy question from Unresolved to an official position — "Type Categories Are Not a Hierarchy," categories connected through semantic relationships rather than taxonomic classification; (4) strengthened the Scope category as a "semantic boundary" defining visibility, ownership, composition, and isolation, not merely a syntactic block; (5) improved the Method-as-Type argument — Methods are Types because they are the fundamental semantic building blocks through which higher-level concepts (rules, vouchers, policies) are expressed, not merely because they have identity and contract; (6) weakened the bridging claim to "currently the primary mechanism" connecting Capsules and Abstractions rather than the definitive bridge; (7) clarified Method lifecycle as definition, composition, specialization, and execution — not runtime creation/destruction; (8) added the conservative-expansion principle, avoiding the OOP-style overloading that rendered "Object" meaningless; (9) recorded Method-as-Type as an unresolved question, well-motivated but not yet validated through implementation; (10) removed the "Beyond DDD" subsection from Type and Modeling.

#### Deliberation
- Flagged the Method-as-Type argument weakness, the Scope justification gap, the Type-definition exclusivity concern, and the DDD reference overhead (Omid Hekayati — recorded in the former Contributors field; the surviving history does not tie this review to a single numbered pass).
- Flagged the Method-as-Type argument weakness, the Scope-as-Type justification gap, the Type-definition exclusivity risk, the DDD reference overhead, the premature bridging claim, and the Type-hierarchy resolution (Claude — recorded against the preceding revision's state; the surviving history does not tie this review to a single numbered pass).

---

### Consistency fixes: relations table, Scope identity, and de-duplication
- Time: unknown (historical import)
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, argued

#### What changed
- Applied critical review from Claude, cross-checked against `khayyam.md`: (1) replaced the parent-child tree diagram under "The Relationships Between Categories" with a relation table, since the tree's visual shape contradicted the adjacent "Type Categories Are Not a Hierarchy" claim; (2) resolved a direct contradiction in the Scope section — the claim that a Scope's identity derives from its containing Method conflicted with the independent-identity criterion; containment within a method body is now framed as a syntactic placement constraint, distinct from Scope's independent semantic identity; (3) reframed "Type and Relations": a Relation presupposes the Types it connects and therefore operates one layer above this document's concern, deferring first-class-Relation questions (endpoint ownership, directionality, arity) to a future companion document, and "Manifestation in Khayyam" no longer lists first-class relations among realized principles, since Khayyam does not currently manifest them; (4) strengthened the Method-as-Type argument with the distinguishing property — independent, referenceable existence (signature, cross-file import, receiver-independent attachment, composition) — closing a circularity gap where the prior argument could equally apply to any executable construct; (5) removed duplication between "How to identify a Type" and "What Is Not a Type," the former now pointing to the latter for the negative-criteria catalog.

---

### Placement-based Scope justification withdrawn; identification framework generalized
- Time: unknown (historical import)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — reviewed, argued

#### What changed
- Applied a second round of critical review from ChatGPT (GPT-5.5): (1) removed the placement-based justification for Scope entirely rather than merely softening it — the claim that Scope "must" live inside a Method is documented as Khayyam's current syntax/usage pattern (a language-layer concern, deferred to `khayyam.md`), not a defining property; (2) added "A note on independent identity" generalizing the fix beyond Scope: independent identity is a claim about meaning, not about existing free of any containing context — a parameter has identity distinct from its Method despite being confined to that Method's signature; (3) added "Why Only Four Categories?" — a Type category is justified only by a fundamental semantic role irreducible to specialization, composition, or usage pattern of an existing category; Rule, Relation, Protocol, Workflow, and Policy depend on Types without justifying distinct categories; (4) added "Type Categories vs Language Keywords," a mapping showing common keywords elsewhere (`struct`/`class`/`record`, `interface`/`trait`, `function`/`procedure`, `namespace`/`module`/`package`) as typically realizations of Capsule, Abstraction, Method, or Scope — a dedicated keyword elsewhere does not imply a distinct foundational concept; (5) added "Type Beyond Programming Languages" to the Introduction — Type is not introduced by programming languages; Khayyam's prominence here reflects its role as the first concrete manifestation of these principles, not a claim that Type originates in language.

#### Deliberation
- The second critical-review round was cross-examined and refined through discussion (ChatGPT).

---

### Migration to the Explanation-facet template with a paired changelog
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- This document is now structured per `documentation-explanation.md` with no provenance in its front matter or body: the former `Applied to`, `Citations`, and `Contributors` front-matter fields and the `## Change Rationale` section are migrated entirely into this file (entries above).
- Two in-body sentences that referenced the removed `Citations` field were reworded (Methodology; "Manifestation in Khayyam"), and plain-text mentions of the documents the reader genuinely needs while reading — `modeling.md` (in "Type Categories Are Not a Hierarchy" and "Type and Modeling"), `terminology.md`, and the Khayyam companion documents — became ordinary hyperlinks, per the rule that reader-needed sources link directly in the body while argumentative provenance lives only here.
- Performed the migration described in this entry (ox-alpha).

#### Deliberation
- Asked that this document be upgraded to the current documentation methodology, moving provenance into a paired changelog file (Omid Hekayati — requested).

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, applied

#### What changed
- Added "Stateless Types" under Type vs Implementation Type, opening with the governing principle — identity belongs to the type system, answerable from the Type alone at compile time, never from runtime data.
- The topic carries the three-role decomposition table (Identity → type system/compile time; Behavior → methods; Data → fields/runtime), the MUST that stateless concepts be carried as their own named entities, the ascent-problem framing of data-simulated identity, boundary clauses against over-splitting and structural reasoning and family-resemblance-as-qualification, and a Drawbacks note recording the accepted proliferation/API-surface trade-off.
- The topic absorbs document 495421, "Static Concepts Must Be Types", now dissolved and deleted together with its changelog file.
- Its principle is a corollary of nominal identity plus the ascent problem, so it survives as a focused topic here rather than an independent document.
- Heritage record consolidated from that artifact's retired changelog: originating design decision production-validated for years in memar-go; first committed 2026-07-08; drafted across six recorded revisions on 2026-07-08/09 — Super Z (GLM) drafting, ChatGPT (GPT-5.5) reframing the rationale around Concept-vs-Data and clarifying MUST/SHOULD criteria, Claude establishing Immutable Infrastructure's logical independence and deferring exhaustiveness to tooling; Go-specific analysis split to a memar-go companion document on 2026-07-09; migrated to the Explanation-facet template earlier today; dissolved hours later when a layer-lens review assigned roughly half its content to Modeling (classification) and Khayyam tooling (enforcement, codegen, cross-language).
- The redistribution above is exhaustive; nothing of value was discarded, and the classification thread continues in modeling.md.
- A second completion pass over the source immediately before final deletion closed the last gaps this entry now carries: the "only identity mechanism left" justification inside the MUST, the conceptual-shift drawback, the Rust/Swift enum trade-off and the industry-drift prior-art observation, the family-member graduation clause (recorded in type.practice.md), and the Pending scope notes for the future tooling documents above.
- A third relocation, prompted by review, moved the Immutable Infrastructure compatibility analysis out of this ledger into immutable_infrastructure.md itself — its proper explanatory home — leaving this ledger a pointer rather than a parking place for substantive prose.
- Authored the new topic from the source's principle core; performed the dissolution and cross-document redistribution (ox-alpha).

#### Deliberation
- Pre-facet micro-documents predate Memar's documentation principles; the end state is strong Explanation documents plus sufficient Practice documents, with citations pointing at Type and Modeling generally so downstream work inherits principles instead of a private vocabulary (Omid Hekayati).
- The lens analysis that motivated dissolution was reviewed (Omid Hekayati).

---

### Rules-and-invariants framing absorbed; relations stub dissolved as redundant
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Propagates to:
  - modeling.changelog.md: Done — the companion stub `type-concepts_vs_data.md` was absorbed into modeling.md in the same pass (its subject matter is modeling-layer); see that file's entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied.

#### What changed
- Two more pre-facet stubs dissolved after lens review.
- `type-rules_and_invariants.md` contributed two framings "Type and Rules" now states up front: a rule exists at the modeling level while implementation code merely executes it (the checking code is one realization, not the rule), and rule ownership follows the constrained concept — belonging to the Type or Relation that governs it, with an explicit cross-link to Modeling's constraint-ownership principle.
- `type-relations.md` added nothing: its promotion criterion, graph perspective, Ownership example, and simple-association contrast were all already carried by "Type and Relations" — and its one blanket claim ("Edges are Types") was rejected as contradicting Modeling's edge taxonomy, under which shortcut edges and loop-edge labels are precisely the edges that do not become independent concepts.

#### Deliberation
- Directed the review and merge of the small type-series companions into the strong documents (Omid Hekayati).

---

### Type Metadata topic added; type-metadata stub absorbed
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed, argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, applied.

#### What changed
- Added "Type Metadata" as an Explanation topic, sibling to "Type Categories vs Language Keywords", extending the anti-keyword philosophy from categories to metadata.
- Three families, three carrying answers: **access** — for state and for behavior invocation alike — handled by encapsulation by construction plus methods governing their own invocation levels, making keywords like `private` surface-restatements that imply openness were the default; **implementation intent** — carried by ordinary first-class constructs (an intent-declaring Abstraction composed into the definition, or a plainly named Method), since such requirements are circumstance-dependent and numerous, syntax is closed and shared, keyword approaches tax every reader (the coloring cost), and precedent shows ceremony without stronger guarantees; **human-facing identity** — localized names, labels, documentation, and failure descriptions held in companion artifacts beside the definition as part of the Type's single source of truth, propagated to downstream languages through generated output, never dispersed into disconnected translation files.
- Absorbs dissolved stub ID 000018, whose Status had been mis-recorded as Proposed — corrected here: Memar documents remain Draft; nothing in the framework is near finalization.
- The stub's concrete file-naming realization was deliberately not carried: it belongs to downstream specifications, pending their own validation.
- A completion pass then restored the stub's fuller texture as three `####` subsections: the four-place fragmentation pathology (behavior, re-expressed validation, lookup-keyed display strings) behind the single-source-of-truth refusal; machine-queryable first-class companion artifacts replacing parallel mappings and string-keyed lookups (with the annotation-based-localization distinction — external resources resolved by lookup vs. first-class parts of the definition); the regenerate-not-re-translate rule for added implementation languages; and the accepted translator-workflow cost with its tooling mitigation.
- A review pass then removed an unintended exhaustivity reading: the intro now states the three families are recorded because they recur, not because they complete the set — every family, recorded or future, receives the same treatment (carrier chosen between first-class constructs and companion artifacts, never syntax), and the closing paragraph generalizes the question from "what keyword?" to "which explicit carrier?".

#### Deliberation
- No new declaration keywords for Type metadata; needs are carried by the Type's own constructs and companion artifacts (Omid Hekayati).
- Refined the framing in review: access expectations span behavior invocation as much as state; multilingual identity is each Type's single-source-of-truth duty (propagated to other languages via generated output), never a scattered-files accommodation; and this foundational document must not reference downstream specifications such as Khayyam, which is shaped by the Type definition, not the reverse (Omid Hekayati).

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, directed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted, argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM) — rewrote, enriched
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied

#### What changed
- Added "Explicit Behavior Ownership" as a major Explanation topic (~150 lines before its Discussion bundle), preserving the dissolved document in full: the Single Visible Ownership principle with its two-condition formal rule and the three always-local questions (where defined / why available / who owns); delegation-as-visibility semantics with the acyclic single-path ownership graph; the seven-mechanism hidden-behavior catalog with the meta-observation that debates are really about ownership/visibility/discoverability; the complete legal-and-genetic critique of the inherited metaphor (hereditas, farāʾiḍ, genotype/phenotype) concluding the taxonomy-has-no-subject position and the extension-not-inheritance terminology; the death-of-abstraction pattern with the is_retryable ownership analysis and the behavior-owner hypothesis; the generics topic carrying all four paragraphs including the generics-as-symptom argument and the domain-specific-capsule answer; the full economics chain (write-once/read-many, opportunity cost and cognitive finiteness, the AI-era collapse of the trade-off, boilerplate as AI-legibility mechanism with the variable-names analogy); both mermaid ownership-graph figures plus tooling implications; and a topic-level Discussion bundle carrying all four Drawbacks, five Rationale-and-alternatives entries, seven Prior-art items with their common-thread observation, five Unresolved questions, and five Future possibilities.
- One structural improvement: the former Dependency-on-Modeling section became an ownership-flow paragraph inside "Type and Modeling," where it belongs directionally.
- Heritage notes: the document itself was born by splitting the monolithic Protocol document, unifying four earlier per-mechanism rejection documents; the reviewer maxim "protocols and explicit implementations reduce cognitive load" is preserved by this record.
- Citations dispositioned: Protocol and Modeling dependencies are satisfied by body links; the Type self-dependency dissolved with absorption; the khayyam-polymorphism Applied_in relation survives as polymorphism's inbound links, repointed.
- Status correction recorded per current policy: the dissolved document said Proposed — everything remains Draft.
- Core EBO principle; the inheritance-concept critique across its legal and genetic home domains and the directive that the inheritance taxonomy has no valid subject; the extension-not-inheritance terminology for abstraction relationships (Omid Hekayati).
- Initial draft of the original EBO material; created the ownership graph models and mermaid diagrams; produced the formal two-condition EBO definition (ChatGPT).
- Split the original monolithic Protocol document into three focused documents; carried working-notes content in (Ownership Discovery Cost, Death of Abstraction, AI-era cost model reconsideration, Boilerplate-vs-Understanding Cost, Trade-Off Reconsideration, the Error Example, the Behavior Owner hypothesis, macros as compile-time execution, and the Social Inheritance Analogy relocated from khayyam-inheritance as a general design-principle argument); restructured to template; authored the independent legal/genetic inheritance critique; enhanced the AI-era argument (explicit code as structural advantage) and added the cognitive-finiteness argument; strengthened enforcement-gap analysis with Java/C# convention evidence; reframed the macro boundary around human cognitive accessibility; corrected protocol-extension carve-outs throughout (Super Z).
- Performed the dissolution into type.md with zero-loss redistribution (Explanation topic plus practice section), reference repointing across polymorphism/inheritance/protocol, and this record (ox-alpha).

#### Deliberation
- Present across the document's entire life — from authoring the principle through directing this dissolution into type.md without any summarization, including routing the operational-residue check toward practice (Omid Hekayati).

---

### Creation, absorbing the operational content of "Static Concepts Must Be Types"
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Cited:
  - [Type](./type.md) — Depends_on: this practice operationalizes that document's principles (nominal identity, stateless Types, category model) as steps; every rule here derives from it.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- Created `type.practice.md` per `documentation-practice.md`'s Practice-facet schema (two-field front matter, imperative body).
- Absorbed the operational layer of the dissolved *Static Concepts Must Be Types* document (495421): the Type-qualification checklist, the category-choice table, the static-concept mapping rules with their detection test and gray zones, the multi-outcome abstraction-return pattern with its dispatch-vs-identification distinction, and the `Err` naming convention.
- Deliberately excluded everything argumentative (rejected alternatives, prior art, rationale) — those live in type.md and in that artifact's consolidated heritage record under type.changelog.md — and routed concept-existence questions to modeling practice, since classification was never a type-layer decision.
- A completion audit added two further clauses from the source: family-member graduation (a member acquiring genuine per-instance data becomes a data carrier while static members stay distinct) and the note that other static-concept families record their own naming conventions.
- A third pass, cross-checking an external review's gap list, restored the framework's review maxim ("polymorphism is about code reuse, not about teaching the compiler how to do its job") and the interim manual-completeness-discipline note, both of which had survived nowhere verbatim after dissolution.
- The same pass surfaced the exhaustiveness mechanism candidates (code-generator metadata; whole-program analysis; Kotlin sealed classes and Swift closed hierarchies as prior art over compiler-known closed sets of Types) into step 4 itself, so they no longer live only in type.changelog.md's Pending ledger.
- Composed this procedure from the retired document's operational content and type.md's principles.

#### Deliberation
- Directed that pre-facet micro-documents be dissolved into strong Explanation documents plus sufficient Practice documents, so an agent needing only the how reads one lean file without inheriting false assumptions from argumentative history (Omid Hekayati).

---

### Type Identity stub dissolved
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Propagates to:
  - type.practice.md: Done — the stub's sole non-redundant asset, the apartment illustration (color differences leave one Type; an ownership relation may itself be a Type because it carries independent meaning), absorbed into the qualification step.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied.

#### What changed
- Dissolved `type-identity.md`, a 42-line pre-facet stub, after a lens review found every claim already carried by a deeper home: identity-as-modeling-decision → "Type and Modeling" here plus Modeling's justification criteria; the identity-sources list (domain meaning, lifecycle, behavior ownership, relationships, rules, external recognition) → the qualification checklist ("external recognition" being this document's already-stated "domain participants recognize, name, and reason about"); attributes-describe-vs-identity-defines-existence → "What Is Not a Type" plus Modeling's Attribute-or-Edge Test; language-as-expression-not-source → "Type Beyond Programming Languages" and "Type vs Implementation Type".
- Its title also collided with this document's own deeper "Type Identity" section, so it could never have remained standalone without confusion.
- The conventions document's mention of the filename is a naming-pattern example, not a content reference, and needed no change.

#### Deliberation
- Directed the review and merge of the small type-series companions into the strong documents (Omid Hekayati).

---

### Absorption of the individual type-companion documents
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied.

#### What changed
- **From `type-identity.md`** (42-line stub): the apartment illustration absorbed into the qualification step — color differences leave one Type; an ownership relation may itself be a Type because it carries independent meaning. Everything else already lived in deeper homes (type.md's Type Identity / What Is Not a Type / Beyond Programming Languages; modeling.md's justification criteria), so nothing further was imported.
- **From `type-metadata.md`** (ID 000018): new "Carrying Type metadata" section — construct-first answers for access and intent signals (never surface keywords); one companion artifact per required language beside the Type's definition, all sharing a single base name qualified by the target language (e.g. `TypeName-detail.en` / `TypeName-detail.fa`); localized names, labels, documentation, and failure descriptions live there, never inline or in external translation maps; regenerate-not-re-translate when an implementation language is added; translator-edits-without-developer-round-trips edge case; plus a routing rule for any unlisted metadata family (carrier by audience: tools/logic → constructs, humans/volume → companion artifacts — then record the decision).
- **From `type-explicit_behavior_ownership.md`** (ID 495466): new "Behavior ownership" operational section — the three always-local questions (where defined / why available / who owns); delegation written as a visible call so what/where/why read in place, navigation reserved for depth; never default-implement — generate explicit methods from the single source instead; generated code must land in readable, auditable source files, never intermediates; multiple delegation targets allowed, each explicit; runtime injection (dynamic proxies, reflection-added methods) prohibited; the macro/generation boundary tested by human cognitive accessibility; and two relocated operational diagrams — the EBO decision flowchart and the Processor→Validator delegation sequence.
- `type-rules_and_invariants`, `type-relations`, and `type-concepts_vs_data` were reviewed in the same series but left no practice-layer residue: their why-level content went to type.md and modeling.md respectively (see those changelogs).

#### Deliberation
- Directed the dissolution of the single-topic companions into the strong documents and this practice file, with no summarization loss (Omid Hekayati).
- Supplied the metadata framings: access expectations span behavior invocation as much as state; multilingual identity is each Type's single-source-of-truth duty (Omid Hekayati).

---

### Added "Concepts Outlive Their Labels"
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- New topic stating the concept-over-label discipline in both directions — wholesale vocabulary rejection losing wrapped concepts, and name multiplication splitting one concept into apparent kinds — with the FP/OOP encapsulation case as the recorded example and the framework's own rejections as the exercised pattern.
- The topic was written with the three-question test (which concept did the label wrap; does it survive independent of the packaging; what explicitly replaces the packaging's function) so future rejections are checkable; the encapsulation argument was grounded in Khayyam's own no-primitive-types design (W32/Bool/String capsules as encapsulation doing its work); the memory dichotomy case was cross-linked; the "too obvious to record" rejection was recorded.

#### Deliberation
- The pattern was brought from Omid's public discussions: functional-programming communities reject object-oriented vocabulary wholesale while remaining fully dependent on the wrapped concepts — encapsulation being the sharp case, since without it even a primitive type cannot be defined (representation must hide behind operations for any value to hold its own invariants) (Omid Hekayati).
- Directed that the pattern be recorded in this document (the Type concept being itself a casualty of label-vs-concept confusion) alongside the framework's own inverse exercises of the same discipline (aggregate-root rejection keeping aggregation, dichotomy rejection keeping both retention needs, behavior-transfer rejection keeping requirement extension) (Omid Hekayati).

---

### Documentation-method migration completed: Discussion wrappers, Rationale, Prior art, Unresolved questions, Future possibilities dissolved per the finalized method
- Time: 2026-09-07T00:00:00Z
- Type: refactor
- Propagates to:
  - type.handoff.md: Created - open questions and future possibilities moved there.
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Super Z - applied the finalized documentation method).
- The document-level `Drawbacks`, `Rationale and alternatives`, and `Prior art` content preserved below; `Unresolved questions` and `Future possibilities` moved to the paired handoff (Super Z).

Dissolved every `#### Discussion` wrapper (How to identify a Type, Definition of Type, Type Identity, Stateless Types, the four-categories topic, Type and Modeling, EBO, Type and Rules, Concepts Outlive Their Labels, Type and Relations) and the document-level `## Discussion`; drawback statements folded into their topics as inline content; rejected alternatives, comparative prior art, document-level Drawbacks, open questions, and future possibilities relocated without loss. (Super Z)

#### Considered and not done
- **No framework, rely on intuition (rejected; migrated from the identification topic's retired `Rationale and alternatives`)**: without guidance, the tendency is to over-type or under-type without consistency.
- **A strict checklist with binary answers (rejected; migrated from the identification topic's retired `Rationale and alternatives`)**: domain modeling is not binary. The responsibility criterion reduces the gray zone but does not eliminate it — that is a feature, not a flaw.
- **Define Type structurally (rejected; migrated from the Definition topic's retired `Rationale and alternatives`)**: a structural definition fails to capture the modeling-level distinction. Two concepts with the same structure are not necessarily the same concept.
- **Define Type as a formal type-theoretic construct (considered, deferred; migrated from the Definition topic's retired `Rationale and alternatives`)**: Martin-Löf Type Theory defines types through introduction, elimination, and computation rules. This is rigorous but may be too formal for the current stage. A future revision could strengthen the definition toward this formalism.
- **Structural typing (rejected; migrated from the Type-Identity topic's retired `Rationale and alternatives`)**: two Types with the same structure would be interchangeable, defeating semantic identity. TypeScript's structural typing demonstrates this: `interface Person { name: string }` and `interface Company { name: string }` are interchangeable, which is precisely the conflation this principle prevents.
- **Behavioral typing (considered, insufficient alone; migrated from the Type-Identity topic's retired `Rationale and alternatives`)**: two Types are the same iff they support the same operations. But `Age` and `Height` both support arithmetic, yet should not be interchangeable. Behavioral typing alone is insufficient without nominal anchoring.
- **Unify Capsule and Abstraction (rejected; migrated from the four-categories topic's retired `Rationale and alternatives`)**: this loses the essential distinction between "owns state" and "defines contract." Scala's experience with stateful traits demonstrates the problems of unification.
- **Treat Method as a separate concept from Type (rejected; migrated from the four-categories topic's retired `Rationale and alternatives`)**: Methods *are* Types. Making them non-types would prevent them from being imported, composed, and referenced through the same mechanism — breaking the orthogonality of the type model. It would also remove the natural bridging unit between Abstractions and Capsules.
- **Treat Method as a kind of Capsule (considered, not chosen; migrated from the four-categories topic's retired `Rationale and alternatives`)**: a method is a "callable capsule" in spirit, but calling it a Capsule obscures the fundamental distinction: a Method's primary purpose is executability, not state ownership. The categories should reflect semantic role, not implementation similarity.
- **Treat Scope as a compiler construct, not a Type (considered, not chosen; migrated from the four-categories topic's retired `Rationale and alternatives`)**: if Scope were merely syntactic, it would not qualify. But Scope establishes semantic boundaries — visibility, ownership, composition, isolation — that are relevant to the type model. These properties justify its inclusion as a Type category.
- **Reject each hidden-behavior mechanism individually (rejected; migrated from the EBO topic's retired `Rationale and alternatives`)** — "no inheritance," "no trait defaults," "no promotion," "no macro methods" was the earlier, per-document approach. Unifying under EBO means future, unimagined mechanisms are evaluated automatically against one rule: does this introduce behavior without explicit, visible ownership? A growing blacklist cannot do that.
- **Allow controlled hidden behavior (rejected; migrated from the EBO topic's retired `Rationale and alternatives`)** — e.g., defaults permitted on abstractions marked pure, or embedding restricted to interface-like targets. Exceptions erode principles: each creates a category to learn and police, and any permission for hidden behavior reopens the exact problem EBO closes — there is no practically definable safe subset, and each exception demands its own enforcement, review, and documentation, consuming what it promised to save. Ecosystem evidence settles the enforcement question: successful Java and C# teams already follow EBO-like conventions ("prefer composition over inheritance," "no deep hierarchies") enforced through reviews, linters, and institutional knowledge — fragile, incomplete, expensive. If a convention is near-universal among high-performing teams, encode it in the language and let the compiler enforce it for free.
- **Rely on tooling to expose hidden behavior (rejected; migrated from the EBO topic's retired `Rationale and alternatives`)** — IDEs annotating inherited methods still place the visibility burden on tools rather than source. Source is the ground truth; if understanding a component requires an IDE, it has already failed. Code review web interfaces, PR diffs, and printed code all lose tool-provided annotations.
- **Define inheritance precisely and permit only that form (rejected; migrated from the EBO topic's retired `Rationale and alternatives`)** — e.g., allowing "protocol extension only." This engages a taxonomy whose subject does not exist: extension is already correctly named and already outside EBO's scope. Granting "precise inheritance" legitimacy re-imports the inapplicable concept; the honest naming is explicit delegation for implementations and extension for protocols.
- **Doing nothing (the cost; migrated from the EBO topic's retired `Rationale and alternatives`)** — without a unifying ownership principle, each mechanism gets debated in isolation, producing inconsistent decisions and ad-hoc rules, with developers navigating hidden behavior through fragile tooling, documentation, and tribal knowledge.
- **Treating labels and concepts as inseparable (rejected; migrated from the Concepts-Outlive-Their-Labels topic's inline considered-and-rejected paragraph)**: that is how whole toolchains get rejected for their names — the FP-overcorrection — and how a framework ends up re-deriving discarded concepts later, under new names, without the record of why.
- **Leaving the concept-over-label pattern unrecorded as too obvious (rejected; migrated from the same paragraph)**: the error recurs at every scale — language communities, framework reviews, and this project's own discussions have all seen it; the named pattern with its three-question test is what makes the next occurrence checkable instead of re-argued.
- **Adopt a traditional type system and enforce modeling through conventions (rejected; migrated from the document-level retired `Rationale and alternatives`)**: this works when the team has strong discipline and fails when it does not. The goal is to make discipline enforceable.
- **Adopt a dependent type system (rejected for now; migrated from the document-level retired `Rationale and alternatives`)**: too complex for the current stage. Refinement types may be added as a middle ground in future revisions.

#### Considered and not done (topic-level drawbacks relocated per owner ruling)
- **Any decision framework risks false precision.** The responsibility-based criterion helps, but responsibility itself can be a matter of perspective — what looks like an independent responsibility to one modeler may look like a derived view to another; and the lifecycle criterion requires careful interpretation — broadened to include definition and composition stages, nearly every named artifact can be argued to have a "lifecycle," weakening the criterion's discriminating power. (Migrated from the identification topic)
- **Defining Type as "first-class modeled entity" sets an expectation a type system may not meet:** if "modeled entity" is merely a naming convention — semantically distinct Types treated as interchangeable because they share structure — the claim is aspirational, and any language claiming semantic types must ensure the type system can observe and enforce the distinction. (Migrated from the Definition topic)
- **Nominal typing creates composability barriers structural typing avoids:** with `Age` and `Height` distinct, no single `max(a, b)` covers both without an explicit abstraction; this is the cost of semantic precision — and its benefit, preventing accidental conflation of distinct concepts. (Migrated from the Type-Identity topic)
- **Requiring one named entity per stateless concept proliferates Types** — accepted deliberately, with such Types expected from code generators rather than hand authorship (the manual path's weight is a signal of intent); each concrete Type in public signatures becomes breaking-change surface, judged worthwhile because compile-time-checked identity is the higher-priority guarantee; and the rule demands a conceptual shift from treating identifiers (errors, statuses, permissions) as values — the framework's philosophy grounds the shift, but adoption friction is real. (Migrated from the Stateless-Types topic)
- **Four categories increase the conceptual burden:** developers must decide not only "should this be a Type?" but "what category?"; the distinction is clear in principle but blurry in practice, and the identification framework is less immediately intuitive for Method and Scope than for Capsule and Abstraction. (Migrated from the four-categories topic)
- **Modeling-gated type introduction raises prototyping friction.** A type system derived from modeling principles must provide mechanisms for gradual introduction — lightweight types strengthenable as the model matures — without requiring full modeling justification from the start. (Migrated from the Type-and-Modeling topic)
- **EBO's costs, stated plainly:** increased boilerplate (explicit delegation instead of inheritance, substantially reduced in AI-assisted environments where generation and lint-scaffolding produce the delegation — the remaining lines purchase visible ownership, shifting the trade-off to "more code AND clear behavior"); initial development speed (early hierarchies are shallow and verbosity feels unnecessary; the comprehension benefit compounds as the codebase grows); pattern migration (teams accustomed to inheritance-based design must reformulate Template Method and inheritance-based Strategy with composition and delegation — with the hidden benefit that principled deviation from OO norms filters for practitioners who think critically about trade-offs, as the Go and Rust communities demonstrate); and generated-code management (heavy reliance on generation demands reliable, auditable generators and workflow discipline around generated artifacts). (Migrated from the EBO topic)

#### Considered and not done (from the removed document-level Drawbacks section)
- **The gap between aspiration and specification**: the claim that Types are "semantic entities" sets an expectation that the type system can verify semantic properties. Without a formal definition of "semantic identity" and without specifying the Capsule/Abstraction realization mechanism in full detail, the claim is philosophical rather than technical. This is acceptable for a Draft but must be addressed before Proposed status.
- **The absence of primitives**: while eliminating primitives solves the ascent problem, it creates a bootstrapping challenge — what are the foundational Capsules that everything else builds on, and how are they defined without circularity? An implementation concern that affects the Type model's coherence.

#### Related work
- Martin-Löf's intuitionistic type theory treats types as meaningful propositions. OWL's named classes carry semantic identity beyond their property definitions. Neither fully aligns with the position taken here — MLTT is more formal but at a different abstraction level; OWL is declarative without behavioral semantics. (Migrated from the Definition topic's retired `Prior art`)
- Rust's struct/trait distinction parallels Capsule/Abstraction, but Rust treats functions as separate from the type system. OCaml's structure/signature distinction is similar but also separates functions from types. Khayyam's "Method as Type" is a genuinely different position — closer to Smalltalk's "everything is an object" but with explicit type categories rather than a single uniform concept. (Migrated from the four-categories topic's retired `Prior art`)
- EBO's language survey: Go interfaces (default-free, aligned — but embedding implicitly promotes methods, which EBO rejects); Java interfaces pre-8 (pure, aligned — Java 8 default methods moved away); Rust traits (default methods and blanket implementations inject behavior the implementing type's source does not define); C# extension methods (behavior visible in IntelliSense but absent from the type's source); Python and duck typing (monkey patching, multiple inheritance, metaclass manipulation violate ownership clarity in favor of flexibility); C++ multiple inheritance (concrete-body MI creates diamond-ownership ambiguity; the single-owner rule eliminates the class of problem); Ada generics (compile-time composition explicit in instantiation — partially aligned, though resulting behavior remains hard to trace). The common thread: every listed language treats "inheritance" (or its equivalents) as a coherent concept to refine, restrict, or work around; EBO's position is that the concept itself — as a model for behavioral transfer — is what fails examination, not particular implementations. (Migrated from the EBO topic's retired `Prior art`)
- Martin-Löf Type Theory (types as meaningful entities defined by formal rules — this document shares the aspiration but lacks MLTT's rigor); Rust (struct/trait distinction parallels Capsule/Abstraction, but Rust treats functions as separate from types; Khayyam does not); Eiffel (Design by Contract parallels rules owned by Types; Eiffel's runtime checking is the most mature implementation); Alloy (relations as foundational entities — first-class relations are viable and powerful); Smalltalk ("everything is an object" parallels "everything is a Type," but Smalltalk lacks explicit type categories). Khayyam's contribution is not any single one of these ideas but their integration: a unified type model where Capsules, Methods, Abstractions, and Scopes are all Types; Methods are currently the primary mechanism connecting Capsules and Abstractions; inheritance is placed between Abstractions while behavior transfer between Capsules is rejected; and polymorphism operates through abstraction conformance rather than generic syntax — all derived from the principle that Type is a modeling decision, not a compiler convenience. (Migrated from the document-level retired `Prior art`)

---

### Structure Is Fixed by Definition added; runtime-registration governance re-derived from it
- Time: 2026-09-09T00:00:00Z
- Type: Added
- Propagates to:
  - type.practice.md: Done — the runtime-registration edge case now cites the new principle alongside step 3's forbidden pattern; the up-reference to the relocated protocol document removed.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — argued, drafted

#### What changed
- Added "Structure Is Fixed by Definition" (the structural twin of Explicit Behavior Ownership): a running system executes its definition and never establishes structure — the system's Structure (in System's sense: the capabilities and constraints it exposes and enforces) is established at definition time in the artifact; every capability increase enters execution only through a new artifact. Three boundary clauses: selection among established alternatives is execution, not structural change; runtime inputs are data; platform consumption is not structure acquisition.
- The runtime-concept-registration governance that had pointed up to the Immutable Infrastructure protocol document is now derivable from this document's own layer — the new principle plus step 3's forbidden pattern — so type.practice.md holds no reference up to the protocol layer projected onto it; the runtime-logic-entry question is named without citation as convergent and owned by the framework's protocol documents.
- The deployment working-out of the principle (immutable infrastructure) remains owned by the protocols layer; this document states the type-level rule that document realizes.

#### Deliberation
- The re-derivation was directed after the relocation attempt had repointed base documents up into protocols/: base documents may not reference the protocol layer projected onto them, and the fix should take the same shape as Explicit Behavior Ownership — a named base-layer principle all documents cite, rather than descriptive restatements scattered across documents (Omid Hekayati — directed).
- The principle's ground is the identity model: runtime-minted structure would be structure carried as data — the ascent problem at system scale, demoting identity and capability alike from decided to encountered (Super Z — argued).
- The first draft of the section enumerated Structure as "concepts, capabilities, and the composition binding them"; corrected against [System](./system.md#structure)'s definition — Structure is capabilities and constraints, explicitly not the arrangement of parts — before any commit (Omid Hekayati — caught; Super Z — corrected).

#### Considered and not done
- Alternative names: "Definition-Execution Separation" and "Single Definition Authority". "Structure Is Fixed by Definition" was kept because System already defines Structure precisely (capabilities and constraints, explicitly not the arrangement of parts) and the title anchors the principle to that defined home; the separation framing survives in the boundary clauses rather than the name.

---

### Definition sections made Khayyam-independent
- Time: 2026-09-10T00:00:00Z
- Type: Fixed
- Cited:
  - [Khayyam](./khayyam/khayyam.md) — Depends_on: this document's realization layer, whose placement (`docs/khayyam/`) and citation rule were registered in the same session
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) — applied

#### What changed
- The *Type Identity* topic's structural-satisfaction paragraph no longer presents implicit satisfaction as a Khayyam property and no longer tracks the language layer's state ("recorded as an open question in the Abstraction document" removed): structural satisfaction is stated as a way a language may realize conformance, the accidental-satisfaction tension is kept, and the mitigation question is named as a language-design question owned where the conformance mechanism itself is defined — a body tracks its own layer's state only.
- The Capsule definition's realization note ("In Khayyam, this is enforced through Sovereign Encapsulation ...") moved to the *Manifestation in Khayyam* section as its own item, where this document's realization claims live; the definition section now ends at the semantic claim.
- The Method definition's "In the Khayyam model" attribution became "In this document's model": Method-as-Type is this document's position, which Khayyam realizes, not a property borrowed from the language.
- The Abstraction composition sentence dropped the "Khayyam's mechanism" attribution: requirement extension is the mechanism defined here; `ab` composition is its realization.
- No definitional content changed — the definitions already stood independently of Khayyam (the Abstract and Introduction had stated that separation explicitly since the document's consolidation); the edits remove the remaining points where realization vocabulary and language-layer state tracking sat inside definition sections.

---

### Abstraction category reworded from contract to specification
- Time: 2026-09-23T05:38:39Z
- Type: Fixed
- Cited:
  - [Protocol](./protocol.md) — Depends_on: Protocol vs Contract defines a contract as parties, obligations, and commitments.
  - [Abstraction in Khayyam](./khayyam/abstraction.md) — Reference: the document-level correction this entry extends to the Type model.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- The Abstract's Khayyam-manifestation sentence now says Abstraction *specifies required behavior*, not *specifies a contract*.
- The Abstraction category section heading is now "Type as Specification"; its definition says Type-level *behavioral specification*.
- Body occurrences tied to the Abstraction category now say specification: fulfilling an Abstraction's specification, compound specifications, specification-level abstraction boundary, implementation-agnostic specification, pure behavioral specifications, and the specification/implementation line for default implementations.
- The four-category justification, the keyword-mapping table's role cell, and the mapping prose now say pure behavioral specification where the role is Abstraction.
- The Manifestation in Khayyam bullet is now "Abstraction as pure specification" with the same body wording.
- The paired type.practice.md category row was aligned; the citation annotation in type.changelog.md's companion-documents entry was updated to match what abstraction.md now specifies.
- Type's own *defined contract* vocabulary (identity/contract as a Type's guarantees), capsule public-interface contract wording, and historical changelog narratives were deliberately left untouched — separate vocabulary questions.

#### Deliberation
- Contract remains a distinct architecture concept; the Abstraction category only declares required behavior (Omid Hekayati — decided).

---

### Manifestation in Khayyam section transferred to the Khayyam specification
- Time: 2026-09-23T07:07:01Z
- Type: refactor
- Propagates to:
  - khayyam/khayyam.md: Done — the realization bullets now live there under "Type Principles Realized", citing down to this document and the companion documents.
  - type.handoff.md: Done — the bootstrapping entry's upward links replaced with plain-text path references (handoff: no entry of its own).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- The "Manifestation in Khayyam" section moved wholesale to `khayyam/khayyam.md` as "Type Principles Realized": No primitive types, Sovereign Encapsulation (the duplicate bullet pair merged during the move), the `tp` keyword, Method as Type, Abstraction as pure specification, Inheritance between Abstractions, and Behavior over type identity. Nothing was dropped — the destination carries the itemized account, with companion links added.
- The Introduction's boundary sentence no longer anchors a local Manifestation section; it now states that how Khayyam realizes these principles is recorded in that language's own documents — prose, no hyperlink: principles first, language second.
- The Scope paragraph and the Concepts Outlive Their Labels paragraph lost their upward hyperlinks into `khayyam/`; the Khayyam specification and the Khayyam inheritance specification are named in prose.

#### Deliberation
- Citations run down: a base document never links into `khayyam/`, so the realization account lives on the realization side, where the citation direction is legal (Omid Hekayati — decided).
