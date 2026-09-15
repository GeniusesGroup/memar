# Modeling Handoff

Open work for `modeling.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Models Are Not Reality
1. Should Memar prescribe specific modeling formalisms, or remain formalism-agnostic?
2. How should models be versioned and evolved alongside the systems they describe?

### One Reality, Multiple Abstraction Lenses
1. Should the recurring lenses (structural, behavioral/process, normative, systemic) ever be named formally as part of Memar's vocabulary, or remain descriptive?
2. By what observable signal does a modeler distinguish "two lenses on one concern" from "two concerns observed through one lens"?

### The Model as the Primary Artifact
1. How much modeling maturity is "sufficient" before implementation begins? Is there a measurable threshold, or does this remain a judgment call?
2. Can a lightweight checklist be derived from the graph-stability indicators to make "sufficient maturity" more objectively evaluable?

### Graphs as a Modeling Tool
1. Should Memar eventually prescribe a concrete graph notation (nodes as rectangles, edges as labeled arrows, etc.), or is the freedom to use any notation a deliberate strength?
2. How should graphs from different modeling sessions be merged or compared when no standard notation exists?

### Edge Types and Their Traditional Counterparts
1. As further recurring ordinary-edge roles are named in practice, should any of them ever graduate into something more formal than descriptive vocabulary (e.g. a required annotation), or should the list remain permanently open and informal?
2. When one conceptual relationship is meaningfully traversable in both directions between two concerns, does the model declare a single relationship Type observed from two directions, or two distinct relationship Types — and where does the identity of a relationship reside: in the relationship itself, in each directional representation, or elsewhere? Answering this requires storage-semantics decisions that modeling.md deliberately does not make.
3. Which Module hosts a relationship whose endpoints belong to different Modules — either endpoint, both, or an independent third home — remains open. Hosting decisions made primarily for repository convenience tend to encode false conceptual ownership (see [Modularity](./modularity.md)).
4. When a Thing acquires a type, the model expresses this as a loop-edge (a dynamic, in-graph type upgrade). Implementations sometimes express the same fact statically instead (e.g., compile-time interface embedding, where a Department is always a Group by definition). What is the criterion for choosing between the mechanisms? The working hypothesis — static typing when the type is always and definitionally the parent type, loop-edge when the type may be acquired dynamically at runtime — has not been validated against real cases.

### Graph Stability as an Indicator of Model Maturity
1. Is there a minimum number of modeling sessions required before graph stability becomes a meaningful indicator? Three? Five?
2. How should "fundamental restructuring" be distinguished from "expected refinement" when evaluating whether new requirements force boundary changes?

### Modeling Before Implementation
1. Should Memar prescribe a specific modeling methodology (event storming, domain storytelling, etc.), or remain methodology-agnostic?
2. How should the cost of late model changes be estimated to help teams decide whether additional modeling investment is justified?

### Concept Existence vs. Model Existence
1. What are the formal criteria — beyond "independent responsibility and lifecycle" — for abstraction justification? Can these criteria be made measurable?
2. How should the system handle a concept that starts as derived but later evolves to carry independent responsibilities? Is this a model evolution or a new abstraction introduction?

### Classification Emerges From Rules and Relations, Not From Intrinsic Labels
1. How should a modeler distinguish, in practice, a loop-edge that is only ever going to remain a loop-edge (like `Status`) from one that is a genuine promotion candidate, before the independent-responsibility test can be fully evaluated?
2. When a label is promoted into its own node, what happens to relationships that were previously expressed as loop-edges on the base node under that label — are they automatically migrated to the newly promoted node, or does that require deliberate, manual re-modeling?
3. The topic's premise is that before classification, an artifact may be viewed as unclassified content. Is that a universal base — could anything exist that is not content, and so cannot be viewed this way — or only a methodological stance that happens to cost nothing to adopt?
4. Rules are the criterion a classification is measured against here. Is a Rule itself content that the model must represent, with this topic's own test applied to it, or only the instrument a modeler wields? [Modularity → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) and [Separating Structure (Code) from Policy (Rule)](#separating-structure-code-from-policy-rule) each take a piece of this without settling it.
5. The dissolved draft cited three Memar principles by name — "Reality First", "Definition-Centric", "Discovery Before Design" — and no document registers those names. Each points at a position that does exist descriptively: [Models Are Not Reality](#models-are-not-reality), the Definition-governs-usage rule in [Terminology](./terminology.md), and "Discovery precedes design" in [Content](./content.md). Whether these three should carry canonical names at all, and where the names would be registered, is a Terminology question this topic's cross-references would inherit.

### Acquired Data vs. Discovered Data
1. When a discovered value becomes expensive to recompute (e.g., an aggregation over a very large history of acquired data), at what point is it legitimate to also persist it as a cached, non-authoritative copy — and how should that copy be modeled so it is never mistaken for an acquired fact?

### Modeling State Change as Events, Not Destructive Updates
1. What criteria distinguish a state change worth preserving as history from one that can be safely treated as a destructive update?
2. Should this concern be formalized as a distinct capability interface (analogous to the `Internal`, `Temporary`, `Timeout` capability interfaces used elsewhere in Memar's error abstraction) that a concern can opt into, rather than being an implicit property of every concern?

### Constraints Belong to the Constraining Concern
1. When multiple independent constraints affect overlapping sets of resources and their effects interact, what composition semantics should the model establish for evaluating their combined result?
2. Under what conditions is it legitimate to persist an evaluated constraint result as a cached, non-authoritative projection, and how should such a cache remain re-derivable under the discipline established for shortcut edges (see [Edge Types and Their Traditional Counterparts](./modeling.md#edge-types-and-their-traditional-counterparts))?

### Domain Decomposition over Aggregate-Root Modeling
1. What happens when two composition-layer widgets need the same aggregation but with slightly different validation rules? Is this handled by the abstractions themselves (context-aware validation) or by the aggregators (decorating the abstractions)?
2. Should there be a convention or lint rule that prevents an abstraction from directly accessing another abstraction's internal state, even when both are assembled by the same aggregator?

### Extensible Behavior Belongs to Pluggable Modules
1. [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) now gives the general test (independent behavioral boundary and lifecycle, checked against a stated concern rather than declared). Whether this test is sufficient on its own to decide when a concept's variations must become pluggable Rule modules, or whether Rule attachment needs an additional criterion beyond ordinary Module boundary justification, is not yet resolved.
2. How does a concept like `Invoice` declare, at the model level, which attachment points exist and what a Rule attaching to one is expected to provide — without reintroducing the fixed, anticipatory contract the section otherwise avoids?

### Separating Structure (Code) from Policy (Rule)
1. What is the internal representation of a Rule node's condition (declarative expression, reference to an external function, decision table, etc.)?
2. How are conflicts between multiple applicable Rules on the same Code element resolved (precedence, specificity ordering, explicit override edge)?
3. How is a Rule's temporal validity (effective date, amendment, repeal) tracked, and how does it interact with historical edges created under a now-superseded Rule? This directly affects auditability, which matters most in high-stakes domains such as tax and dispute resolution.
4. What is the precise boundary test for "this condition must be a Rule" vs. "this constraint is inherent enough to remain Code"? [What Earns Foundational Status](./modularity.md#what-earns-foundational-status) gives an analogous test for foundational membership; no equivalent exists yet for the Code/Rule line.
5. The section treats Rule as a first-class graph node, while [Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) treats *Rule* as a provisional name for a Module's optional relationship to another Module. Whether these are two views of one concept, or whether the graph-node framing should be replaced by the module framing, is not resolved there.
6. Where does the rule-engine live architecturally, and how does it query the graph efficiently at the scale this framework targets?

### Document-level
1. Should Memar prescribe specific modeling workshops or exercises (e.g., event storming, domain storytelling) as part of the standard modeling process, or should the modeling technique remain entirely up to the team?
2. How should modeling be integrated into CI/CD pipelines? Can model quality be automatically checked (e.g., detecting cycles in the dependency graph, flagging abstractions without clear responsibilities)?
3. What is the recommended approach when a team inherits a legacy system with no existing model? Should they model from scratch and migrate, or incrementally extract the model from the existing codebase?

## Anticipated Work

- A future document could define a lightweight graph notation tailored to Memar's modeling needs, designed to be expressive enough for architectural discovery while remaining simple enough to be sketched on a whiteboard or in a plain-text editor. (From the Graphs-as-a-Modeling-Tool topic.)
- A future document should define an abstraction-justification checklist — a set of questions that, when answered for a given concept, produce a clear recommendation on whether it deserves an independent abstraction. This would reduce the subjectivity inherent in the current "responsibility-driven" judgment. (From the Concept-Existence topic.)
- A future document could formalize the loop-edge-to-node promotion mechanism as part of a broader graph notation, addressing how classification-in-progress is represented during a modeling session versus how it is finalized once a label is promoted. (From the Classification topic.)
- A future document could define the relationship between the state-history modeling concern and Memar's eventual persistence/storage architecture, including how event history is expected to be queried, without prescribing a specific storage engine. (From the Events-not-destructive-updates topic.)
- A future document could define a formal "aggregation contract" — a lightweight protocol that specifies what an aggregator may and may not do with the abstractions it assembles, including constraints on accessing internal state, propagating errors, and managing lifecycle. (From the Domain-Decomposition topic.)
- The shared Modularity document should define how a concern declares an attachment point, how a Rule module registers against one, and how conflicts between multiple attached Rules (e.g. two discount Rules on the same `Invoice`) are resolved — none of which modeling.md takes a position on. (From the Pluggable-Modules topic.)
- Rule versioning and temporal-validity tracking as a dedicated sub-model; Rule composition/inheritance (e.g., a jurisdiction-level Rule as a base that organization-level Rules can narrow but not widen); and a formal "Domain Boundary Criteria" treatment generalizing, in framework terms, when a new node/edge type is warranted vs. when something should remain a label or a Rule (related to, but distinct from, the foundational-status test in [Modularity](./modularity.md#what-earns-foundational-status)). (From the Code/Rule topic.)
- A future document could define a model-quality linter — an automated tool that checks a graph for common modeling anti-patterns such as circular dependencies, overly broad abstractions, or concepts without clear responsibility boundaries. (Document-level.)
- A future document could address the transition path from legacy systems to Memar-structured models, including strategies for incremental model extraction and migration. (Document-level.)
