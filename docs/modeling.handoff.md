# Modeling Handoff
Open work for `modeling.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### What a Model Is
1. The owner holds that a system is studied, and understood, only once it is described in the language of mathematics, and that a qualitative reading is admissible only where the science is silent and there is no time to answer by its own methods — and must not be abused (recorded 2026-10-08 in the `organization` project, `bundles/supply-chain/supply-chain.changelog.md`, *Deliberation*, attributed to Omid Hekayati). The first half is already this topic's position: every system is modelable in mathematics, and a natural-language account is a report of a system's Types, not a substitute for stating them. The second half is stated nowhere, and it meets a sentence it would have to amend: this topic says Memar "prescribes no notation and no method for how a model is constructed or read", while the owner's position ranks methods — a mathematical description first, a qualitative reading only as a bounded fallback. Open: whether that ranking belongs here as a limit on the agnosticism, or in [Cognition](./cognition.md) as a norm on how a thinker reaches understanding that this topic then cites; and what makes the fallback checkable — who judges that the science is silent, what counts as no time, and what a qualitative reading must record so that a later mathematical description can replace it.

### Models Are Not Reality
1. How should models be versioned and evolved alongside the systems they describe?

### One Reality, Multiple Abstraction Lenses
1. Should the recurring lenses (structural, behavioral/process, normative, systemic) ever be named formally as part of Memar's vocabulary, or remain descriptive?

### The Model as the Primary Artifact
1. Can a lightweight checklist be derived from the graph-stability indicators to make "sufficient maturity" more objectively evaluable? The eighth step is now the checkable form this item asked for, so what remains open is narrower: whether the gate's own pass condition should be derived from graph-stability indicators rather than stated as the single test it is now.
2. [sqlc](https://sqlc.dev) is registered 2026-10-04 from a retired session note, unexamined, as a working instance of the position this topic states: a declared source of truth, and code generated from it rather than written beside it, so a change to the declaration reaches the implementation without a human editing both. What examining it would test is the boundary - the declaration is a schema and the generated code is a query layer, so whether this counts as one concern realized twice or as two concerns, one derived from the other, is the same question this document asks of every derived concept.

### Graphs as a Modeling Tool
1. How should graphs from different modeling sessions be merged or compared when no standard notation exists?
2. [ent](https://entgo.io) is registered 2026-10-04 from a retired session note, unexamined, as a test of this document's own position that a graph is not a documentation artifact: a schema is declared in code and a graph layer is generated from it deterministically, so the graph sits upstream of the implementation rather than being a picture of it. Whether that is the same arrangement this document means by a model, or a different one wearing the same word, is what examining it would settle.

### Edge Types and Their Traditional Counterparts
1. As further recurring ordinary-edge roles are named in practice, should any of them ever graduate into something more formal than descriptive vocabulary (e.g. a required annotation), or should the list remain permanently open and informal?
2. When one conceptual relationship is meaningfully traversable in both directions between two concerns, does the model declare a single relationship Type observed from two directions, or two distinct relationship Types — and where does the identity of a relationship reside: in the relationship itself, in each directional representation, or elsewhere? Answering this requires storage-semantics decisions that modeling.md deliberately does not make.

### Graph Stability as an Indicator of Model Maturity
1. Is there a minimum number of modeling sessions required before graph stability becomes a meaningful indicator? Three? Five?
2. Whether a signal can be read *during* a session rather than only across sessions is a different question, held at [Early Indicators of Modeling Progress](#early-indicators-of-modeling-progress); this one is retrospective by construction and cannot answer it.

### Modeling Before Implementation
1. How should the cost of late model changes be estimated to help teams decide whether additional modeling investment is justified?

### Early Indicators of Modeling Progress
1. The topic states that graph stability cannot guide a team's first few sessions and that a smaller set of earlier, session-level signals can indicate convergence, then supplies none. Recovered 2026-10-04 from a retired session file: five candidate criteria were proposed there and never ruled on — least duplication of responsibility, least conceptual overlap, least mutual dependency, greatest stability under requirement change, and greatest reusability. Two are already governed elsewhere and cannot stand as indicators in their own form: least responsibility duplication is this document's independent-responsibility criterion ([Concept Existence vs. Model Existence](#concept-existence-vs-model-existence)), and least mutual dependency is a dependency-direction question belonging to [Modularity](./modularity.md). A third is in tension with what this document already holds — greatest reusability is stated as a corroborating signal that is explicitly not required, since the absence of reuse does not disqualify a concept from independent-abstraction status ([Reuse Across Contexts as an Additional Signal](./modeling.md#reuse-across-contexts-as-an-additional-signal)) — so whether it may serve as a stability signal at all, in a place where it deliberately does not gate, is the part that needs a ruling. What is left genuinely unexamined is whether the two structural candidates are observable early enough to act on within a first session, and whether greatest stability under requirement change is checkable at all before the requirements it is stable against have had occasion to change.
2. Whether these candidates are indicators of progress or criteria of maturity is itself unsettled, and the two roles ask different questions: an indicator is read during a session to decide what to do next, a criterion is applied afterwards to judge whether the work is finished. [Graph Stability as an Indicator of Model Maturity](#graph-stability-as-an-indicator-of-model-maturity) is a criterion of the second kind, which is the reason this topic exists separately rather than as a third question there.

### Concept Existence vs. Model Existence
1. What are the formal criteria — beyond "independent responsibility and lifecycle" — for a concept to earn a model element of its own, and can they be made measurable? The other half of this question is settled: a concept has semantic identity and so is a Type, and what is separate is whether it is stated as an element of its own or as an attribute, derived representation, or contextual view of another Type ([Modeling → Concept Existence vs. Model Existence](./modeling.md#concept-existence-vs-model-existence)).

### Classification Emerges From Rules and Relations, Not From Intrinsic Labels
1. The topic's premise is that before classification, an artifact may be viewed as unclassified content. Is that a universal base — could anything exist that is not content, and so cannot be viewed this way — or only a methodological stance that happens to cost nothing to adopt?
2. Rules are the criterion a classification is measured against here. Is a Rule itself content that the model must represent, with this topic's own test applied to it, or only the instrument a modeler wields? [Modularity → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) and [Separating Structure (Code) from Policy (Rule)](#separating-structure-code-from-policy-rule) each take a piece of this without settling it.
3. The dissolved draft cited three Memar principles by name — "Reality First", "Definition-Centric", "Discovery Before Design" — and no document registers those names. Each points at a position that does exist descriptively: [Models Are Not Reality](#models-are-not-reality), the Definition-governs-usage rule in [Terminology](./terminology.md), and "Discovery precedes design" in [Content](./content.md). Whether these three should carry canonical names at all, and where the names would be registered, is a Terminology question this topic's cross-references would inherit.

### Modeling State Change as Events, Not Destructive Updates
1. Should this concern be formalized as a distinct capability interface (analogous to the `Internal`, `Temporary`, `Timeout` capability interfaces used elsewhere in Memar's error abstraction) that a concern can opt into, rather than being an implicit property of every concern?

### Constraints Belong to the Constraining Concern
1. When multiple independent constraints affect overlapping sets of resources and their effects interact, what composition semantics should the model establish for evaluating their combined result?
2. Under what conditions is it legitimate to persist an evaluated constraint result as a cached, non-authoritative projection, and how should such a cache remain re-derivable under the discipline established for shortcut edges (see [Edge Types and Their Traditional Counterparts](./modeling.md#edge-types-and-their-traditional-counterparts))?

### Separating Structure (Code) from Policy (Rule)
1. What is the internal representation of a Rule node's condition (declarative expression, reference to an external function, decision table, etc.)?
2. How are conflicts between multiple applicable Rules on the same Code element resolved (precedence, specificity ordering, explicit override edge)?
3. What is the precise boundary test for "this condition must be a Rule" vs. "this constraint is inherent enough to remain Code"? [What Earns Foundational Status](./modularity.md#what-earns-foundational-status) gives an analogous test for foundational membership; no equivalent exists yet for the Code/Rule line.
4. Where does the rule-engine live architecturally, and how does it query the graph efficiently at the scale this framework targets?

### Edge identity and reification
1. Does an ordinary edge carry its own addressable identity — independently of promotion to a node or a Type? The rejected blanket claim "Edges are Types" (type.changelog.md, *Rules-and-invariants framing absorbed* entry) settled that not every edge becomes an independent concept, but it left open the prior capability: addressing a specific edge in order to attach another edge to it (an annotation, a guarantee, a supersession), which graph-based modeling sessions have assumed when giving every edge its own identifier and letting edges terminate other edges. The edge taxonomy is silent on whether edges are first-class addressables at this minimal level.

### Document-level
1. How should modeling be integrated into CI/CD pipelines? Can model quality be automatically checked (e.g., detecting cycles in the dependency graph, flagging abstractions without clear responsibilities)?
2. What is the recommended approach when a team inherits a legacy system with no existing model? Should they model from scratch and migrate, or incrementally extract the model from the existing codebase?

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
