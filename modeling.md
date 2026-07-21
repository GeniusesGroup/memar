---
Title: "Modeling"
Status: Proposed
Start Date: 2026-06-30
RFC Number: 495216
Applied to: []
Related RFCs:
    - Title: "Terminology"
      URI: "./terminology.md"
      Reason: "Depends_on"
      Explanation: "Terminology governs how concepts are understood across all modeling discussions."
    - Title: "Protocol"
      URI: "./protocol.md"
      Reason: "Depends_on"
      Explanation: "Defines Protocol as a pure declarative specification; modeling produces the domain structures that protocols then constrain."
    - Title: "System"
      URI: "./system.md"
      Reason: "Depends_on"
      Explanation: "Defines Model and Abstraction at the conceptual level. This RFC builds on those definitions to specify how Memar performs modeling as an architectural activity."
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Titles: ["Core principles", "Domain decomposition", "Abstraction justification"]
        URI: ""
        Explanation: "Defined the core modeling philosophy; directed the rejection of aggregate-root ownership and the abstraction-responsibility principle."
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
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "Claude Sonnet 5"
    Effort: "medium - thinking"
    Tasks:
      - Titles: ["Critical review", "Attribute-or-edge test", "Acquired vs. discovered data", "Event-aware state modeling", "Initial discovery checklist"]
        URI: ""
        Explanation: "Critiqued the aggregate-root rejection example, the behavior-before-structure sequencing claim, and the undefined operational criterion for independent responsibility; replaced the Order/Payment example with Invoice/Financial Transaction and added the naming-precision note; added the Attribute-or-Edge Test and its Reuse-Across-Contexts corroborating signal; added Acquired Data vs. Discovered Data and the discovered-should-not-automatically-be-stored principle; added Modeling State Change as Events, Not Destructive Updates, led by the reality-before-projections framing; added the Initial Discovery Questions checklist; incorporated further review from ChatGPT (GPT-5.5) on this same revision pass."
---

# Modeling

## Summary
This RFC defines how Memar approaches domain modeling: treating the model as the primary architectural artifact, discovering it through graph-based exploration before any implementation commitment, and decomposing the domain around independent responsibilities rather than data ownership or presentation structures. It establishes that an abstraction is justified by an autonomous responsibility and lifecycle, not by the existence of data; that adaptability emerges from model quality, not from technology choices; and that behavioral complexity is a modeling smell rather than a requirement. The aggregate-root pattern of conventional DDD is rejected in favor of composing independent concerns at the composition layer, with no single fixed owning entity. Crucially, the output of the modeling phase is a set of abstractions, concerns, relationships, and supporting documents — not capsules. Capsules are implementation-level realizations that belong to later architectural and implementation phases.

## Motivation
The framework should prevent incorrect models before implementation and reduce the cost of correction when mistakes inevitably occur. In practice, most architectural rigidity does not originate from poor technology choices — it originates from models that conflate unrelated concerns, mirror presentation structures, or bind responsibilities to fixed owning entities. Once a flawed model propagates into databases, APIs, user interfaces, and deployment pipelines, every subsequent correction carries compounding cost. Memar therefore needs an explicit, opinionated modeling discipline that maximizes the quality of the model before implementation begins and preserves the ability to evolve it afterward.

## Guide-level explanation
Modeling begins when a new requirement enters the system. The objective is not to immediately design APIs, databases, screens, or implementation structures. The objective is to understand the domain well enough that architectural boundaries emerge naturally.

A modeling session typically follows this workflow:
1. Extract concepts, responsibilities, constraints, and relationships from the requirement.
2. Treat every discovered concept as provisional rather than accepted.
3. Challenge each concept:
  - Does an equivalent concept already exist?
  - Is it introducing a new responsibility or only a new name?
  - Is it a fundamental concern or a contextual view?
4. Build a graph of concepts and relationships.
5. Examine the graph for responsibility boundaries.
6. Identify concerns that appear to have independent responsibilities or lifecycles.
7. Delay implementation decisions until the graph stabilizes and major assumptions have been challenged.

During modeling, assumptions are targets for investigation rather than facts to be recorded. The purpose of discussion is not to collect concepts but to eliminate incorrect ones. A modeling session is successful when it improves understanding of the domain. New questions, rejected assumptions, clarified terminology, and refined boundaries are all valid outcomes. Producing implementation artifacts is not required. Modeling should continue until the team can explain the domain using stable concepts, stable relationships, and clear responsibility boundaries. Only then should implementation-oriented activities begin.

Modeling inherently requires systemic thinking — examining how concerns interact, how behaviors propagate across boundaries, and how decisions in one part of the system affect behavior in another. A modeling effort that examines concepts in isolation, or that partitions the domain along organizational or team boundaries (e.g., frontend vs. backend) rather than along natural concern boundaries, will produce a model that reflects organizational structure rather than system behavior. Many architectural failures — a retry mechanism that degrades user experience, an error message that exposes internal failures, a validation step placed at the wrong point in a workflow — originate not from poor modeling of individual components but from a failure to model the system as a whole.

## Reference-level explanation

### What a Model Is
A **model** is a simplified representation of a system or aspect of reality, constructed to facilitate understanding, analysis, prediction, communication, or transformation.

Models are composed of abstractions and relationships. They preserve information that is relevant to a specific purpose and discard information that is not. No model captures its target in full; the act of modeling is inherently selective, and the quality of a model is judged not by how much it includes but by how well it serves its stated purpose.

A model may be formal or informal, mathematical or visual, textual or computational. An equation that describes orbital mechanics is a model. A diagram that describes a software system's component structure is a model. A natural-language description of a business process is a model. The medium of the model is less important than the rigor and purpose with which it is constructed.

This definition is grounded in the [System RFC](./system.md), where Model is defined as a concept in the Scientific terminology layer: its meaning is rooted in the philosophy of science and systems theory, defined with explicit boundaries, and intended to be open to criticism and revision.

#### Models Are Not Reality
A model is not the thing it models. This distinction — between the map and the territory, the representation and the represented — is one of the oldest and most frequently violated principles in intellectual history. Confusing a model with reality leads to several well-documented failures:

- Treating an economic model as if it fully describes economic behavior, leading to policy decisions that fail when real behavior deviates from model assumptions.
- Treating a software architecture diagram as if it fully describes the running system, leading to maintenance decisions that fail when the actual runtime behavior differs from the diagrammed structure.
- Treating a data model as if it fully describes the domain it represents, leading to application behavior that fails when real-world entities exhibit properties the model did not anticipate.

Within Memar, every model should be treated as a tool with known limitations, not as a complete description of its target. Memar's modeling process should include explicit mechanisms for identifying and documenting what each model deliberately omits.

#### Discussion

##### Drawbacks
Emphasizing the gap between models and reality can lead to a form of epistemic paralysis: if no model is complete, how can any model be trusted? The answer is that models do not need to be complete to be useful; they need to be honest about what they include and what they exclude, and the consequences of each omission should be understood and documented. A model that is explicitly incomplete but whose incompleteness is well-characterized is more useful than a model that claims completeness but silently omits important aspects of its target.

##### Rationale and alternatives
- **Treat models as approximations of reality (considered, not chosen as primary definition).** While true, this framing can imply that models should be judged by their fidelity to reality, which is only one dimension of model quality. A model may serve its purpose well even if it departs significantly from reality in aspects that are irrelevant to that purpose.

##### Prior art
The distinction between models and reality is discussed extensively in philosophy of science, most accessibly in Box and Draper ("Empirical Model-Building and Response Surfaces," 1987) and in the broader systems modeling literature.

##### Unresolved questions
1. Should Memar prescribe specific modeling formalisms, or remain formalism-agnostic?
2. How should models be versioned and evolved alongside the systems they describe?

### Initial Discovery Questions
Understanding what a model is (see above) does not by itself tell a modeler where to begin when facing an unstructured requirement — a lengthy specification document, a stakeholder interview, or an existing but undocumented system. Before any node is proposed, the following questions give a concrete entry point:

- What information must the system know to fulfill this requirement?
- For each piece of information: is it [acquired or discovered](#acquired-data-vs-discovered-data)?
- What responsibilities are implied by this requirement — what rules, validations, or lifecycle transitions does it require?
- Which of those responsibilities could plausibly evolve independently of the others?
- Does a similar responsibility already exist elsewhere in the graph, under a different name?
- Which of the concepts under discussion are [derived or contextual views](#concept-existence-vs-model-existence) of another concept, rather than fundamental concerns in their own right?
- What relationships connect these concepts, and what do those relationships encode — ownership, reference, composition, or something else?

These questions do not replace the fuller discovery process described in this RFC — they exist to give a modeler a starting point rather than a blank page. Answering them produces the first provisional candidates that the rest of the modeling process (see [Challenging Proposed Concepts](#challenging-proposed-concepts)) then interrogates, tests, and refines.

#### Discussion

##### Drawbacks
A checklist risks being treated as a mechanical procedure whose completion signals that modeling is "done," which contradicts the iterative, non-linear nature of the rest of this RFC. It is intended only as an entry point for the first pass over a new requirement, not as a gate or a substitute for the deeper discovery process.

##### Rationale and alternatives
- **No initial checklist (rejected)**: leaving modelers to begin entirely from first principles each time is consistent with treating modeling as pure judgment, but in practice produces inconsistent starting points across sessions and modelers, and gives no guidance for the common case of an unstructured, lengthy requirement.

##### Future possibilities
A future RFC could expand this into a fuller intake template for requirement documents, connecting each answer directly to the graph-construction workflow.

### The Model as the Primary Artifact
Modeling in Memar means discovering the natural structure of a domain before writing any implementation code. The output of modeling is not a database schema, not an API definition, and not a class hierarchy — it is a graph of concerns, responsibilities, and relationships that reveals where the real architectural boundaries lie.

Memar treats the domain model as the primary architectural artifact of a system. The purpose of implementation is not to define the model. The purpose of implementation is to realize a model that has already been discovered and validated. A successful implementation does not prove that a model is correct. It only proves that the model can be implemented. This distinction is important because implementation introduces irreversible costs. Once a model is reflected in databases, APIs, user interfaces, deployment pipelines, integrations, and operational procedures, changing the model becomes increasingly expensive.

For this reason, Memar encourages extensive model exploration before implementation and seeks to minimize the coupling between implementation details and domain concepts. The closer a system keeps its implementation aligned with the model, the easier it becomes to evolve the architecture when new understanding emerges. The model should remain the source of truth. Implementations are merely projections of that truth into specific technological contexts.

#### Discussion

##### Drawbacks
Treating the model as primary requires upfront investment in modeling before any visible implementation progress can be demonstrated. In environments where stakeholders measure velocity by shipping features, this approach can create political friction. Additionally, the claim that "a model can be validated without implementation" is itself limited — some categories of correctness (performance characteristics, storage feasibility, integration compatibility) can only be fully evaluated once an implementation exists.

##### Rationale and alternatives
- **Implementation-driven modeling (rejected)**: starting from code and extracting the model afterward is common in agile practices, but consistently produces models that reflect incidental implementation decisions rather than domain structure. The cost of correcting such models grows with every additional feature built on top of them.
- **Parallel modeling and implementation (considered, not chosen)**: developing the model and implementation concurrently reduces time-to-first-prototype but makes it harder to distinguish model concepts from implementation artifacts during review. Memar permits rapid prototyping for learning purposes but does not treat prototypes as committed implementation.

##### Prior art
The idea that the model precedes and constrains the implementation is central to model-driven architecture (MDA) as defined by the OMG, and to Eric Evans' Domain-Driven Design, which argues that the domain model should be the heart of the software. Memar's contribution is not the principle itself but the specific mechanisms (graph-based discovery, conceptual boundaries, protocol separation) that make the principle practically enforceable.

##### Unresolved questions
1. How much modeling maturity is "sufficient" before implementation begins? Is there a measurable threshold, or does this remain a judgment call?
2. Can a lightweight checklist be derived from the graph-stability indicators to make "sufficient maturity" more objectively evaluable?

### Modeling Produces Abstractions, Not Capsules
The output of modeling is not a set of capsules. Modeling operates entirely at the conceptual level. The primary outputs of modeling are:

* Abstractions
* Concerns
* Responsibilities
* Relationships
* Constraints
* Conceptual Boundaries
* Supporting Documents

These artifacts describe the domain independently of any implementation strategy. A capsule is an implementation-level realization of one or more abstractions and therefore belongs to later architectural and implementation phases. For this reason, modeling discussions should avoid prematurely introducing capsules, services, classes, databases, APIs, or other implementation-oriented structures. The objective of modeling is to discover the abstractions that exist within the domain, not to decide how those abstractions will eventually be implemented.

### Modeling, Protocol, and Architecture
Modeling, Protocol, and Architecture are not sequential phases in a linear pipeline. In Memar, architecture encompasses the entire process of designing and building a system — from initial domain discovery through implementation. Modeling and Protocol are complementary aspects of this overarching architectural process.

Modeling discovers the abstractions, concerns, responsibilities, relationships, and behavioral expectations that exist within a domain. Protocol captures and constrains those discoveries as stable knowledge contracts. A protocol is not merely an interface definition or a communication contract — it is the structured knowledge that governs how a concern is understood, constrained, and interacted with, encompassing concepts, abstractions, constraints, relationships, behaviors, rules, and eventually their realizations. The model produced by modeling is not separate from the protocol; it becomes part of the protocol's knowledge base. As modeling deepens understanding of a domain, that understanding is absorbed into the protocol. As implementation progresses, the protocol ensures that the relationship between understanding and realization remains transparent and enforceable.

This means the boundary between modeling and protocol is not a hard phase transition — it is a gradual shift in emphasis from discovery to formalization. Early in a project, modeling dominates and the protocol is thin. As understanding matures, the protocol grows richer and begins to constrain implementation decisions. Both activities remain architectural in nature: they are decisions about the system's structure and behavior, made before and during implementation.

For a detailed discussion of Protocol, see the [Protocol RFC](./protocol.md). For terminology definitions, see the [Terminology RFC](./terminology.md).

### Models Must Survive Implementation Changes
A model should not become difficult to change merely because an implementation already exists. One of the primary responsibilities of architecture is to preserve the ability to evolve domain understanding over time. As knowledge grows, previously accepted models may be refined, decomposed, consolidated, or replaced. Such changes should be treated as normal architectural evolution rather than exceptional events.

Memar therefore places significant emphasis on protocols as stable boundaries between models and their implementations. A protocol defines the observable contract of a concern without exposing the implementation decisions behind it. By preserving this separation, implementations can evolve, migrate, or even be completely replaced while minimizing the impact on the surrounding architecture.

For a detailed discussion, see the [Protocol RFC](./protocol.md).

#### Discussion

##### Drawbacks
Protocol boundaries introduce indirection. Every interaction with an abstraction's implementation must pass through its protocol rather than accessing implementation details directly, which can increase the cognitive overhead of understanding the system, particularly for developers accustomed to directly accessing object internals. There is also a risk of over-abstracting early, creating protocol boundaries around concerns that turn out to be simple enough that the indirection is not justified by any real need for implementation independence.

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
This principle can be misinterpreted as license to defer all technology decisions indefinitely. In practice, some technology constraints (regulatory requirements, existing infrastructure, team expertise) may legitimately constrain the model or at least the shape of its realizations. A team that exclusively models without considering technological feasibility risks producing a model that cannot be practically implemented in its target environment.

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

For example, consider `Invoice` and `Financial Transaction`. These are related via a reference edge — an `Invoice` references the `Financial Transaction`s recorded against it — but the invariant governing when an `Invoice` may transition to a `Paid` status is not owned by a third, aggregating entity. It is owned by `Invoice` itself, as part of its own state-transition responsibility: the method that attempts the transition to `Paid` traverses its reference edges to the related `Financial Transaction` nodes, sums their amounts, and only permits the transition if that sum meets or exceeds the invoice total. `Financial Transaction`, in turn, owns its own validation and lifecycle independently of any `Invoice` — it does not need to know about invoices to be valid.

This illustrates that a cross-concern invariant does not require a shared owning entity or a composition-layer aggregator to be enforced correctly. It requires only that the concern whose lifecycle the invariant actually gates — here, `Invoice`'s transition to `Paid` — reads what it needs from its own edges to already-independent nodes. The invariant is not split, duplicated, or homeless; it belongs entirely to the one concern whose state it governs, without that concern absorbing the internal validation logic of the nodes it references. Examining `Invoice` and `Financial Transaction` in isolation would miss all of this.

Word choice in this kind of example is not cosmetic. `Order` and `Payment` were initially considered and rejected: an order is a command that may never be fulfilled (e.g. an order to buy 1,000 shares of a stock, or 50 beams of steel, that never executes), so it has no inherent connection to financial settlement; and a `Payment` is typically itself a composition-layer construct (a checkout widget or page) rather than a base concern. `Invoice` and `Financial Transaction` were chosen instead because they name the actual base concerns without smuggling in assumptions about workflow outcome or implementation layer. This level of care in naming is not optional polish — an imprecise name at the modeling stage silently encodes an incorrect assumption into the abstraction's identity, and that assumption then propagates into every place the abstraction is used.

`Invoice`/`Financial Transaction` illustrates where a cross-concern behavioral invariant lives once aggregate-root ownership is rejected. For the complementary, more structural question of when a concept deserves its own node at all, see the recurring `Product`/`Title`/`Text` example in [The Attribute-or-Edge Test](#the-attribute-or-edge-test).

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
* Potential architectural abstractions

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

Furthermore, graphs serve as a discovery environment where concepts, relationships, questions, assumptions, discussions, and modeling decisions can evolve together. The value of graph-based modeling is therefore not limited to representing structure — it also supports the exploration and refinement of the model itself. Questions posed about a node, challenges raised against an edge, and assumptions recorded during discussion all become part of the modeling context that the graph carries. In table-driven or schema-driven modeling approaches, these observations often go unrecorded entirely.

The practical consequence is that a graph is expected to change frequently during modeling. It is a working tool, not a polished deliverable. A graph that has not been revised multiple times during the modeling process is likely a graph that has not been used seriously as a discovery mechanism.

#### Discussion

##### Drawbacks
Treating graphs as disposable working tools means there may be no durable record of the modeling process once implementation begins. If a team revisits a modeling decision months later, the original graph — with all its intermediate states, abandoned alternatives, and rejected structures — may no longer exist. This loss of modeling history can make it difficult to understand why certain boundaries were chosen and others were not, especially when the original modelers are no longer available.

##### Rationale and alternatives
- **Graphs as living documentation (considered, not chosen)**: maintaining the graph as a continuously updated document alongside the codebase keeps the modeling history accessible but introduces an ongoing maintenance obligation. The graph must be updated every time the model evolves, or it becomes misleading. For teams that already struggle with documentation maintenance, this obligation may be unrealistic.
- **Versioned graph artifacts (considered, not chosen)**: committing graph snapshots to version control at each modeling milestone preserves history without requiring continuous maintenance. This approach is promising but has no established convention for graph file formats or commit granularity.

##### Prior art
The distinction between "design as discovery" and "design as documentation" parallels the distinction between exploratory data analysis and confirmatory data analysis in statistics. In both cases, the exploratory phase uses flexible, informal tools, while the confirmatory phase produces structured, auditable artifacts.

### Behavior and Structure Are Discovered Together
Structures are often the first thing stakeholders can articulate — entities, fields, and data relationships come easily to describe. Behaviors are usually harder to surface and often only emerge through careful, repeated questioning. This does not mean structure and behavior belong to separate phases of modeling, one strictly preceding the other; in practice, both surface together on the same whiteboard, in the same conversation, and in the same graph-editing session, and a modeler should not attempt to suppress structural thinking until some declared "behavior phase" is complete.

What the modeling process must guard against is treating a structure as settled before its behavioral implications have been questioned. A system's real complexity resides not only in what it stores but in what it does: how it responds to failure, how it handles concurrent operations, how it recovers from inconsistent states, how it communicates delays to users, and how it enforces rules across temporal boundaries. A node or edge proposed in the graph should be interrogated for its behavioral consequences as soon as it is proposed — not deferred to a later pass — precisely because behavior and structure inform each other continuously throughout modeling. A retry mechanism designed without considering user experience, an error message that exposes internal failures, or a validation step placed at the wrong point in a workflow — these are all behavioral failures that stem from structure that was allowed to calcify before its behavioral implications were questioned.

A model that captures both together tends to reveal appropriate structures naturally. A structurally elegant model produced without equal attention to behavioral expectations will inevitably require expensive corrections once implementation exposes the gaps.

#### Discussion

##### Drawbacks
Treating structure and behavior as inseparable can make modeling sessions feel unfocused, since a discussion of a node's fields can be repeatedly interrupted by behavioral questions and vice versa — stakeholders who expect a clean, sequential process (first the data model, then the behavior) may find this uncomfortable. In domains where behavior is poorly documented or where domain experts think primarily in terms of data structures (e.g., reporting systems, data-warehousing contexts), the constant behavioral interrogation may feel unfamiliar and require additional facilitation effort. There is also a risk of over-analyzing edge-case behavior before the core structural patterns have stabilized, consuming modeling time on concerns that may turn out to be rare or irrelevant.

##### Rationale and alternatives
- **Structure-first modeling (rejected)**: defining entities, their attributes, and their relationships before examining behavior is the dominant industry approach, driven by ORM tools, database-first design, and API-specification workflows. It produces models that accurately describe what the system contains but often fail to capture what the system does — leading to behavioral gaps that surface only during implementation or, worse, in production.
- **Strict behavior-before-structure sequencing (rejected)**: requiring behavior to be fully understood before any structural decision is made is appealing in principle but unworkable in practice — stakeholders cannot describe behavior in a vacuum, without reference to the concepts that behavior acts upon. It also implies a rigidity of phases that Memar's modeling process does not otherwise impose.
- **Unstructured parallel discovery (rejected)**: discovering behavior and structure simultaneously without discipline is appealing but in practice tends to produce models where structural assumptions unconsciously constrain behavioral exploration. For example, once an `Order` entity has been defined with a `status` field, the team may stop asking whether `status` is even the right behavioral model for order lifecycle. Memar's approach differs from unstructured parallelism by requiring that every proposed node or edge be immediately interrogated for its behavioral consequences, rather than accepted and revisited later.

##### Prior art
The principle that behavior deserves equal attention to structure is central to behavior-driven development (BDD) and to event-storming, where domain events — behavioral occurrences — are a primary discovery mechanism alongside structural ones. Memar's contribution is treating this as continuous, disciplined co-discovery within graph-based modeling, rather than either a separate development practice or a strictly sequential phase.

### Behavior Often Reveals the Quality of the Model
In Memar, behavior is not treated as an independent concern that is discovered only after structural modeling is complete. A well-formed graph frequently constrains and reveals the space of valid behaviors. As concepts, responsibilities, and relationships become clearer, many behavioral expectations emerge naturally from the model itself. For this reason, unusual behavioral complexity should often be treated as a signal rather than a requirement.

When a system requires an increasing number of special cases, exceptions, coordination rules, translation layers, synchronization mechanisms, or procedural workarounds, the underlying model should be re-examined before additional implementation complexity is introduced. In many cases, behavioral complexity is not evidence of a sophisticated domain. It is evidence that responsibilities, boundaries, or relationships have not yet been modeled correctly.

**A mature model tends to simplify behavior. An immature model often transfers its complexity into implementation.**

When behavioral complexity accumulates special cases, coordination rules, synchronization mechanisms, translation layers, or procedural workarounds the model should be re-examined before additional implementation complexity is introduced. A mature model tends to simplify behavior. An immature model tends to transfer its complexity into implementation.

#### Discussion

##### Drawbacks
The claim that behavioral complexity signals modeling immaturity can be overapplied. Some domains are genuinely complex — regulatory compliance, multi-currency financial settlement, real-time collaborative editing — and no amount of modeling will eliminate their inherent behavioral complexity. Applying this principle indiscriminately risks creating a culture where legitimate domain complexity is dismissed as a modeling failure, leading to oversimplified models that cannot handle real-world edge cases.

##### Rationale and alternatives
- **Behavior-driven modeling (rejected in its conventional form)**: starting from user stories or behavior specifications and deriving the model from them tends to produce models that reflect usage patterns rather than domain structure. The resulting model may be optimized for current workflows but resistant to unanticipated changes.
- **Separate behavioral and structural modeling (rejected)**: this is the dominant industry practice — model the structure first, then define behavior as methods, handlers, or services. Memar does not treat behavior as a separate phase because behavioral expectations are often the clearest indicator of whether structural boundaries have been drawn correctly.

##### Prior art
This principle resonates with Rich Hickey's "design is about pulling things apart" philosophy and with the notion of "essential complexity" from Fred Brooks' "No Silver Bullet." Memar's contribution is the specific heuristic: when behavioral complexity accumulates, re-examine the model before adding implementation complexity.

### Graph Stability as an Indicator of Model Maturity
Model maturity should not be measured by the number of concepts, concerns, or abstractions. Instead, maturity emerges when graph exploration repeatedly converges toward the same structural understanding of the domain.

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
- **Artifact-count metrics (rejected)**: measuring maturity by the number of concerns, services, or tests produced is tempting because it is easy to automate. However, these metrics conflate modeling quality with implementation effort. A system can have hundreds of well-tested services built on a poorly structured model.
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

### Challenging Proposed Concepts
Every newly proposed concept should be assumed to be provisional until it survives critical examination. The purpose of modeling is not to collect concepts. The purpose of modeling is to discover whether a proposed concept represents a genuinely independent responsibility.

For every proposed concept, the team should ask:
- Does an equivalent concept already exist?
- Is this concept merely a contextual view of another concept?
- Is it introducing a new responsibility or only a new name?
- Does it have an independent lifecycle?
- Does it enforce rules that no existing concern already owns?
- Would the system lose architectural clarity if this concept disappeared?

A concept that cannot justify its existence should not become an independent abstraction.

#### Discussion

##### Rationale and alternatives
- Without explicit challenge rules, teams tend to accept concepts too quickly and reproduce presentation structures inside the model.

### Assumptions Are Modeling Targets
During modeling, statements from stakeholders should be treated as hypotheses rather than facts.

- **The responsibility of the modeler is not to record assumptions.**
- **The responsibility of the modeler is to test them.**

For example `"We need a Comment model."` should immediately trigger questions such as:
- Why is Comment different from Content?
- Which responsibility exists in Comment that does not already exist elsewhere?
- Is this a domain concept or merely a presentation distinction?

Modeling progresses through validated assumptions, not collected assumptions.

### Questions Are Architectural Tools
Questions are not merely a communication mechanism. A good modeling question can eliminate entire branches of an incorrect model before implementation begins. Modeling sessions should prioritize discovering better questions rather than producing more diagrams. A team that rapidly creates concepts without questioning them is usually documenting assumptions rather than modeling the domain.

### Early Indicators of Modeling Progress
Before graph stability can be observed, teams may use the following indicators:
- Fewer newly introduced concepts per session.
- Increasing agreement on concept meanings.
- Reduction of duplicate terminology.
- Reduction of exceptional behaviors.
- Ability to explain the domain using fewer fundamental concepts.

These indicators do not prove model maturity, but they often signal convergence.

### Expected Output of a Modeling Session
A modeling session is successful if it produces:
- New questions.
- Clarified terminology.
- Rejected assumptions.
- Refined relationships.
- Improved responsibility boundaries.

A session does not need to produce implementation artifacts, database schemas, APIs, or finalized abstraction definitions.

### Concept Existence vs. Model Existence
A recurring source of confusion in modeling discussions is the assumption that every identifiable concept must become an independent model element. Memar does not make this claim. The existence of a concept and the existence of a dedicated model are separate questions.

An abstraction — the primary output of Memar's modeling phase — is not justified by the existence of data. An abstraction is justified by the existence of an independent responsibility, behavioral boundary, or lifecycle. Data structures are consequences of responsibility decomposition, not its drivers.

A concept may justify an independent abstraction only when it represents an autonomous concern with its own rules, behavior, lifecycle, validation requirements, or architectural responsibilities. The mere ability to assign a name to something does not automatically justify introducing a separate abstraction.

For example, a system may contain concepts such as `Price`, `DiscountedPrice`, `TaxIncludedPrice`, and `FinalPrice`. The existence of these terms does not imply that all of them should become independent abstractions. In many cases, only `Price` represents a fundamental concern, while the others are derived representations, calculated views, or contextual interpretations of the same underlying concept.

The modeling challenge is therefore not to maximize the number of abstractions, but to correctly distinguish between:

* Fundamental Concepts
* Derived Concepts
* Data Representations
* Contextual Views
* Infrastructure Structures

Failure to make these distinctions often produces two opposite architectural failures:

1. Under-modeling, where multiple independent concerns are collapsed into a single structure and their boundaries become unclear.
2. Artificial decomposition, where multiple names for the same concern are incorrectly promoted into independent architectural elements.

The primary objective of modeling is not decomposition itself. The objective is discovering and preserving the natural boundaries that already exist within the domain.

A future RFC should provide formal criteria for determining when a concept becomes an independent abstraction and when it should remain a derived or contextual representation of another concept.

#### The Attribute-or-Edge Test
A practical operationalization of the "independent responsibility" criterion is available directly from the graph itself: for any data point a node appears to need, ask whether that node actually owns the responsibility for that data, or whether the requirement is better expressed as an edge to an already-independent node.

For example, when modeling a `Product` node, the requirement "a product needs a name" does not automatically justify a `ProductName` field on `Product`. The question to ask is: does `Product` — or indeed any node that merely references text — carry the responsibility of storing, validating, versioning, internationalizing (i18n), and making searchable, the textual content itself? In most domains it does not — that responsibility already belongs to a general-purpose `Text` abstraction, used identically for comment bodies, article titles, or any other free-form content. The correct model is therefore not a `ProductName` attribute, but an edge — e.g. `Product --(Title)--> Text` — where `Title` names the relationship and the referenced `Text` node owns the concern of holding, validating, translating, and indexing textual content.

Concentrating text-handling responsibility into a single concern this way resolves two problems that otherwise recur across nearly every domain:

* **Internationalization.** When text is duplicated as ad-hoc string fields across many unrelated nodes (`ProductName`, `CategoryTitle`, `UserBio`, and so on), adding a new language requires touching every one of those nodes and every schema that stores them. When all free-form text is instead a reference to a single `Text` abstraction, multilingual support is a concern the `Text` abstraction alone owns and evolves — no other domain needs to change, even retroactively, for content that existed before internationalization was considered.
* **Search.** When the textual source of truth is scattered across every domain, a search capability has no choice but to reach into every one of those domains individually to answer even a simple text-based query. When text is centralized behind one abstraction, that abstraction becomes the natural place to build indexing and search capability once, rather than once per domain.

This test — "is this data owned here, or is it a named relationship to an already-independent concern?" — gives modelers a concrete, graph-native way to apply the single-responsibility principle without relying purely on intuitive judgment. It does not eliminate subjectivity in the harder cases (see Unresolved Questions below), but it converts many everyday attribute-vs-abstraction decisions into a mechanical check against the existing graph.

The `Product --(Title)--> Text` example is used as a recurring reference example throughout this RFC precisely because it exercises internationalization, search, versioning, reuse, and derived-structure concerns in a single, small graph — it is worth returning to whenever a new principle needs a concrete illustration.

#### Reuse Across Contexts as an Additional Signal
The Attribute-or-Edge Test answers a narrower question than the one it is sometimes mistaken for. It tells a modeler whether a piece of data belongs to the node that appears to need it, or to an edge pointing at an already-independent node. It does not by itself explain why a node such as `Text` is independent in the first place, as opposed to `Title` or `ProductName`, which are not.

Independent responsibility, behavioral boundary, or lifecycle (see above) remains the primary criterion for justifying an abstraction. Reuse across contexts is a strong, but not required, corroborating signal: when the same responsibility is needed by multiple otherwise-unrelated concerns — as `Text` is needed by `Product`, `Comment`, and `Article` alike — that recurrence is strong evidence the responsibility does not belong to any single one of them, which is exactly what "independent responsibility" means in practice. `Title` and `ProductName`, by contrast, are not independently reused anywhere — they are names for a relationship and an unnecessary duplication, respectively — which is why neither warrants its own node.

The absence of reuse does not disqualify a concept from independent-abstraction status. `Invoice` (see [Modeling Requires Explicit Relationship Analysis](#modeling-requires-explicit-relationship-analysis)) is used in only one context — financial/billing — yet still warrants its own abstraction, because its lifecycle and responsibility are independent regardless of how many other concerns reference it. Reuse strengthens the case for extraction; it is not the test itself, and a modeler should not withhold an abstraction from a concept with a clear independent lifecycle merely because that concept has not yet appeared in a second context.

#### Discussion

##### Drawbacks
The distinction between "fundamental" and "derived" concepts is itself subjective and context-dependent. A `DiscountedPrice` that in one context is merely a calculated view of `Price` may, in another context, carry its own business rules — minimum discount thresholds, regulatory restrictions, temporal validity windows — that justify an independent abstraction. The risk of misclassification increases with domain complexity, and an incorrect classification in either direction (promoting a derived concept to an abstraction, or collapsing a fundamental concern into a derived view) produces real architectural damage.

##### Rationale and alternatives
- **Name-driven decomposition (rejected)**: every named concept gets its own abstraction. This maximizes modularity but produces artificial fragmentation — the "artificial decomposition" failure described above.
- **Data-driven decomposition (rejected)**: every distinct data structure gets its own abstraction. This inherits the assumptions of database normalization and conflates storage concerns with domain boundaries.
- **Responsibility-driven decomposition (chosen)**: only concepts that carry an independent responsibility, behavioral boundary, or lifecycle receive their own abstraction. This requires more judgment but produces boundaries that reflect the domain's actual architecture.

##### Prior art
The distinction between fundamental and derived concepts parallels the "value object" vs. "entity" distinction in DDD, but Memar extends it beyond data identity to encompass responsibility and lifecycle. The "contextual view" category is informed by CQRS (Command Query Responsibility Segregation), where the same underlying data may be projected into multiple read-model shapes without each projection becoming an independent architectural element.

##### Unresolved questions
1. What are the formal criteria — beyond "independent responsibility and lifecycle" — for abstraction justification? Can these criteria be made measurable?
2. How should the system handle a concept that starts as derived but later evolves to carry independent responsibilities? Is this a model evolution or a new abstraction introduction?

##### Future possibilities
A future RFC should define a abstraction-justification checklist — a set of questions that, when answered for a given concept, produce a clear recommendation on whether it deserves an independent abstraction. This would reduce the subjectivity inherent in the current "responsibility-driven" judgment.

### Acquired Data vs. Discovered Data
A complementary lens for distinguishing fundamental concepts from derived ones (see [Concept Existence vs. Model Existence](#concept-existence-vs-model-existence)) is to ask, for any candidate data point, whether it is **acquired** or **discovered**:

* **Acquired data** is stated directly by an external source — typically a user, a sensor, or another system — and cannot be recomputed from anything else already in the model. It is a primary fact.
* **Discovered data** is derived from acquired data (or from other discovered data) through computation, aggregation, or inference. It is not a primary fact; it is a view.

This question exposes a common modeling mistake: storing a discovered value as though it were acquired, thereby losing the underlying acquired data it was computed from. For example, a system tracking a moving object should acquire and store the object's position and time of observation — these are the primary facts a sensor or user actually reports. Velocity and acceleration are discovered: they are computable from a sequence of position/time observations. Modeling `Speed` as if it were itself an acquired, independently stored value discards the position/time observations that produced it, and with them, the ability to recompute speed differently (over a different time window, with a different smoothing method, or corrected against a later understanding of sensor error) or to derive anything else the same acquired data could support.

Every discovered data point should be traceable, through the graph, to the acquired data it depends on. If a discovered value cannot be traced back to an acquired source, that is a signal that either an acquisition point is missing from the model, or the value is being treated as more fundamental than it actually is.

A discovered concept should not automatically become a stored concept. The ability to derive a value from existing data is often evidence that the value belongs to a view, projection, report, calculation, or contextual model rather than to the core model itself — `Speed` is exactly this kind of case: a legitimate, useful concept, but one that belongs downstream of the model rather than inside it.

#### Discussion

##### Rationale and alternatives
- **Treating all stored data uniformly (rejected)**: not distinguishing acquired from discovered data is the default in most schema-first designs, where every field is stored as though it were an equally primary fact. This makes it impossible to later tell which fields are recomputable and which represent irreplaceable source-of-truth information.

##### Unresolved questions
1. When a discovered value becomes expensive to recompute (e.g., an aggregation over a very large history of acquired data), at what point is it legitimate to also persist it as a cached, non-authoritative copy — and how should that copy be modeled so it is never mistaken for an acquired fact?

### Modeling State Change as Events, Not Destructive Updates
**The model should preserve reality before it preserves projections.** A concern's actual history of state changes — the sequence of facts that actually occurred — is reality. A concern's current field values, snapshots, or read-optimized views are projections of that reality, convenient but replaceable. Modeling should establish the former before committing to the latter, in the same way [acquired data must be preserved even when a discovered value is more immediately useful](#acquired-data-vs-discovered-data).

Two related situations are commonly, and mistakenly, treated identically in modeling:

1. Data that is inherently time-series in nature — for example, a sequence of position readings from a moving sensor, where every reading is meaningful on its own and none of them "replaces" a previous one.
2. Data that is not inherently time-series, but which the system nonetheless changes over time — for example, a user's `Username`. When a value like this changes, treating the change as a destructive, in-place update that overwrites the previous value discards information: the previous value, and the fact that a change occurred at a specific point in time, are themselves architecturally significant facts that many requirements eventually need. ("Who held the username `omid` before the current holder, and when did the change happen?" is a completely ordinary requirement that a destructive-update model cannot answer after the fact.)

Memar treats both situations as instances of the same underlying modeling concern: a change to a concern's state is itself an event, and event design is not separable from modeling that concern's structure and behavior. A concern's lifecycle should be modeled with the expectation that its history of state changes may need to be queried, not only its current state.

To be explicit about what this principle does not claim: it does not mean Event Sourcing, CQRS, or append-only storage are mandatory. This is a modeling-level concern, not an implementation or storage-engine mandate. This RFC does not prescribe event sourcing, a specific storage engine, or a specific persistence strategy as a required implementation approach — those are implementation-phase decisions addressed elsewhere. What belongs to modeling is the recognition that overwriting state without preserving its history is a decision with real, often unintended, architectural consequences, and that decision should be made deliberately during modeling rather than defaulted into by whichever storage technology a team happens to reach for. In practice, storage engines that operate above a raw key-value layer typically build indexes over exactly this kind of event history to answer queries efficiently — but how indexing is achieved is an implementation concern; that the history exists to be indexed is a modeling concern.

#### Discussion

##### Drawbacks
Treating every state change as a preservable event can be taken to an extreme where trivial, high-frequency, or genuinely inconsequential changes are all retained indefinitely, creating storage and query-performance concerns that have nothing to do with domain modeling. Not every state change carries architectural significance, and modeling should distinguish changes worth preserving from incidental ones rather than preserving everything by default.

##### Rationale and alternatives
- **Destructive update as the default (rejected)**: treating in-place overwrite as the default and history preservation as an opt-in special case is the dominant industry practice, inherited directly from relational `UPDATE` semantics. It silently discards architecturally significant information unless a team happens to think of history preservation in advance.
- **Mandatory event sourcing for all concerns (rejected)**: requiring every concern to be modeled as an append-only event log is appealing for consistency but conflates a modeling-level concern with an implementation-level commitment. Memar treats the *preservability* of state history as a modeling question and leaves *how* it is achieved to implementation.

##### Unresolved questions
1. What criteria distinguish a state change worth preserving as history from one that can be safely treated as a destructive update?
2. Should this concern be formalized as a distinct capability interface (analogous to the `Internal`, `Temporary`, `Timeout` capability interfaces used elsewhere in Memar's error abstraction) that a concern can opt into, rather than being an implicit property of every concern?

##### Future possibilities
A future RFC could define the relationship between this modeling-level concern and Memar's eventual persistence/storage architecture, including how event history is expected to be queried, without prescribing a specific storage engine.

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
A common misunderstanding is to start modeling by defining aggregators such as `User`, `Order`, `Project`, or similar high-level compositions and then placing other concerns inside them. Memar rejects this approach.

- **Aggregation is not a modeling primitive.**
- **Aggregation is a consequence of modeling.**

The purpose of modeling is first to discover concerns, responsibilities, lifecycles, and relationships. Only after those concerns have been understood may context-specific aggregators emerge. An aggregator is a context-specific assembly of independently discovered concerns — it does not introduce new responsibilities of its own; its sole purpose is to compose concerns that have already been modeled as separate abstractions. Because aggregation is shaped by use-case context rather than by domain structure, the same set of concerns may be aggregated differently in different contexts (e.g., a registration form vs. a profile-viewing page). Aggregators are therefore not modeling primitives; they are composition decisions that follow from the model. As a result, modeling should never begin by searching for a canonical aggregator. In many domains no single canonical aggregator exists at all. Different contexts may legitimately assemble the same concerns into different aggregations.

Memar rejects the conventional DDD pattern where a domain "owner" entity (e.g. `User`) directly contains and owns sub-concerns like `username`, `email`, or `password` as its own fields/methods. Instead, each such concern is modeled as its own independent abstraction, and any "User"-like concept is just one possible *aggregator* among several — aggregators are not fixed, singular, or domain-owned; they commonly form at the composition layer (GUI widgets/pages), though they are not limited to that layer.

The traditional aggregate-root pattern assumes a single, stable owning entity for a cluster of related data, but real systems frequently need different aggregations of the same underlying concerns depending on context. A canonical example: identity resolved via a local registration form needs a different aggregation shape than identity resolved via a third-party OAuth provider (e.g. Google login) — a single fixed `User` aggregator forces both flows into one shape that fits neither well, and tempts the owning entity to absorb logic (like credential validation) that does not actually belong to it.

`username`, `email`, and similar concerns are modeled as independent, self-contained abstractions with their own validation and behavior. A composition-layer construct (typically a GUI widget or page, though this is the common case, not the only one) assembles whichever subset of these independent abstractions a specific use case actually needs, and is responsible only for that assembly — not for absorbing the internal logic of the concerns it aggregates. Per [Composition Depth as a Decomposition Signal (No Expression Chaining)](./khayyam-composition_depth_as_decomposition_signal)'s decomposition-signal principle, if an aggregator's body starts doing more than its one named responsibility (e.g. a `RegisterComment` widget that also resolves "who is the current user"), that is the signal to split out a separate, dedicated widget (e.g. one that returns only an `ActiveUserID`), pushing that sub-concern's own validation and error-handling down into that separate widget rather than leaving it in the original caller.

A common misunderstanding is to interpret decomposition as merely extracting fields from a larger structure. For example, an `ActiveUserID` returned by a dedicated widget is not itself the concern being modeled. The actual concern is active-user resolution and selection: maintaining the currently active identity, enforcing any rules that govern identity switching, validating permissions, and exposing the selected identity to other parts of the system. The returned identifier is only an output of that concern, not the concern itself. This distinction is important because Memar decomposes systems around responsibilities and behavioral boundaries, not around individual pieces of data. A data value may appear in many places, but the responsibility that governs its creation, validation, and lifecycle should exist in exactly one place.

There is no language-level "aggregate root" or "entity" construct distinct from an ordinary abstraction realization. Any abstraction realization that happens to compose several other realizations is, structurally, just another realization — its role as an "aggregator" is a naming/architectural convention applied by the developer, not a special grammar feature.

An abstraction is not justified by the existence of data. An abstraction is justified by the existence of an independent responsibility, behavioral boundary, or lifecycle. Data decomposition is a consequence of responsibility decomposition, not the objective of modeling.

#### Discussion

##### Naming Conventions
An aggregator should be named after the use case it serves (e.g. `RegisterComment`, `LocalLoginForm`, `OAuthCallbackHandler`), not after the domain concept it assembles (e.g. `User`). This convention reinforces that the aggregator is a composition-layer construct with a single named responsibility, not a domain-owned entity.

##### Drawbacks
Without a single canonical owning entity, code that needs "the whole picture" of a concept like a user must always go through some composition-layer construct rather than a direct, centrally-defined object — this can mean more indirection to assemble a complete view, and requires discipline to avoid quietly re-inventing a de facto aggregate root inside a frequently reused widget. The approach also increases the number of abstractions in a system, which can make the overall architecture harder to navigate for newcomers who expect to find a `User` object that contains all user-related data and behavior.

##### Rationale and alternatives
- **Classical DDD aggregate-root pattern (rejected)**: a single, owning entity directly containing related sub-concerns. In practice, it tends to pull unrelated validation and identity logic into one type, and breaks down whenever a concept (like "the current user") genuinely has more than one valid shape depending on context (local form vs. OAuth-resolved identity).
- **Trait/mixin-based decomposition (considered, not chosen)**: defining concerns as mixins that are composed into a single entity at compile time. This addresses the code-organization concern but does not solve the architectural problem: the composed entity still has a single identity and lifecycle, which forces all contexts to share one shape.
- **Composition-root pattern from functional programming (considered, not chosen)**: assembling dependencies at a single composition root, as in pure dependency injection. Memar's approach is similar but applies at the concept level (abstractions) rather than the service level, and allows multiple composition roots for different contexts rather than a single application-wide root.

##### Prior art
This is closely related to, but distinct from, established critiques of Anemic/God-object Aggregate Roots within the DDD community itself; it also resonates with component-composition patterns common in modern frontend frameworks, where a "page" or "widget" composes several independent, narrowly-scoped pieces of state rather than a single monolithic model object. The principle that aggregation should happen at the composition layer rather than within the domain model also has parallels in the ports-and-adapters (hexagonal) architecture, where the domain core defines capabilities and the application layer assembles them into use cases.

##### Unresolved questions
1. What happens when two composition-layer widgets need the same aggregation but with slightly different validation rules? Is this handled by the abstractions themselves (context-aware validation) or by the aggregators (decorating the abstractions)?
2. Should there be a convention or lint rule that prevents an abstraction from directly accessing another abstraction's internal state, even when both are assembled by the same aggregator?

##### Future possibilities
A future RFC could define a formal "aggregation contract" — a lightweight protocol that specifies what an aggregator may and may not do with the abstractions it assembles, including constraints on accessing internal state, propagating errors, and managing lifecycle.

## Discussion

### Naming Conventions
This RFC does not introduce new naming conventions for implementation artifacts. The conceptual terms used here (abstraction, concern, aggregator, composition layer, graph) are established elsewhere in the Memar specification and are not redefined here.

### Drawbacks
The modeling approach described in this RFC demands significant upfront investment before any implementation progress is visible. For small or well-understood domains, the full graph-discovery process may be disproportionate to the complexity being managed. The approach also assumes that a team has access to domain expertise — if the domain experts are unavailable or the domain is poorly understood, graph exploration may produce a model that reflects the team's assumptions rather than the domain's actual structure.

### Rationale and alternatives
- **Ad-hoc modeling without a defined process (rejected)**: this is the default in most organizations. It produces inconsistent models whose quality depends entirely on the individual architect's skill and experience, without any mechanism for systematic improvement.
- **Heavyweight formal modeling (rejected)**: approaches like full UPDM or SysML modeling provide rigor but introduce tooling and expertise barriers that make them impractical for most software teams. Memar seeks a middle ground: systematic enough to be teachable and repeatable, lightweight enough to be applied without specialized tools.

### Prior art
The overall approach draws from multiple traditions: DDD (Eric Evans) for the emphasis on domain language and bounded contexts, Event Storming (Alberto Brandolini) for the practice of discovering domain structure through collaborative exploration, and graph theory for the analytical framework used to evaluate model structure. Memar's distinctive contribution is the integration of these traditions into a single, coherent modeling discipline that is tightly coupled with the abstraction and protocol constructs defined in other RFCs.

### Unresolved questions
1. Should Memar prescribe specific modeling workshops or exercises (e.g., event storming, domain storytelling) as part of the standard modeling process, or should the modeling technique remain entirely up to the team?
2. How should modeling be integrated into CI/CD pipelines? Can model quality be automatically checked (e.g., detecting cycles in the dependency graph, flagging abstractions without clear responsibilities)?
3. What is the recommended approach when a team inherits a legacy system with no existing model? Should they model from scratch and migrate, or incrementally extract the model from the existing codebase?

### Future possibilities
- A future RFC could define a model-quality linter — an automated tool that checks a graph for common modeling anti-patterns such as circular dependencies, overly broad abstractions, or concepts without clear responsibility boundaries.
- A future RFC could address the transition path from legacy systems to Memar-structured models, including strategies for incremental model extraction and migration.

## Change Rationale
- **Initial revision.** First structured revision of this RFC. Added `RFC Number` (495216, derived from the original Start Date). Migrated `Contributor(s)` from the deprecated `contribution`/`task` format to the `Tasks`-based format per the RFC Template Specification. Fixed `Related RFCs` `Reason` value for Terminology from the non-standard `"Foundation Alignment"` to `"Depends_on"`. Wrote the previously empty `Summary` and `Guide-level explanation` sections. Added `#### Discussion` bundles (with Drawbacks, Rationale and alternatives, Prior art, and where appropriate Unresolved questions and Future possibilities) to every Reference-level topic. Added the missing `## Discussion` and `## Change Rationale` sections. Converted plain-text internal references to hyperlinks. Added additional examples (e-commerce Order/Payment relationship) and expanded existing discussion points with deeper analysis and more alternatives.
- **Vocabulary separation revision.** Replaced all modeling-phase references to "capsule" with Discovery Vocabulary terms (abstraction, concern, conceptual boundary, responsibility). Clarified that capsules are implementation-level constructs and are not outputs of the modeling phase. Added the "Modeling Produces Abstractions, Not Capsules" section to establish a clear vocabulary boundary between the modeling phase (which produces abstractions, concerns, relationships, constraints, and supporting documents) and later architectural/implementation phases (which produce capsules, protocols, services, and other implementation structures). Rewrote the "Concept Existence vs. Model Existence" and "Domain Decomposition" sections to consistently use abstraction-level terminology throughout.
- **Discovery and behavior emphasis.** Added a paragraph to "Graphs Are Not Documentation Artifacts" clarifying that graphs serve as a discovery environment where questions, assumptions, and modeling decisions evolve alongside structure — not merely as visualization tools. Added the "Modeling Focuses on Behavior Before Structure" section to establish that a system's real complexity resides in what it does, not what it stores, and that modeling should prioritize behavioral understanding before structural decisions. Added an explicit definition of "aggregator" in the "Domain Decomposition over Aggregate-Root Modeling" section to prevent ambiguous interpretation across modeling, architecture, and composition contexts.
- **Phase relationships and systemic thinking.** Added the "Modeling, Protocol, and Architecture" section to clarify that these are not sequential pipeline phases but complementary aspects of a single architectural process — modeling discovers domain understanding, protocol captures it as knowledge contracts, and both are architectural in nature. Added a paragraph on systemic thinking to the guide-level explanation, emphasizing that modeling must examine how concerns interact across boundaries rather than partitioning the domain along organizational lines.
- **Attribute-or-edge test, naming precision, concurrent discovery, and event-aware state modeling.** Added "The Attribute-or-Edge Test" under "Concept Existence vs. Model Existence," operationalizing the independent-responsibility criterion as a mechanical check ("is this data owned here, or is it a named edge to an already-independent concern?"), using a `Product`/`Text` example that explicitly covers storage, validation, versioning, internationalization (i18n), and search as responsibilities properly owned by a shared `Text` abstraction rather than duplicated per node. Replaced the `Order`/`Payment` example in "Modeling Requires Explicit Relationship Analysis" with `Invoice`/`Financial Transaction`, and added an explicit note that word choice at the modeling stage is not cosmetic — `Order` and `Payment` were rejected because they smuggle in incorrect assumptions about workflow outcome and implementation layer. Renamed "Modeling Focuses on Behavior Before Structure" to "Behavior and Structure Are Discovered Together" and rewrote it to clarify that behavior and structure are discovered concurrently rather than in strict sequence, while retaining the discipline of interrogating every proposed node or edge for its behavioral consequences immediately; this also resolves an internal tension with the adjacent "Behavior Often Reveals the Quality of the Model" section, which already described behavior as co-discovered rather than sequentially deferred. Added "Acquired Data vs. Discovered Data" as a complementary lens to the existing Fundamental/Derived distinction, with a position/velocity example illustrating why a discovered value should not be stored as if it were an acquired one. Added "Modeling State Change as Events, Not Destructive Updates," establishing that state changes are architecturally significant events to be modeled deliberately — covering both inherently time-series data and ordinary field changes (e.g. `Username`) — without prescribing any specific storage engine or persistence strategy.
- **Independence signal, event framing, and discovery entry point (ChatGPT/GPT-5.5 review incorporated).** Added "Reuse Across Contexts as an Additional Signal" beneath the Attribute-or-Edge Test, framing cross-context reuse as a corroborating but non-required signal for independent-abstraction status, with `Text` (reused) and `Invoice` (not reused, still independent) as contrasting examples; this avoids overstating reuse as the primary criterion, which independent responsibility/lifecycle remains. Established the `Product`/`Title`/`Text` example as a recurring reference example, and cross-referenced it from the `Invoice`/`Financial Transaction` example so the structural (attribute-vs-node) and behavioral (invariant-ownership) lessons remain distinct but mutually discoverable. Added an explicit "a discovered concept should not automatically become a stored concept" principle to "Acquired Data vs. Discovered Data." Reordered "Modeling State Change as Events, Not Destructive Updates" to lead with "the model should preserve reality before it preserves projections" and an explicit disclaimer that Event Sourcing, CQRS, and append-only storage are not thereby mandated, rather than leaving that disclaimer implicit until later in the section. Added "Initial Discovery Questions," a short checklist distinguishing *how to begin* discovering abstractions from the rest of the RFC's treatment of *what a good abstraction looks like*, explicitly scoped as an entry point rather than a gate.
