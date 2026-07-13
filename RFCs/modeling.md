---
Title: "Modeling"
Status: Proposed
Start Date: 2026-06-30
RFC Number: 495216
Applied to: []
Related RFCs:
    - Title: "Protocol"
      URI: "./protocol.md"
      Reason: "Depends_on"
      Explanation: "Defines Protocol as a pure declarative specification; modeling produces the domain structures that protocols then constrain."
    - Title: "Terminology"
      URI: "./terminology.md"
      Reason: "Depends_on"
      Explanation: "Terminology governs how concepts are understood across all modeling discussions."
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Titles: ["Core principles", "Domain decomposition", "Capsule justification"]
        URI: ""
        Explanation: "Defined the core modeling philosophy; directed the rejection of aggregate-root ownership and the capsule-responsibility principle."
  - Name: "Gemini"
    URI: "https://gemini.google.com/"
    Model: "3.1 Pro"
    Effort: "Extended thinking enabled"
    Tasks:
      - Titles: ["Initial draft", "Argumentation"]
        URI: ""
        Explanation: "Drafted initial text; argued for and against alternatives; incorporated revisions."
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Tasks:
      - Titles: ["Initial draft", "Argumentation"]
        URI: ""
        Explanation: "Drafted initial text; argued for and against alternatives; incorporated revisions."
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Tasks:
      - Titles: ["Structural revision", "Template compliance", "Content enrichment"]
        URI: ""
        Explanation: "Restructured to comply with RFC Template Specification; wrote Summary and Guide-level explanation; added Discussion bundles, cross-references, and Drawbacks to every topic; fixed front-matter field formats and Related RFCs Reason values."
---

# Modeling

## Summary
This RFC defines how Memar approaches domain modeling: treating the model as the primary architectural artifact, discovering it through graph-based exploration before any implementation commitment, and decomposing the domain around independent responsibilities rather than data ownership or presentation structures. It establishes that a capsule is justified by an autonomous responsibility and lifecycle, not by the existence of data; that adaptability emerges from model quality, not from technology choices; and that behavioral complexity is a modeling smell rather than a requirement. The aggregate-root pattern of conventional DDD is rejected in favor of composing independent capsules at the composition layer, with no single fixed owning entity.

## Motivation
The framework should prevent incorrect models before implementation and reduce the cost of correction when mistakes inevitably occur. In practice, most architectural rigidity does not originate from poor technology choices — it originates from models that conflate unrelated concerns, mirror presentation structures, or bind responsibilities to fixed owning entities. Once a flawed model propagates into databases, APIs, user interfaces, and deployment pipelines, every subsequent correction carries compounding cost. Memar therefore needs an explicit, opinionated modeling discipline that maximizes the quality of the model before implementation begins and preserves the ability to evolve it afterward.

## Guide-level explanation
Modeling in Memar means discovering the natural structure of a domain before writing any implementation code. The output of modeling is not a database schema, not an API definition, and not a class hierarchy — it is a graph of concerns, responsibilities, and relationships that reveals where the real architectural boundaries lie.

The process works in three broad stages. First, identify every concept the domain requires — not by looking at screens, forms, or API endpoints, but by analyzing the language, behavior, and relationships that the domain demands. Second, organize those concepts into a graph: nodes represent concerns or responsibilities, and edges represent the relationships between them. This graph is a discovery tool, not a documentation artifact — its purpose is to expose hidden structures, coupling patterns, and natural boundaries that would remain invisible if you started from implementation-oriented perspectives like database tables or object hierarchies. Third, evaluate which nodes represent genuinely independent concerns (candidates for their own capsules) and which are derived representations, contextual views, or mere data of existing concerns.

A capsule — Memar's fundamental architectural unit — is not justified by the existence of data. A capsule is justified by the existence of an independent responsibility, behavioral boundary, or lifecycle. For example, the fact that a system displays a `DiscountedPrice` does not mean `DiscountedPrice` deserves its own capsule; in most cases it is a calculated view of the fundamental `Price` concern. The modeling challenge is distinguishing between fundamental concepts, derived concepts, data representations, contextual views, and infrastructure structures.

Memar explicitly rejects the conventional DDD aggregate-root pattern where a single "owner" entity (like `User`) directly contains sub-concerns as its own fields and methods. Instead, each concern — `username`, `email`, identity resolution, credential validation — is modeled as its own independent capsule. A composition-layer construct (typically a GUI widget or page) assembles whichever subset of capsules a specific use case needs, without absorbing the internal logic of the concerns it composes. This means "the user" has no single canonical shape; different contexts legitimately require different aggregations of the same underlying concerns.

When behavioral complexity accumulates — special cases, coordination rules, translation layers, synchronization mechanisms — the model should be re-examined before adding implementation complexity. A mature model tends to simplify behavior; an immature model tends to transfer its complexity into implementation.

The practical implication for a team starting a new feature is: resist the urge to open an IDE and start coding. Instead, draw the graph. Challenge every proposed concept against existing ones. Ask whether a genuinely new responsibility exists or whether the proposal is just a contextual specialization of something already modeled. The cost of redesign is lowest during modeling, so the majority of conceptual consolidation should happen before implementation, not after it.

## Reference-level explanation

### The Model as the Primary Artifact
Memar treats the domain model as the primary architectural artifact of a system. The purpose of implementation is not to define the model. The purpose of implementation is to realize a model that has already been discovered and validated. A successful implementation does not prove that a model is correct. It only proves that the model can be implemented. This distinction is important because implementation introduces irreversible costs. Once a model is reflected in databases, APIs, user interfaces, deployment pipelines, integrations, and operational procedures, changing the model becomes increasingly expensive.

For this reason, Memar encourages extensive model exploration before implementation and seeks to minimize the coupling between implementation details and domain concepts. The closer a system keeps its implementation aligned with the model, the easier it becomes to evolve the architecture when new understanding emerges. The model should remain the source of truth. Implementations are merely projections of that truth into specific technological contexts.

#### Discussion

##### Drawbacks
Treating the model as primary requires upfront investment in modeling before any visible implementation progress can be demonstrated. In environments where stakeholders measure velocity by shipping features, this approach can create political friction. Additionally, the claim that "a model can be validated without implementation" is itself limited — some categories of correctness (performance characteristics, storage feasibility, integration compatibility) can only be fully evaluated once an implementation exists.

##### Rationale and alternatives
- **Implementation-driven modeling (rejected)**: starting from code and extracting the model afterward is common in agile practices, but consistently produces models that reflect incidental implementation decisions rather than domain structure. The cost of correcting such models grows with every additional feature built on top of them.
- **Parallel modeling and implementation (considered, not chosen)**: developing the model and implementation concurrently reduces time-to-first-prototype but makes it harder to distinguish model concepts from implementation artifacts during review. Memar permits rapid prototyping for learning purposes but does not treat prototypes as committed implementation.

##### Prior art
The idea that the model precedes and constrains the implementation is central to model-driven architecture (MDA) as defined by the OMG, and to Eric Evans' Domain-Driven Design, which argues that the domain model should be the heart of the software. Memar's contribution is not the principle itself but the specific mechanisms (graph-based discovery, capsule boundaries, protocol separation) that make the principle practically enforceable.

##### Unresolved questions
1. How much modeling maturity is "sufficient" before implementation begins? Is there a measurable threshold, or does this remain a judgment call?
2. Can a lightweight checklist be derived from the graph-stability indicators to make "sufficient maturity" more objectively evaluable?

### Models Must Survive Implementation Changes
A model should not become difficult to change merely because an implementation already exists. One of the primary responsibilities of architecture is to preserve the ability to evolve domain understanding over time. As knowledge grows, previously accepted models may be refined, decomposed, consolidated, or replaced. Such changes should be treated as normal architectural evolution rather than exceptional events.

Memar therefore places significant emphasis on protocols as stable boundaries between models and their implementations. A protocol defines the observable contract of a concern without exposing the implementation decisions behind it. By preserving this separation, implementations can evolve, migrate, or even be completely replaced while minimizing the impact on the surrounding architecture.

For a detailed discussion, see the [Protocol RFC](./protocol.md).

#### Discussion

##### Drawbacks
Protocol boundaries introduce indirection. Every interaction with a capsule must pass through its protocol rather than accessing implementation details directly, which can increase the cognitive overhead of understanding the system, particularly for developers accustomed to directly accessing object internals. There is also a risk of over-abstracting early, creating protocol boundaries around concerns that turn out to be simple enough that the indirection is not justified by any real need for implementation independence.

##### Rationale and alternatives
- **Direct implementation coupling (rejected)**: allowing implementations to depend directly on each other's internals is simpler in the short term but makes any change to a single concern ripple unpredictably across the system. This is the dominant source of rigidity in most software architectures.
- **Shared-database integration without protocol boundaries (rejected)**: this is the de facto pattern in many systems, where different services or modules share a database schema and therefore share each other's structural decisions. It eliminates the indirection but makes any schema change a coordinated, high-risk event.

##### Prior art
The principle that stable interfaces should outlive their implementations is foundational in software engineering, from Parnas' 1972 paper on information hiding to the interface-segregation principle in SOLID design. Memar's protocol concept extends this principle by making it a first-class architectural construct rather than a coding convention.

### Adaptability Emerges from Modeling, Not Technology
Architectural adaptability is often incorrectly attributed to implementation technologies. Technologies such as REST, gRPC, messaging systems, databases, or programming languages can influence development costs, but they do not fundamentally determine the adaptability of a system. The primary factor that determines how easily a system evolves is the quality of its underlying model.

A well-structured model can often survive major implementation changes with limited disruption. A poorly structured model remains difficult to evolve regardless of the technologies used to implement it. For this reason, Memar focuses first on discovering stable conceptual boundaries and only then on selecting implementation technologies.

**Technology choices should serve the model, not define it.**

#### Discussion

##### Drawbacks
This principle can be misinterpreted as license to defer all technology decisions indefinitely. In practice, some technology constraints (regulatory requirements, existing infrastructure, team expertise) may legitimately constrain the model or at least the shape of its capsules. A team that exclusively models without considering technological feasibility risks producing a model that cannot be practically implemented in its target environment.

##### Rationale and alternatives
- **Technology-first architecture (rejected)**: selecting the technology stack and then fitting the domain into it is the dominant industry practice. It produces systems whose structure reflects framework conventions (controllers, repositories, entities) rather than domain boundaries, making the system adaptable to framework changes but not to domain evolution.
- **Full technology agnosticism (considered, not chosen)**: deferring all technology decisions until after modeling is complete is the ideal but may be impractical when the team's expertise or the deployment environment constrains the feasible implementation options. A pragmatic middle ground acknowledges known constraints without allowing them to dictate the model's conceptual structure.

##### Prior art
The observation that architecture is dominated by model quality rather than technology choice echoes arguments in Ralph Johnson's "Frameworks = Components + Patterns" and more recently in the "bounded context" concept from DDD, where the quality of the context boundary matters far more than the technology used within it.

### Modeling Requires Explicit Relationship Analysis
A domain model cannot be discovered by analyzing entities in isolation. Concepts derive much of their meaning from their relationships with other concepts. Therefore, modeling must focus not only on identifying nodes but also on identifying and understanding the relationships that connect them.

Many traditional modeling approaches inherit assumptions from relational database design, where relationships are often reduced to foreign keys, join tables, and storage-oriented structures. As a result, relationships frequently become implementation details rather than first-class modeling concerns.

Memar takes a different approach.

Relationships are architectural information. They often reveal responsibilities, boundaries, ownership, lifecycle dependencies, and behavioral constraints that cannot be discovered by examining concepts independently. A model should therefore be evaluated as a graph of interacting concerns rather than as a collection of isolated structures.

For example, in an e-commerce system, the relationship between `Order` and `Payment` is not merely a foreign-key link — it encodes a lifecycle dependency (an order cannot be considered complete without payment resolution), a temporal constraint (payment must be resolved within a specific window), and a responsibility boundary (the rules governing payment validation belong to the `Payment` concern, not to `Order`). Examining `Order` and `Payment` in isolation would miss all of this.

#### Discussion

##### Drawbacks
Treating every relationship as a first-class modeling concern increases the complexity of the modeling process itself. Not all relationships carry architectural significance — many are purely structural or incidental. The risk is that the modeling effort becomes bogged down in cataloging relationships that have no impact on boundaries or responsibilities, consuming time without producing architectural insight. Distinguishing architecturally significant relationships from incidental ones requires judgment that is difficult to codify.

##### Rationale and alternatives
- **Entity-first modeling (rejected)**: starting by defining entities and their attributes, then adding relationships as an afterthought, produces models where the relationships are shaped by storage convenience rather than domain semantics. This is the dominant approach in ORM-driven development.
- **Relationship-only modeling (rejected)**: focusing exclusively on relationships without grounding them in identifiable concerns produces an abstract graph that is difficult to map to concrete system boundaries. Memar requires both nodes and edges, not one at the expense of the other.

##### Prior art
Graph-based conceptual modeling has roots in entity-relationship modeling (Chen, 1976) and concept maps (Novak, 1984). More recently, knowledge-graph approaches in data engineering treat relationships as first-class entities with their own attributes and lifecycle. Memar applies this principle specifically to software architecture rather than data engineering.

### Graphs as a Modeling Tool
Memar approaches modeling primarily as a graph-discovery activity rather than a schema-design activity. The objective of modeling is not to construct database structures, API payloads, or implementation artifacts. The objective is to discover the natural structure of the domain. Graph representations are particularly valuable because they allow concepts and relationships to be examined independently from implementation technologies. Nodes represent concerns, concepts, responsibilities, or capabilities. Edges represent the relationships that exist between them.

By analyzing graph structure, it becomes possible to identify:
* Natural boundaries
* Responsibility clusters
* Coupling patterns
* Ownership relationships
* Dependency directions
* Potential architectural capsules

This process often reveals structures that remain hidden when modeling is performed through database schemas, object hierarchies, or user-interface layouts. For this reason, graph exploration should precede implementation-oriented design activities whenever possible.

#### Discussion

##### Drawbacks
Graph exploration has no natural stopping criterion. A team can continue discovering new relationships, refining node boundaries, and reorganizing the graph indefinitely, which conflicts with the practical need to begin implementation at some point. Additionally, there is no widely adopted standard for what a "modeling graph" should look like — the lack of a prescribed notation means different teams or different modeling sessions may produce graphs that are difficult to compare or consolidate.

##### Rationale and alternatives
- **Schema-first modeling (rejected)**: starting from database schemas or API definitions anchors the model to implementation decisions too early. The resulting model reflects storage and transport concerns rather than domain structure.
- **Text-first modeling (rejected)**: describing the domain in prose and extracting entities from the text is a common UML-driven practice, but prose descriptions tend to linearize relationships that are inherently graph-structured, causing many cross-cutting concerns to be missed.
- **Formal ontology languages (considered, not chosen)**: using OWL or similar formalisms would provide precise semantics but introduces a tooling and expertise barrier that is disproportionate for most software modeling contexts. Memar uses informal graphs but structures the modeling process around them systematically.

##### Unresolved questions
1. Should Memar eventually prescribe a concrete graph notation (nodes as rectangles, edges as labeled arrows, etc.), or is the freedom to use any notation a deliberate strength?
2. How should graphs from different modeling sessions be merged or compared when no standard notation exists?

##### Future possibilities
A future RFC could define a lightweight graph notation tailored to Memar's modeling needs, designed to be expressive enough for architectural discovery while remaining simple enough to be sketched on a whiteboard or in a plain-text editor.

### Graphs Are Not Documentation Artifacts
In Memar, graphs are not used merely to visualize a model that has already been discovered. Graphs are used as a discovery mechanism. The purpose of graph analysis is to expose relationships, dependencies, responsibilities, and architectural structures that may not be visible through implementation-oriented perspectives.

A graph is therefore not the final documentation of a model. It is one of the primary tools used to discover the model itself. This distinction is important because many modeling approaches treat diagrams as explanatory artifacts produced after design decisions have already been made. Memar instead treats graph exploration as part of the design process itself.

The practical consequence is that a graph is expected to change frequently during modeling. It is a working tool, not a polished deliverable. A graph that has not been revised multiple times during the modeling process is likely a graph that has not been used seriously as a discovery mechanism.

#### Discussion

##### Drawbacks
Treating graphs as disposable working tools means there may be no durable record of the modeling process once implementation begins. If a team revisits a modeling decision months later, the original graph — with all its intermediate states, abandoned alternatives, and rejected structures — may no longer exist. This loss of modeling history can make it difficult to understand why certain boundaries were chosen and others were not, especially when the original modelers are no longer available.

##### Rationale and alternatives
- **Graphs as living documentation (considered, not chosen)**: maintaining the graph as a continuously updated document alongside the codebase keeps the modeling history accessible but introduces an ongoing maintenance obligation. The graph must be updated every time the model evolves, or it becomes misleading. For teams that already struggle with documentation maintenance, this obligation may be unrealistic.
- **Versioned graph artifacts (considered, not chosen)**: committing graph snapshots to version control at each modeling milestone preserves history without requiring continuous maintenance. This approach is promising but has no established convention for graph file formats or commit granularity.

##### Prior art
The distinction between "design as discovery" and "design as documentation" parallels the distinction between exploratory data analysis and confirmatory data analysis in statistics. In both cases, the exploratory phase uses flexible, informal tools, while the confirmatory phase produces structured, auditable artifacts.

### Behavior Often Reveals the Quality of the Model
In Memar, behavior is not treated as an independent concern that is discovered only after structural modeling is complete. A well-formed graph frequently constrains and reveals the space of valid behaviors. As concepts, responsibilities, and relationships become clearer, many behavioral expectations emerge naturally from the model itself. For this reason, unusual behavioral complexity should often be treated as a signal rather than a requirement.

When a system requires an increasing number of special cases, exceptions, coordination rules, translation layers, synchronization mechanisms, or procedural workarounds, the underlying model should be re-examined before additional implementation complexity is introduced. In many cases, behavioral complexity is not evidence of a sophisticated domain. It is evidence that responsibilities, boundaries, or relationships have not yet been modeled correctly.

**A mature model tends to simplify behavior. An immature model often transfers its complexity into implementation.**

#### Discussion

##### Drawbacks
The claim that behavioral complexity signals modeling immaturity can be overapplied. Some domains are genuinely complex — regulatory compliance, multi-currency financial settlement, real-time collaborative editing — and no amount of modeling will eliminate their inherent behavioral complexity. Applying this principle indiscriminately risks creating a culture where legitimate domain complexity is dismissed as a modeling failure, leading to oversimplified models that cannot handle real-world edge cases.

##### Rationale and alternatives
- **Behavior-driven modeling (rejected in its conventional form)**: starting from user stories or behavior specifications and deriving the model from them tends to produce models that reflect usage patterns rather than domain structure. The resulting model may be optimized for current workflows but resistant to unanticipated changes.
- **Separate behavioral and structural modeling (rejected)**: this is the dominant industry practice — model the structure first, then define behavior as methods, handlers, or services. Memar does not treat behavior as a separate phase because behavioral expectations are often the clearest indicator of whether structural boundaries have been drawn correctly.

##### Prior art
This principle resonates with Rich Hickey's "design is about pulling things apart" philosophy and with the notion of "essential complexity" from Fred Brooks' "No Silver Bullet." Memar's contribution is the specific heuristic: when behavioral complexity accumulates, re-examine the model before adding implementation complexity.

### Graph Stability as an Indicator of Model Maturity
Model maturity should not be measured by the number of concepts, capsules, services, or implementation artifacts. Instead, maturity emerges when graph exploration repeatedly converges toward the same structural understanding of the domain.

Indicators of increasing maturity may include:
* Stable responsibility boundaries
* Clear relationship semantics
* Reduced conceptual duplication
* Fewer exceptional behaviors
* Reduced need for translation layers
* Reduced synchronization concerns
* Consistent protocol definitions

A mature model does not eliminate change. Rather, it reduces the frequency with which new requirements force fundamental restructuring of existing boundaries. As understanding improves, implementation details may continue to evolve while the core graph remains relatively stable.

#### Discussion

##### Drawbacks
Graph stability is a retrospective indicator — it can only be measured after multiple modeling sessions, which means it cannot guide early modeling decisions. A team in its first modeling session has no prior graph to compare against, making this indicator useless at the stage where guidance is most needed. Additionally, apparent stability may reflect insufficient challenge rather than genuine convergence — a model that has not been tested against new requirements or critical review may appear stable simply because it has not been stressed.

##### Rationale and alternatives
- **Artifact-count metrics (rejected)**: measuring maturity by the number of capsules, services, or tests produced is tempting because it is easy to automate. However, these metrics conflate modeling quality with implementation effort. A system can have hundreds of well-tested services built on a poorly structured model.
- **External review as the primary maturity signal (considered, not chosen)**: relying on peer review or expert assessment to determine model maturity is valuable but subjective and difficult to scale. Graph stability provides an internal, reproducible signal that complements external review.

##### Unresolved questions
1. Is there a minimum number of modeling sessions required before graph stability becomes a meaningful indicator? Three? Five?
2. How should "fundamental restructuring" be distinguished from "expected refinement" when evaluating whether new requirements force boundary changes?

### Modeling Before Implementation
Modeling should reach a sufficient level of maturity before implementation begins. Once a concept enters implementation, every subsequent change becomes progressively more expensive due to dependencies in storage, APIs, user interfaces, tests, deployment pipelines, and operational procedures. For this reason, Memar encourages extensive exploration at the modeling stage before committing to implementation decisions.

A proposed model should be continuously challenged:
* Does an equivalent concept already exist?
* Is this truly a new concern or merely a specialized use of an existing one?
* Does the proposed model introduce a new responsibility, or only a new presentation?
* Are we creating a new concept, or simply giving a new name to an existing one?

For example, a team may initially introduce a `Comment` model. Before implementation begins, the model should be examined against existing concepts such as `Content`. The goal is not to maximize reuse, but to determine whether a genuinely new responsibility exists or whether the proposed model is simply a contextual specialization of an already existing concept.

The cost of redesign is lowest during modeling. Therefore, the majority of conceptual consolidation should happen before implementation rather than after it.

#### Discussion

##### Drawbacks
The "model before implement" discipline can conflict with lean and experimental product-development approaches that emphasize validated learning through working software. If the team discovers, after implementing a prototype, that their model assumptions were wrong, the modeling effort invested before the prototype may have been partially wasted. The principle also does not account for domains that are poorly understood at the outset and can only be clarified through iterative implementation — in such cases, insisting on modeling maturity before any implementation may delay the very learning that would improve the model.

##### Rationale and alternatives
- **Spike-driven modeling (considered, not chosen)**: building a thin vertical slice through the system to validate model assumptions, then discarding the spike and modeling properly before real implementation. This preserves the learning benefit of early implementation without committing to the model that the spike reveals to be wrong. The risk is that teams rarely discard spikes — they tend to evolve into production code, carrying their modeling assumptions with them.
- **Time-boxed modeling (considered, not chosen)**: setting a fixed duration for modeling (e.g., one sprint) and beginning implementation regardless of maturity. This is pragmatic but explicitly accepts the cost of model changes during implementation.

##### Unresolved questions
1. Should Memar prescribe a specific modeling methodology (event storming, domain storytelling, etc.), or remain methodology-agnostic?
2. How should the cost of late model changes be estimated to help teams decide whether additional modeling investment is justified?

### Concept Existence vs. Model Existence
A recurring source of confusion in modeling discussions is the assumption that every identifiable concept must become an independent model element.

Memar does not make this claim.

The existence of a concept and the existence of a dedicated model are separate questions.

A concept deserves an independent capsule only when it represents an autonomous concern with its own rules, behavior, lifecycle, validation requirements, or architectural responsibilities. The mere ability to assign a name to something does not automatically justify introducing a separate capsule.

For example, a system may contain concepts such as `Price`, `DiscountedPrice`, `TaxIncludedPrice`, and `FinalPrice`. The existence of these terms does not imply that all of them should become independent capsules. In many cases, only `Price` represents a fundamental concern, while the others are derived representations, calculated views, or contextual interpretations of the same underlying concept.

The modeling challenge is therefore not to maximize the number of capsules, but to correctly distinguish between:

* Fundamental Concepts
* Derived Concepts
* Data Representations
* Contextual Views
* Infrastructure Structures

Failure to make these distinctions often produces two opposite architectural failures:

1. Under-modeling, where multiple independent concerns are collapsed into a single structure and their boundaries become unclear.
2. Artificial decomposition, where multiple names for the same concern are incorrectly promoted into independent architectural elements.

The primary objective of modeling is not decomposition itself. The objective is discovering and preserving the natural boundaries that already exist within the domain.

A future RFC should provide formal criteria for determining when a concept becomes an independent capsule and when it should remain a derived or contextual representation of another concept.

#### Discussion

##### Drawbacks
The distinction between "fundamental" and "derived" concepts is itself subjective and context-dependent. A `DiscountedPrice` that in one context is merely a calculated view of `Price` may, in another context, carry its own business rules — minimum discount thresholds, regulatory restrictions, temporal validity windows — that justify an independent capsule. The risk of misclassification increases with domain complexity, and an incorrect classification in either direction (promoting a derived concept to a capsule, or collapsing a fundamental concern into a derived view) produces real architectural damage.

##### Rationale and alternatives
- **Name-driven decomposition (rejected)**: every named concept gets its own capsule. This maximizes modularity but produces artificial fragmentation — the "artificial decomposition" failure described above.
- **Data-driven decomposition (rejected)**: every distinct data structure gets its own capsule. This inherits the assumptions of database normalization and conflates storage concerns with domain boundaries.
- **Responsibility-driven decomposition (chosen)**: only concepts that carry an independent responsibility, behavioral boundary, or lifecycle receive their own capsule. This requires more judgment but produces boundaries that reflect the domain's actual architecture.

##### Prior art
The distinction between fundamental and derived concepts parallels the "value object" vs. "entity" distinction in DDD, but Memar extends it beyond data identity to encompass responsibility and lifecycle. The "contextual view" category is informed by CQRS (Command Query Responsibility Segregation), where the same underlying data may be projected into multiple read-model shapes without each projection becoming an independent architectural element.

##### Unresolved questions
1. What are the formal criteria — beyond "independent responsibility and lifecycle" — for capsule justification? Can these criteria be made measurable?
2. How should the system handle a concept that starts as derived but later evolves to carry independent responsibilities? Is this a model evolution or a new capsule introduction?

##### Future possibilities
A future RFC should define a capsule-justification checklist — a set of questions that, when answered for a given concept, produce a clear recommendation on whether it deserves an independent capsule. This would reduce the subjectivity inherent in the current "responsibility-driven" judgment.

### Concept Discovery Must Not Be Driven by Presentation
Memar treats presentation structures as unreliable sources for discovering domain concepts.

User interfaces are designed around user experience, workflows, screen layouts, and interaction patterns. These concerns frequently change between products, platforms, and contexts, even when the underlying domain remains unchanged.

As a result, modeling should not begin by examining pages, forms, screens, widgets, or API endpoints and converting each visible element into a corresponding model.

For example, systems may expose concepts such as comments, social-media posts, news articles, blog articles, forum topics, or messages through completely different user experiences. However, a modeling effort may reveal that many of these are merely different presentations, aggregations, or contextual interpretations of a more fundamental concept such as `Content`.

The purpose of modeling is to discover stable domain boundaries, not to mirror presentation structures.

Presentation concerns may eventually require specialized widgets, pages, APIs, or aggregators, but these should emerge from the model rather than define it.

#### Discussion

##### Drawbacks
In practice, many projects begin with a user interface design or a set of API specifications, and the team has no alternative starting point for modeling. Dismissing the UI as an unreliable source is theoretically sound but practically frustrating when the UI is the most concrete artifact the team possesses. Additionally, in some domains — particularly consumer-facing products — the user experience is the domain, and the distinction between "presentation structure" and "domain concept" becomes difficult to maintain.

##### Rationale and alternatives
- **UI-driven modeling (rejected)**: deriving the model from pages, screens, and API endpoints is the de facto industry practice, driven by the prevalence of UI-first design tools and API-first development workflows. It produces models that are tightly coupled to a specific product's user experience and resistant to changes in that experience.
- **Event-driven modeling (considered, not chosen)**: starting from domain events (e.g., "OrderPlaced", "PaymentReceived") rather than UI structures. This is a stronger starting point for domain discovery but requires familiarity with event-storming techniques and does not naturally capture state-based concepts.
- **Language-driven modeling (considered, not chosen)**: analyzing the domain's ubiquitous language — the terms, phrases, and patterns that domain experts use — to identify concepts. This is aligned with DDD's strategic design phase but requires sustained access to domain experts, which is not always available.

##### Prior art
The critique of UI-driven modeling is shared by Eric Evans, who warns against "CRUD-driven" design where every screen becomes an entity. The specific argument that multiple presentation forms (comments, posts, articles, messages) may share a fundamental concept (`Content`) resonates with the "shared kernel" pattern in DDD, where multiple bounded contexts agree on a common model subset.

### Domain Decomposition over Aggregate-Root Modeling
Memar rejects the conventional DDD pattern where a domain "owner" entity (e.g. `User`) directly contains and owns sub-concerns like `username`, `email`, or `password` as its own fields/methods. Instead, each such concern is modeled as its own independent capsule, and any "User"-like concept is just one possible *aggregator* among several — aggregators are not fixed, singular, or domain-owned; they commonly form at the composition layer (GUI widgets/pages), though they are not limited to that layer.

The traditional aggregate-root pattern assumes a single, stable owning entity for a cluster of related data, but real systems frequently need different aggregations of the same underlying concerns depending on context. A canonical example: identity resolved via a local registration form needs a different aggregation shape than identity resolved via a third-party OAuth provider (e.g. Google login) — a single fixed `User` aggregator forces both flows into one shape that fits neither well, and tempts the owning entity to absorb logic (like credential validation) that does not actually belong to it.

`username`, `email`, and similar concerns are modeled as independent, self-contained capsules with their own validation and behavior. A composition-layer construct (typically a GUI widget or page, though this is the common case, not the only one) assembles whichever subset of these independent capsules a specific use case actually needs, and is responsible only for that assembly — not for absorbing the internal logic of the concerns it aggregates. Per [Composition Depth as a Decomposition Signal (No Expression Chaining)](./khayyam-composition_depth_as_decomposition_signal)'s decomposition-signal principle, if an aggregator's body starts doing more than its one named responsibility (e.g. a `RegisterComment` widget that also resolves "who is the current user"), that is the signal to split out a separate, dedicated widget (e.g. one that returns only an `ActiveUserID`), pushing that sub-concern's own validation and error-handling down into that separate widget rather than leaving it in the original caller.

A common misunderstanding is to interpret decomposition as merely extracting fields from a larger structure. For example, an `ActiveUserID` returned by a dedicated widget is not itself the concern being modeled. The actual concern is active-user resolution and selection: maintaining the currently active identity, enforcing any rules that govern identity switching, validating permissions, and exposing the selected identity to other parts of the system. The returned identifier is only an output of that concern, not the concern itself. This distinction is important because Memar decomposes systems around responsibilities and behavioral boundaries, not around individual pieces of data. A data value may appear in many places, but the responsibility that governs its creation, validation, and lifecycle should exist in exactly one place.

There is no language-level "aggregate root" or "entity" construct distinct from an ordinary capsule. Any capsule that happens to compose several other capsules is, structurally, just another capsule — its role as an "aggregator" is a naming/architectural convention applied by the developer, not a special grammar feature.

A capsule is not justified by the existence of data. A capsule is justified by the existence of an independent responsibility, behavioral boundary, or lifecycle. Data decomposition is a consequence of responsibility decomposition, not the objective of modeling.

#### Discussion

##### Naming Conventions
An aggregator capsule should be named after the use case it serves (e.g. `RegisterComment`, `LocalLoginForm`, `OAuthCallbackHandler`), not after the domain concept it assembles (e.g. `User`). This convention reinforces that the aggregator is a composition-layer construct with a single named responsibility, not a domain-owned entity.

##### Drawbacks
Without a single canonical owning entity, code that needs "the whole picture" of a concept like a user must always go through some composition-layer construct rather than a direct, centrally-defined object — this can mean more indirection to assemble a complete view, and requires discipline to avoid quietly re-inventing a de facto aggregate root inside a frequently reused widget. The approach also increases the number of capsules in a system, which can make the overall architecture harder to navigate for newcomers who expect to find a `User` object that contains all user-related data and behavior.

##### Rationale and alternatives
- **Classical DDD aggregate-root pattern (rejected)**: a single, owning entity directly containing related sub-concerns. In practice, it tends to pull unrelated validation and identity logic into one type, and breaks down whenever a concept (like "the current user") genuinely has more than one valid shape depending on context (local form vs. OAuth-resolved identity).
- **Trait/mixin-based decomposition (considered, not chosen)**: defining concerns as mixins that are composed into a single entity at compile time. This addresses the code-organization concern but does not solve the architectural problem: the composed entity still has a single identity and lifecycle, which forces all contexts to share one shape.
- **Composition-root pattern from functional programming (considered, not chosen)**: assembling dependencies at a single composition root, as in pure dependency injection. Memar's approach is similar but applies at the concept level (capsules) rather than the service level, and allows multiple composition roots for different contexts rather than a single application-wide root.

##### Prior art
This is closely related to, but distinct from, established critiques of Anemic/God-object Aggregate Roots within the DDD community itself; it also resonates with component-composition patterns common in modern frontend frameworks, where a "page" or "widget" composes several independent, narrowly-scoped pieces of state rather than a single monolithic model object. The principle that aggregation should happen at the composition layer rather than within the domain model also has parallels in the ports-and-adapters (hexagonal) architecture, where the domain core defines capabilities and the application layer assembles them into use cases.

##### Unresolved questions
1. What happens when two composition-layer widgets need the same aggregation but with slightly different validation rules? Is this handled by the capsules themselves (context-aware validation) or by the aggregators (decorating the capsules)?
2. Should there be a convention or lint rule that prevents a capsule from directly accessing another capsule's internal state, even when both are assembled by the same aggregator?

##### Future possibilities
A future RFC could define a formal "aggregation contract" — a lightweight protocol that specifies what an aggregator may and may not do with the capsules it assembles, including constraints on accessing internal state, propagating errors, and managing lifecycle.

## Discussion

### Naming Conventions
This RFC does not introduce new naming conventions for implementation artifacts. The conceptual terms used here (capsule, aggregator, composition layer, graph) are established elsewhere in the Memar specification and are not redefined here.

### Drawbacks
The modeling approach described in this RFC demands significant upfront investment before any implementation progress is visible. For small or well-understood domains, the full graph-discovery process may be disproportionate to the complexity being managed. The approach also assumes that a team has access to domain expertise — if the domain experts are unavailable or the domain is poorly understood, graph exploration may produce a model that reflects the team's assumptions rather than the domain's actual structure.

### Rationale and alternatives
- **Ad-hoc modeling without a defined process (rejected)**: this is the default in most organizations. It produces inconsistent models whose quality depends entirely on the individual architect's skill and experience, without any mechanism for systematic improvement.
- **Heavyweight formal modeling (rejected)**: approaches like full UPDM or SysML modeling provide rigor but introduce tooling and expertise barriers that make them impractical for most software teams. Memar seeks a middle ground: systematic enough to be teachable and repeatable, lightweight enough to be applied without specialized tools.

### Prior art
The overall approach draws from multiple traditions: DDD (Eric Evans) for the emphasis on domain language and bounded contexts, Event Storming (Alberto Brandolini) for the practice of discovering domain structure through collaborative exploration, and graph theory for the analytical framework used to evaluate model structure. Memar's distinctive contribution is the integration of these traditions into a single, coherent modeling discipline that is tightly coupled with the capsule and protocol abstractions defined in other RFCs.

### Unresolved questions
1. Should Memar prescribe specific modeling workshops or exercises (e.g., event storming, domain storytelling) as part of the standard modeling process, or should the modeling technique remain entirely up to the team?
2. How should modeling be integrated into CI/CD pipelines? Can model quality be automatically checked (e.g., detecting cycles in the dependency graph, flagging capsules without clear responsibilities)?
3. What is the recommended approach when a team inherits a legacy system with no existing model? Should they model from scratch and migrate, or incrementally extract the model from the existing codebase?

### Future possibilities
- A future RFC could define a model-quality linter — an automated tool that checks a graph for common modeling anti-patterns such as circular dependencies, overly broad capsules, or concepts without clear responsibility boundaries.
- A future RFC could address the transition path from legacy systems to Memar-structured models, including strategies for incremental model extraction and migration.

## Change Rationale
- **Initial revision.** First structured revision of this RFC. Added `RFC Number` (495216, derived from the original Start Date). Migrated `Contributor(s)` from the deprecated `contribution`/`task` format to the `Tasks`-based format per the RFC Template Specification. Fixed `Related RFCs` `Reason` value for Terminology from the non-standard `"Foundation Alignment"` to `"Depends_on"`. Wrote the previously empty `Summary` and `Guide-level explanation` sections. Added `#### Discussion` bundles (with Drawbacks, Rationale and alternatives, Prior art, and where appropriate Unresolved questions and Future possibilities) to every Reference-level topic. Added the missing `## Discussion` and `## Change Rationale` sections. Converted plain-text internal references to hyperlinks. Added additional examples (e-commerce Order/Payment relationship) and expanded existing discussion points with deeper analysis and more alternatives.