---
Title: "Modeling"
Status: Proposed
Start Date: 2026-06-30
ID: 495220
---

# Modeling

## Abstract
This document defines how Memar approaches modeling: treating the model as the primary architectural artifact, discovering it through graph-based exploration before any implementation commitment, and decomposing the domain around independent responsibilities rather than data ownership or presentation structures. It establishes that an abstraction is justified by an autonomous responsibility and lifecycle, not by the existence of data; that adaptability emerges from model quality, not from technology choices; and that behavioral complexity is a modeling smell rather than a requirement. The aggregate-root pattern of conventional DDD is rejected in favor of composing independent concerns at the composition layer, with no single fixed owning entity. Crucially, the output of the modeling phase is conceptual: abstractions, concerns, relationships, constraints, boundaries, and supporting documents. It does not prescribe implementation structures.

## Introduction

### Motivation
The framework should prevent incorrect models before implementation and reduce the cost of correction when mistakes inevitably occur. In practice, most architectural rigidity does not originate from poor technology choices — it originates from models that conflate unrelated concerns, mirror presentation structures, or bind responsibilities to fixed owning entities. Once a flawed model propagates into databases, APIs, user interfaces, and deployment pipelines, every subsequent correction carries compounding cost. Memar therefore needs an explicit, opinionated modeling discipline that maximizes the quality of the model before implementation begins and preserves the ability to evolve it afterward.

### Methodology
Memar approaches modeling as graph-based discovery rather than schema design: concepts and relationships are proposed provisionally, challenged against the criteria established throughout this document, and retained only once they survive that challenge.

Modeling inherently requires systemic thinking — examining how concerns interact, how behaviors propagate across boundaries, and how decisions in one part of the system affect behavior in another. A modeling effort that examines concepts in isolation, or that partitions the domain along organizational or team boundaries (e.g., frontend vs. backend) rather than along natural concern boundaries, will produce a model that reflects organizational structure rather than system behavior. Many architectural failures — a retry mechanism that degrades user experience, an error message that exposes internal failures, a validation step placed at the wrong point in a workflow — originate not from poor modeling of individual components but from a failure to model the system as a whole.

## Explanation

### What a Model Is
A **model** is a simplified representation of a system or aspect of reality, constructed to facilitate understanding, analysis, prediction, communication, or transformation.

Models are composed of abstractions and relationships. They preserve information that is relevant to a specific purpose and discard information that is not. No model captures its target in full; the act of modeling is inherently selective, and the quality of a model is judged not by how much it includes but by how well it serves its stated purpose.

A model may be formal or informal, mathematical or visual, textual or computational. An equation that describes orbital mechanics is a model. A diagram that describes a software system's component structure is a model. A natural-language description of a business process is a model. The medium of the model is less important than the rigor and purpose with which it is constructed.

This definition is grounded in the [System document](./system.md), where Model is defined as a concept in the Scientific terminology layer: its meaning is rooted in the philosophy of science and systems theory, defined with explicit boundaries, and intended to be open to criticism and revision.

#### Models Are Not Reality
A model is not the thing it models. This distinction — between the map and the territory, the representation and the represented — is one of the oldest and most frequently violated principles in intellectual history. Confusing a model with reality leads to several well-documented failures:

- Treating an economic model as if it fully describes economic behavior, leading to policy decisions that fail when real behavior deviates from model assumptions.
- Treating a software architecture diagram as if it fully describes the running system, leading to maintenance decisions that fail when the actual runtime behavior differs from the diagrammed structure.
- Treating a data model as if it fully describes the domain it represents, leading to application behavior that fails when real-world entities exhibit properties the model did not anticipate.

Within Memar, every model should be treated as a tool with known limitations, not as a complete description of its target. Memar's modeling process should include explicit mechanisms for identifying and documenting what each model deliberately omits.

The distinction between models and reality is discussed extensively in philosophy of science, most accessibly in Box and Draper ("Empirical Model-Building and Response Surfaces," 1987) and in the broader systems modeling literature.

### One Reality, Multiple Abstraction Lenses
A single aspect of reality can be modeled through more than one co-equal abstraction lens. A structural lens asks what exists and how it is organized; a behavioral or process lens asks how it acts and progresses; a normative lens asks what rules govern that behavior; a systemic lens asks how parts interact within boundaries to produce emergent results. These lenses are modes of observation applied to one reality — they are not levels of a hierarchy, and they are not entities inside the produced model.

Conflating a lens with a modeled entity is a recurring category error in modeling discussions. Statements such as "the structural view of X", "the process view of X", and "the rule view of X" name three observations of one concern, not three concerns to be discovered, named, and stored alongside it. When a modeling session starts producing parallel structures whose only difference is the lens they were observed through, that is usually evidence that one concern has been counted several times.

The lenses are complementary rather than competing: each reveals aspects the others abstract away, and all may describe the same underlying reality simultaneously without contradiction (see [System → A Note on Systems Thinking](./system.md#a-note-on-systems-thinking) for the general claim that system-hood itself is such a lens, and [Process → Observation](./process.md#observation) for why different observers of the same process may legitimately report different, genuinely real aspects of it). Which lens deserves attention at a given moment follows from the concern being addressed; a modeling effort that exercises only one lens tends to leave the discovered structure silently shaped by that lens's blind spots — most commonly, structure discovered purely structurally and behavior retrofitted afterward.

### Initial Discovery Questions
Understanding what a model is (see above) does not by itself tell a modeler where to begin when facing an unstructured requirement — a lengthy specification document, a stakeholder interview, or an existing but undocumented system. The concrete entry-point questions a modeler asks before proposing any node are execution practice rather than architectural definition, and are not restated here. Answering them produces the first provisional candidates that the rest of the modeling process (see [Challenging Proposed Concepts](#challenging-proposed-concepts)) then interrogates, tests, and refines.

### Initial Discovery Questions
Understanding what a model is (see above) does not by itself tell a modeler where to begin when facing an unstructured requirement — a lengthy specification document, a stakeholder interview, or an existing but undocumented system. The concrete entry-point questions a modeler asks before proposing any node are execution practice rather than architectural definition, and are not restated here. Answering them produces the first provisional candidates that the rest of the modeling process (see [Challenging Proposed Concepts](#challenging-proposed-concepts)) then interrogates, tests, and refines.

### The Model as the Primary Artifact
Modeling in Memar means discovering the natural structure of a domain before writing any implementation code. The output of modeling is not a database schema, not an API definition, and not a class hierarchy — it is a graph of concerns, responsibilities, and relationships that reveals where the real architectural boundaries lie.

Memar treats the domain model as the primary architectural artifact of a system. The purpose of implementation is not to define the model. The purpose of implementation is to realize a model that has already been discovered and validated. A successful implementation does not prove that a model is correct. It only proves that the model can be implemented. This distinction is important because implementation introduces irreversible costs. Once a model is reflected in databases, APIs, user interfaces, deployment pipelines, integrations, and operational procedures, changing the model becomes increasingly expensive.

For this reason, Memar encourages extensive model exploration before implementation and seeks to minimize the coupling between implementation details and domain concepts. The closer a system keeps its implementation aligned with the model, the easier it becomes to evolve the architecture when new understanding emerges. The model should remain the source of truth. Implementations are merely projections of that truth into specific technological contexts.

The idea that the model precedes and constrains the implementation is central to model-driven architecture (MDA) as defined by the OMG, and to Eric Evans' Domain-Driven Design, which argues that the domain model should be the heart of the software. Memar's contribution is not the principle itself but the specific mechanisms (graph-based discovery, conceptual boundaries, protocol separation) that make the principle practically enforceable.

### Modeling Produces Conceptual Abstractions, Not Implementation Structures
The output of modeling is entirely conceptual. The primary outputs of modeling are:

* Abstractions
* Concerns
* Responsibilities
* Relationships
* Constraints
* Conceptual Boundaries
* Supporting Documents

These artifacts describe the domain independently of any implementation strategy. Modeling should therefore avoid prematurely deciding how an abstraction will be realized in code, services, classes, databases, APIs, or other implementation-oriented structures. Such realizations belong to later architectural and implementation work. The objective of modeling is to discover the abstractions that exist within the domain and the relationships and rules that define them, not to decide how those abstractions will eventually be implemented.

### Modeling, Protocol, and Architecture
Modeling, Protocol, and Architecture are not sequential phases in a linear pipeline. In Memar, architecture encompasses the entire process of designing and building a system — from initial domain discovery through implementation. Modeling and Protocol are complementary aspects of this overarching architectural process.

Modeling discovers the abstractions, concerns, responsibilities, relationships, and behavioral expectations that exist within a domain. Protocol captures and constrains those discoveries as stable knowledge contracts. A protocol is not merely an interface definition or a communication contract — it is the structured knowledge that governs how a concern is understood, constrained, and interacted with, encompassing concepts, abstractions, constraints, relationships, behaviors, rules, and eventually their realizations. The model produced by modeling is not separate from the protocol; it becomes part of the protocol's knowledge base. As modeling deepens understanding of a domain, that understanding is absorbed into the protocol. As implementation progresses, the protocol ensures that the relationship between understanding and realization remains transparent and enforceable.

This means the boundary between modeling and protocol is not a hard phase transition — it is a gradual shift in emphasis from discovery to formalization. Early in a project, modeling dominates and the protocol is thin. As understanding matures, the protocol grows richer and begins to constrain implementation decisions. Both activities remain architectural in nature: they are decisions about the system's structure and behavior, made before and during implementation.

A word of caution on terminology: "process," as used throughout this document — a business process, the modeling process, the process of designing a system — is ordinary English, not a claim about Memar's formal **Process** concept. Memar does define Process formally, in its own document, and that formal definition is what Protocol actually governs (see [System → contains → Processes → governed by → Protocols](./protocol.md#protocol-process-and-system)). When modeling surfaces a domain's behavioral expectations — what happens, in what order, under what failure conditions, with what retry or cancellation semantics — it is discovering processes in that formal sense, not merely informal activity. A model is therefore not finished once its abstractions and their static relationships are settled; it must also account for the processes those abstractions participate in. See [Process](./process.md) for the full treatment — in particular, its warning against treating failure as automatically implying rollback, or concurrency as automatically implying a lock, both of which are exactly the kind of premature-mechanism thinking this document's own "process-before-mechanism" and "adaptability emerges from modeling, not technology" principles argue against for structure. Do not assume the ecosystem-default, informal sense of "process" is what Memar means by the term; check the Process document itself.

For a detailed discussion of Protocol, see the [Protocol document](./protocol.md). For the formal definition of Process, see the [Process document](./process.md). For terminology definitions, see the [Terminology document](./terminology.md).

### Models Must Survive Implementation Changes
A model should not become difficult to change merely because an implementation already exists. One of the primary responsibilities of architecture is to preserve the ability to evolve domain understanding over time. As knowledge grows, previously accepted models may be refined, decomposed, consolidated, or replaced. Such changes should be treated as normal architectural evolution rather than exceptional events.

Memar therefore places significant emphasis on protocols as stable boundaries between models and their implementations. A protocol defines the observable contract of a concern without exposing the implementation decisions behind it. By preserving this separation, implementations can evolve, migrate, or even be completely replaced while minimizing the impact on the surrounding architecture.

For a detailed discussion, see the [Protocol document](./protocol.md).

The principle that stable interfaces should outlive their implementations is foundational in software engineering, from Parnas' 1972 paper on information hiding to the interface-segregation principle in SOLID design. Memar's protocol concept extends this principle by making it a first-class architectural construct rather than a coding convention.

### Adaptability Emerges from Modeling, Not Technology
Architectural adaptability is often incorrectly attributed to implementation technologies. Technologies such as REST, gRPC, messaging systems, databases, or programming languages can influence development costs, but they do not fundamentally determine the adaptability of a system. The primary factor that determines how easily a system evolves is the quality of its underlying model.

A well-structured model can often survive major implementation changes with limited disruption. A poorly structured model remains difficult to evolve regardless of the technologies used to implement it. For this reason, Memar focuses first on discovering stable conceptual boundaries and only then on selecting implementation technologies.

**Technology choices should serve the model, not define it.**

The observation that architecture is dominated by model quality rather than technology choice echoes arguments in Ralph Johnson's "Frameworks = Components + Patterns" and more recently in the "bounded context" concept from DDD, where the quality of the context boundary matters far more than the technology used within it.

### Modeling Requires Explicit Relationship Analysis
A domain model cannot be discovered by analyzing entities in isolation. Concepts derive much of their meaning from their relationships with other concepts. Therefore, modeling must focus not only on identifying nodes but also on identifying and understanding the relationships that connect them.

Many traditional modeling approaches inherit assumptions from relational database design, where relationships are often reduced to foreign keys, join tables, and storage-oriented structures. As a result, relationships frequently become implementation details rather than first-class modeling concerns.

Memar takes a different approach.

Relationships are architectural information. They often reveal responsibilities, boundaries, ownership, lifecycle dependencies, and behavioral constraints that cannot be discovered by examining concepts independently. A model should therefore be evaluated as a graph of interacting concerns rather than as a collection of isolated structures.

For example, consider `Invoice` and `Financial Transaction`. These are related via a reference edge — an `Invoice` references the `Financial Transaction`s recorded against it — but the invariant governing when an `Invoice` may transition to a `Paid` status is not owned by a third, aggregating entity. It is owned by `Invoice` itself, as part of its own state-transition responsibility: the method that attempts the transition to `Paid` traverses its reference edges to the related `Financial Transaction` nodes, sums their amounts, and only permits the transition if that sum meets or exceeds the invoice total. `Financial Transaction`, in turn, owns its own validation and lifecycle independently of any `Invoice` — it does not need to know about invoices to be valid.

This illustrates that a cross-concern invariant does not require a shared owning entity or a composition-layer aggregator to be enforced correctly. It requires only that the concern whose lifecycle the invariant actually gates — here, `Invoice`'s transition to `Paid` — reads what it needs from its own edges to already-independent nodes. The invariant is not split, duplicated, or homeless; it belongs entirely to the one concern whose state it governs, without that concern absorbing the internal validation logic of the nodes it references. Examining `Invoice` and `Financial Transaction` in isolation would miss all of this.

`Invoice`/`Financial Transaction` illustrates where a cross-concern behavioral invariant lives once aggregate-root ownership is rejected. For the complementary, more structural question of when a concept deserves its own node at all, see the recurring `Product`/`Title`/`Text` example in [The Attribute-or-Edge Test](#the-attribute-or-edge-test).

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

### Edge Types and Their Traditional Counterparts
Three structurally distinct kinds of edge recur across every graph model, and they are worth naming precisely because the difference between them is easy to miss:

* An **edge** connects two distinct nodes. What it represents — reference, ownership, or anything else — is open-ended and not enumerated exhaustively by this document (see below); what makes it this first kind of edge is simply that it has two different nodes at its ends.
* A **loop-edge** connects a node to itself. It is easy to overlook as its own category — many modelers only ever think in terms of edges joining two different things — but a self-referencing edge is structurally different from an ordinary edge, and Memar gives it a dedicated role: naming a candidate or established classification of the node it is attached to (see [Classification Emerges From Rules and Relations, Not From Intrinsic Labels](#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels)). Traditionally, this is the counterpart of a `type` column, or a row's membership in a specific table under table-per-type inheritance.
* A **shortcut edge** carries no new architectural information on its own. It exists purely to make an already-derivable traversal cheaper to compute. For example, determining whether an `Invoice` was paid in cash would otherwise require traversing every `Financial Transaction` connected to it and checking, for each one, whether its receiving account carries a `Cash_Account` label — a shortcut edge can instead connect `Invoice` directly to that already-derived fact. This is the graph-native counterpart of a database index or a materialized, denormalized column. A shortcut edge deserves particular caution: it must never become the source of truth for the information it shortcuts. It is only ever a cache of a fact derivable from other edges already in the graph, and should be modeled and named in a way that makes clear it is not itself authoritative — the same discipline already established for [Acquired vs. Discovered data](#acquired-data-vs-discovered-data) applies here: a shortcut edge is discovered, not acquired, and must always remain re-derivable from the edges that produced it.

An ordinary edge — the first kind above — can still play many different roles, and naming a few recurring ones is useful for building a shared vocabulary and recognizing traditional-modeling counterparts, without treating the list as closed or mandatory:

* A **reference** — a named pointer from one node to another that the referencing node depends on but does not own, e.g. `Product --(Title)--> Text` (see [The Attribute-or-Edge Test](#the-attribute-or-edge-test)). Traditionally, this is a foreign key.
* An **ownership/composition** relationship — the lifecycle of the referenced node is bound to the owning node, which has no independent existence outside it. Traditionally, this is an embedded/owned row, or a foreign key with cascading delete.

The edge/shortcut-edge distinction parallels the general/index-or-materialized-view distinction across both entity-relationship modeling and property-graph databases; the loop-edge draws on the same reification pattern discussed under [Classification Emerges From Rules and Relations, Not From Intrinsic Labels](#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels).

### Graphs Are Not Documentation Artifacts
In Memar, graphs are not used merely to visualize a model that has already been discovered. Graphs are used as a discovery mechanism. The purpose of graph analysis is to expose relationships, dependencies, responsibilities, and architectural structures that may not be visible through implementation-oriented perspectives.

A graph is therefore not the final documentation of a model. It is one of the primary tools used to discover the model itself. This distinction is important because many modeling approaches treat diagrams as explanatory artifacts produced after design decisions have already been made. Memar instead treats graph exploration as part of the design process itself.

Furthermore, graphs serve as a discovery environment where concepts, relationships, questions, assumptions, discussions, and modeling decisions can evolve together. The value of graph-based modeling is therefore not limited to representing structure — it also supports the exploration and refinement of the model itself. Questions posed about a node, challenges raised against an edge, and assumptions recorded during discussion all become part of the modeling context that the graph carries. In table-driven or schema-driven modeling approaches, these observations often go unrecorded entirely.

The practical consequence is that a graph is expected to change frequently during modeling. It is a working tool, not a polished deliverable. A graph that has not been revised multiple times during the modeling process is likely a graph that has not been used seriously as a discovery mechanism.

The distinction between "design as discovery" and "design as documentation" parallels the distinction between exploratory data analysis and confirmatory data analysis in statistics. In both cases, the exploratory phase uses flexible, informal tools, while the confirmatory phase produces structured, auditable artifacts.

### Behavior and Structure Are Discovered Together
Structures are often the first thing stakeholders can articulate — entities, fields, and data relationships come easily to describe. Behaviors are usually harder to surface and often only emerge through careful, repeated questioning. This does not mean structure and behavior belong to separate phases of modeling, one strictly preceding the other; in practice, both surface together on the same whiteboard, in the same conversation, and in the same graph-editing session, and a modeler should not attempt to suppress structural thinking until some declared "behavior phase" is complete.

What the modeling process must guard against is treating a structure as settled before its behavioral implications have been questioned. A system's real complexity resides not only in what it stores but in what it does: how it responds to failure, how it handles concurrent operations, how it recovers from inconsistent states, how it communicates delays to users, and how it enforces rules across temporal boundaries. A node or edge proposed in the graph should be interrogated for its behavioral consequences as soon as it is proposed — not deferred to a later pass — precisely because behavior and structure inform each other continuously throughout modeling. A retry mechanism designed without considering user experience, an error message that exposes internal failures, or a validation step placed at the wrong point in a workflow — these are all behavioral failures that stem from structure that was allowed to calcify before its behavioral implications were questioned.

The vocabulary in the previous paragraph — failure, retry, concurrency, recovery — is not incidental; it is exactly the vocabulary [Process](./process.md) treats formally, including its caution against assuming failure implies rollback or concurrency implies a lock before the actual requirement has been understood. A modeler surfacing "what the system does" is, in Memar's terms, discovering process; this section's behavioral questions and that document's formal treatment describe the same underlying activity from two different points in the framework.

A model that captures both together tends to reveal appropriate structures naturally. A structurally elegant model produced without equal attention to behavioral expectations will inevitably require expensive corrections once implementation exposes the gaps.

The principle that behavior deserves equal attention to structure is central to behavior-driven development (BDD) and to event-storming, where domain events — behavioral occurrences — are a primary discovery mechanism alongside structural ones. Memar's contribution is treating this as continuous, disciplined co-discovery within graph-based modeling, rather than either a separate development practice or a strictly sequential phase.

### Behavior Often Reveals the Quality of the Model
In Memar, behavior is not treated as an independent concern that is discovered only after structural modeling is complete. A well-formed graph frequently constrains and reveals the space of valid behaviors. As concepts, responsibilities, and relationships become clearer, many behavioral expectations emerge naturally from the model itself. For this reason, unusual behavioral complexity should often be treated as a signal rather than a requirement.

When a system requires an increasing number of special cases, exceptions, coordination rules, translation layers, synchronization mechanisms, or procedural workarounds, the underlying model should be re-examined before additional implementation complexity is introduced. In many cases, behavioral complexity is not evidence of a sophisticated domain. It is evidence that responsibilities, boundaries, or relationships have not yet been modeled correctly.

**A mature model tends to simplify behavior. An immature model often transfers its complexity into implementation.**

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

### Modeling Before Implementation
Modeling should reach a sufficient level of maturity before implementation begins. Once a concept enters implementation, every subsequent change becomes progressively more expensive due to dependencies in storage, APIs, user interfaces, tests, deployment pipelines, and operational procedures. For this reason, Memar encourages extensive exploration at the modeling stage before committing to implementation decisions.

A proposed model should be continuously challenged against the same criteria used throughout modeling (see [Challenging Proposed Concepts](#challenging-proposed-concepts)) — this is not a separate, implementation-adjacent check, but the same discipline applied at the point where the cost of getting it wrong is about to rise sharply.

For example, a team may initially introduce a `Comment` model. Before implementation begins, the model should be examined against existing concepts such as `Content`. The goal is not to maximize reuse, but to determine whether a genuinely new responsibility exists or whether the proposed model is simply a contextual specialization of an already existing concept.

The cost of redesign is lowest during modeling. Therefore, the majority of conceptual consolidation should happen before implementation rather than after it.

### Challenging Proposed Concepts
Every newly proposed concept should be assumed to be provisional until it survives critical examination. The purpose of modeling is not to collect concepts. The purpose of modeling is to discover whether a proposed concept represents a genuinely independent responsibility. The specific set of challenge questions a team runs a proposed concept through is execution practice and is not restated here.

A concept that cannot justify its existence should not become an independent abstraction.

Without explicit challenge rules, teams tend to accept concepts too quickly and reproduce presentation structures inside the model.

### Assumptions Are Modeling Targets
During modeling, statements from stakeholders should be treated as hypotheses rather than facts.

- **The responsibility of the modeler is not to record assumptions.**
- **The responsibility of the modeler is to test them.**

For example, a stakeholder statement such as `"We need a Comment model."` is an assumption to be tested, not a requirement to be recorded — the modeler's job is to determine whether `Comment` names a genuinely new responsibility or merely a presentation distinction on top of an existing concept such as `Content` (see [Challenging Proposed Concepts](#challenging-proposed-concepts) for the fuller test).

Modeling progresses through validated assumptions, not collected assumptions.

### Questions Are Architectural Tools
Questions are not merely a communication mechanism. A good modeling question can eliminate entire branches of an incorrect model before implementation begins. Modeling sessions should prioritize discovering better questions rather than producing more diagrams. A team that rapidly creates concepts without questioning them is usually documenting assumptions rather than modeling the domain.

### Early Indicators of Modeling Progress
[Graph stability](#graph-stability-as-an-indicator-of-model-maturity) is retrospective and cannot guide a team's first few sessions. Before it becomes observable, a smaller set of earlier, session-level signals can indicate convergence without proving maturity.

### Expected Output of a Modeling Session
A modeling session does not need to produce implementation artifacts, database schemas, APIs, or finalized abstraction definitions to be successful. Its success is measured by improved understanding of the domain.

### Concept Existence vs. Model Existence
A recurring source of confusion in modeling discussions is the assumption that every identifiable concept must become an independent model element. Memar does not make this claim. The existence of a concept and the existence of a dedicated model are separate questions.

An abstraction — the primary output of Memar's modeling phase — is not justified by the existence of data. An abstraction is justified by the existence of an independent responsibility, behavioral boundary, or lifecycle. Data structures are consequences of responsibility decomposition, not its drivers.

The working distinction underneath these criteria: a **concept** has semantic identity — it participates in the model and may own behavior and rules — while **data** represents information and does not necessarily have independent identity of its own. A `Person` is a concept and a birth date is its data; a `Contract` is a concept and its description field is its data.

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

A future document should provide formal criteria for determining when a concept becomes an independent abstraction and when it should remain a derived or contextual representation of another concept.

#### The Attribute-or-Edge Test
A practical operationalization of the "independent responsibility" criterion is available directly from the graph itself: for any data point a node appears to need, ask whether that node actually owns the responsibility for that data, or whether the requirement is better expressed as an edge to an already-independent node.

For example, when modeling a `Product` node, the requirement "a product needs a name" does not automatically justify a `ProductName` field on `Product`. The question to ask is: does `Product` — or indeed any node that merely references text — carry the responsibility of storing, validating, versioning, internationalizing (i18n), and making the textual content searchable? In most domains it does not — that responsibility already belongs to a general-purpose `Text` abstraction, used identically for comment bodies, article titles, or any other free-form content. The correct model is therefore not a `ProductName` attribute, but an edge — e.g. `Product --(Title)--> Text` — where `Title` names the relationship and the referenced `Text` node owns the concern of holding, validating, translating, and indexing textual content.

Concentrating text-handling responsibility into a single concern this way resolves two problems that otherwise recur across nearly every domain:

* **Internationalization.** When text is duplicated as ad-hoc string fields across many unrelated nodes (`ProductName`, `CategoryTitle`, `UserBio`, and so on), adding a new language requires touching every one of those nodes and every schema that stores them. When all free-form text is instead a reference to a single `Text` abstraction, multilingual support is a concern the `Text` abstraction alone owns and evolves — no other domain needs to change, even retroactively, for content that existed before internationalization was considered.
* **Search.** When the textual source of truth is scattered across every domain, a search capability has no choice but to reach into every one of those domains individually to answer even a simple text-based query. When text is centralized behind one abstraction, that abstraction becomes the natural place to build indexing and search capability once, rather than once per domain.

This test — "is this data owned here, or is it a named relationship to an already-independent concern?" — gives modelers a concrete, graph-native way to apply the single-responsibility principle without relying purely on intuitive judgment. It does not eliminate subjectivity in the harder cases (see Unresolved Questions below), but it converts many everyday attribute-vs-abstraction decisions into a mechanical check against the existing graph.

The `Product --(Title)--> Text` example is used as a recurring reference example throughout this document precisely because it exercises internationalization, search, versioning, reuse, and derived-structure concerns in a single, small graph — it is worth returning to whenever a new principle needs a concrete illustration.

#### Reuse Across Contexts as an Additional Signal
The Attribute-or-Edge Test answers a narrower question than the one it is sometimes mistaken for. It tells a modeler whether a piece of data belongs to the node that appears to need it, or to an edge pointing at an already-independent node. It does not by itself explain why a node such as `Text` is independent in the first place, as opposed to `Title` or `ProductName`, which are not.

Independent responsibility, behavioral boundary, or lifecycle (see above) remains the primary criterion for justifying an abstraction. Reuse across contexts is a strong, but not required, corroborating signal: when the same responsibility is needed by multiple otherwise-unrelated concerns — as `Text` is needed by `Product`, `Comment`, and `Article` alike — that recurrence is strong evidence the responsibility does not belong to any single one of them, which is exactly what "independent responsibility" means in practice. `Title` and `ProductName`, by contrast, are not independently reused anywhere — they are names for a relationship and an unnecessary duplication, respectively — which is why neither warrants its own node.

The absence of reuse does not disqualify a concept from independent-abstraction status. `Invoice` (see [Modeling Requires Explicit Relationship Analysis](#modeling-requires-explicit-relationship-analysis)) is used in only one context — financial/billing — yet still warrants its own abstraction, because its lifecycle and responsibility are independent regardless of how many other concerns reference it. Reuse strengthens the case for extraction; it is not the test itself, and a modeler should not withhold an abstraction from a concept with a clear independent lifecycle merely because that concept has not yet appeared in a second context.

The distinction between fundamental and derived concepts parallels the "value object" vs. "entity" distinction in DDD, but Memar extends it beyond data identity to encompass responsibility and lifecycle. The "contextual view" category is informed by CQRS (Command Query Responsibility Segregation), where the same underlying data may be projected into multiple read-model shapes without each projection becoming an independent architectural element.

### Classification Emerges From Rules and Relations, Not From Intrinsic Labels
A common modeling mistake is to treat classification as an intrinsic property of a node. Terms such as *Instruction*, *Memory*, *Skill*, *Procedure*, or *Research Artifact* are often assumed to describe fundamentally different kinds of things from the moment they are created. From a modeling perspective, this assumption should be questioned. Before classification, all of these artifacts may be viewed simply as unclassified content — a base node that has not yet acquired any of these identities.

A classification is not an inherent property of a node. It emerges when the node satisfies a specific set of rules that allow it to participate in a particular role or relationship. A piece of content may be considered an *Instruction* because it satisfies the rules required for guiding behavior; a *Memory* because it satisfies the rules required for long-term contextual reuse; a *Procedure* because it satisfies the rules required for repeatable execution. The classification does not exist independently of the rules that justify it.

The criterion is therefore a completable sentence: *[artifact] may be classified as [label] because it satisfies rules […], and therefore participates in relations […]*. A label that cannot complete that sentence — because the rules are not stated, or because no relation the model recognizes opens up once it applies — is a label, not a classification, however confidently it is used in the conversation. The checks that surface this during a session are execution practice; see [Modeling Practice → Premature Classification Check](./modeling.practice.md#premature-classification-check).

Graph-based modeling gives this principle a concrete mechanical form. A candidate classification can be represented as a self-referencing (loop) edge on the unclassified base node — a provisional label that says "this node may be an X" without yet committing to X as an independent concept. Whether that label is ever promoted from a loop-edge into its own, independently referenced node follows the same test already established in [Concept Existence vs. Model Existence](#concept-existence-vs-model-existence): the label is promoted only when it itself carries an independent responsibility, behavioral boundary, or lifecycle. Not every loop-edge is a candidate for promotion — a `Status` loop-edge (e.g. marking a node `Active` or `Archived`) rarely carries independent responsibility of its own, and correctly stays a loop-edge rather than becoming a node. This is not a separate promotion criterion; it is the same independent-responsibility test applied to loop-edges specifically, giving [The Attribute-or-Edge Test](#the-attribute-or-edge-test) a sibling for the node-vs-loop-edge question, alongside the attribute-vs-edge question it already answers.

Two recurring gray zones in this classification deserve explicit treatment, because both are commonly mistaken for promotion or demotion criteria. The first is incidental metadata: a label carrying a field that merely records when or in what scope it applies (a timestamp on a status marker, a scope parameter on a permission) has not thereby become a data-carrying concern in its own right — the test remains whether an independent responsibility exists, not whether any field happens to be present. The second is temporal: something classified today may evolve until its rules justify independence tomorrow. Such a graduation from label to node is legitimate, but it is a modeling decision to be made explicitly at each evolution point under the same test, never assumed silently in either direction.

Once a classification is established, it can unlock relationship types that are explicitly valid only between nodes sharing that classification — for example, a `Substitute` edge, defined once for a given classification, may be used to mark two nodes as functional stand-ins for each other (two `Product`s that satisfy the same customer need, say), regardless of what other classifications either of them separately carries. This is explicit reuse at the abstraction level, not implicit inheritance: the base node does not silently gain behavior from an ambient hierarchy; it gains the ability to participate in specific, named relationships because it explicitly satisfies the rules that define a specific classification.

This perspective helps reduce unnecessary type proliferation, prevents terminology from being mistaken for structure, and gives the [Reuse Across Contexts](#reuse-across-contexts-as-an-additional-signal) signal a mechanical trigger: the more often a given loop-edge label recurs across otherwise-unrelated base nodes with its own consistent rules, the stronger the case that it deserves promotion into an independent node in its own right.

The loop-edge-to-node promotion mechanism echoes reification in knowledge representation — the process by which a relationship or property is "promoted" into a first-class entity in its own right when it needs to carry further properties or relationships of its own. It also parallels the multi-label mechanism found in property-graph databases, where a single node may carry several labels simultaneously, while adding the further discipline of an explicit promotion criterion rather than treating every label as equally durable.

### Acquired Data vs. Discovered Data
A complementary lens for distinguishing fundamental concepts from derived ones (see [Concept Existence vs. Model Existence](#concept-existence-vs-model-existence)) is to ask, for any candidate data point, whether it is **acquired** or **discovered**:

* **Acquired data** is stated directly by an external source — typically a user, a sensor, or another system — and cannot be recomputed from anything else already in the model. It is a primary fact.
* **Discovered data** is derived from acquired data (or from other discovered data) through computation, aggregation, or inference. It is not a primary fact; it is a view.

This question exposes a common modeling mistake: storing a discovered value as though it were acquired, thereby losing the underlying acquired data it was computed from. For example, a system tracking a moving object should acquire and store the object's position and time of observation — these are the primary facts a sensor or user actually reports. Velocity and acceleration are discovered: they are computable from a sequence of position/time observations. Modeling `Speed` as if it were itself an acquired, independently stored value discards the position/time observations that produced it, and with them, the ability to recompute speed differently (over a different time window, with a different smoothing method, or corrected against a later understanding of sensor error) or to derive anything else the same acquired data could support.

Every discovered data point should be traceable, through the graph, to the acquired data it depends on. If a discovered value cannot be traced back to an acquired source, that is a signal that either an acquisition point is missing from the model, or the value is being treated as more fundamental than it actually is.

A discovered concept should not automatically become a stored concept. The ability to derive a value from existing data is often evidence that the value belongs to a view, projection, report, calculation, or contextual model rather than to the core model itself — `Speed` is exactly this kind of case: a legitimate, useful concept, but one that belongs downstream of the model rather than inside it.

### Modeling State Change as Events, Not Destructive Updates
**The model should preserve reality before it preserves projections.** A concern's actual history of state changes — the sequence of facts that actually occurred — is reality. A concern's current field values, snapshots, or read-optimized views are projections of that reality, convenient but replaceable. Modeling should establish the former before committing to the latter, in the same way [acquired data must be preserved even when a discovered value is more immediately useful](#acquired-data-vs-discovered-data).

Two related situations are commonly, and mistakenly, treated identically in modeling:

1. Data that is inherently time-series in nature — for example, a sequence of position readings from a moving sensor, where every reading is meaningful on its own and none of them "replaces" a previous one.
2. Data that is not inherently time-series, but which the system nonetheless changes over time — for example, a user's `Username`. When a value like this changes, treating the change as a destructive, in-place update that overwrites the previous value discards information: the previous value, and the fact that a change occurred at a specific point in time, are themselves architecturally significant facts that many requirements eventually need. ("Who held the username `omid` before the current holder, and when did the change happen?" is a completely ordinary requirement that a destructive-update model cannot answer after the fact.)

Memar treats both situations as instances of the same underlying modeling concern: a change to a concern's state is itself an event, and event design is not separable from modeling that concern's structure and behavior. A concern's lifecycle should be modeled with the expectation that its history of state changes may need to be queried, not only its current state.

To be explicit about what this principle does not claim: it does not mean Event Sourcing, CQRS, or append-only storage are mandatory. This is a modeling-level concern, not an implementation or storage-engine mandate. This document does not prescribe event sourcing, a specific storage engine, or a specific persistence strategy as a required implementation approach — those are implementation-phase decisions addressed elsewhere. What belongs to modeling is the recognition that overwriting state without preserving its history is a decision with real, often unintended, architectural consequences, and that decision should be made deliberately during modeling rather than defaulted into by whichever storage technology a team happens to reach for. In practice, storage engines that operate above a raw key-value layer typically build indexes over exactly this kind of event history to answer queries efficiently — but how indexing is achieved is an implementation concern; that the history exists to be indexed is a modeling concern.

### Constraints Belong to the Constraining Concern
When a requirement limits what may be done with some resources, the source of the limitation matters as much as the limit itself. A constraint that originates outside a resource — imposed by another concern, another participant, or another System — should be modeled as a relationship owned by the constraining concern, not as additional fields duplicated onto every resource it affects.

The constraining concern carries its own state: what it targets, how much of its demand has so far been realized against the resources it observes, and what remains. The constrained resources are places where the constraint may become effective; they are not owners of the constraint's bookkeeping. Duplicating constraint state onto each affected resource corrupts exactly the information the constraint exists to express: once the same limitation is recorded as independent copies spread across many resources, the aggregate effect of the single original constraint can no longer be read correctly from those copies, and adding, removing, or retargeting resources forces edits everywhere except in the constraining concern itself.

This principle has a consequence that frequently resolves otherwise confusing field-level questions: two quantities visible on the same resource are not necessarily one primary fact plus one cached copy of it. A resource-visible value may instead be the evaluation result of the external constraints and rules currently active against that resource. Before storing a value that looks derivable, the question is therefore not only "which stored fact produces this?" but "is this actually the evaluation result of concerns outside this node?" — because if it is, no amount of caching another local field will reproduce it correctly.

Such a constraining concern is often realized as an independently modeled Module attaching to the affected concept rather than growing that concept's fields or branches (see [Extensible Behavior Belongs to Pluggable Modules](#extensible-behavior-belongs-to-pluggable-modules)).

### Concept Discovery Must Not Be Driven by Presentation
Memar treats presentation structures as unreliable sources for discovering domain concepts.

User interfaces are designed around user experience, workflows, screen layouts, and interaction patterns. These concerns frequently change between products, platforms, and contexts, even when the underlying domain remains unchanged.

As a result, modeling should not begin by examining pages, forms, screens, widgets, or API endpoints and converting each visible element into a corresponding model.

For example, systems may expose concepts such as comments, social-media posts, news articles, blog articles, forum topics, or messages through completely different user experiences. However, a modeling effort may reveal that many of these are merely different presentations, aggregations, or contextual interpretations of a more fundamental concept such as `Content`.

The purpose of modeling is to discover stable domain boundaries, not to mirror presentation structures.

Presentation concerns may eventually require specialized widgets, pages, APIs, or aggregators, but these should emerge from the model rather than define it.

The critique of UI-driven modeling is shared by Eric Evans, who warns against "CRUD-driven" design where every screen becomes an entity. The specific argument that multiple presentation forms (comments, posts, articles, messages) may share a fundamental concept (`Content`) resonates with the "shared kernel" pattern in DDD, where multiple bounded contexts agree on a common model subset.

### Domain Decomposition over Aggregate-Root Modeling
A common misunderstanding is to start modeling by defining aggregators such as `User`, `Order`, `Project`, or similar high-level compositions and then placing other concerns inside them. Memar rejects this approach.

- **Aggregation is not a modeling primitive.**
- **Aggregation is a consequence of modeling.**

The purpose of modeling is first to discover concerns, responsibilities, lifecycles, and relationships. Only after those concerns have been understood may context-specific aggregators emerge. An aggregator is a context-specific assembly of independently discovered concerns — it does not introduce new responsibilities of its own; its sole purpose is to compose concerns that have already been modeled as separate abstractions. Because aggregation is shaped by use-case context rather than by domain structure, the same set of concerns may be aggregated differently in different contexts (e.g., a registration form vs. a profile-viewing page). Aggregators are therefore not modeling primitives; they are composition decisions that follow from the model. As a result, modeling should never begin by searching for a canonical aggregator. In many domains no single canonical aggregator exists at all. Different contexts may legitimately assemble the same concerns into different aggregations.

Memar rejects the conventional DDD pattern where a domain "owner" entity (e.g. `User`) directly contains and owns sub-concerns like `username`, `email`, or `password` as its own fields/methods. Instead, each such concern is modeled as its own independent abstraction, and any "User"-like concept is just one possible *aggregator* among several — aggregators are not fixed, singular, or domain-owned; they commonly form at the composition layer (GUI widgets/pages), though they are not limited to that layer.

The traditional aggregate-root pattern assumes a single, stable owning entity for a cluster of related data, but real systems frequently need different aggregations of the same underlying concerns depending on context. A canonical example: identity resolved via a local registration form needs a different aggregation shape than identity resolved via a third-party OAuth provider (e.g. Google login) — a single fixed `User` aggregator forces both flows into one shape that fits neither well, and tempts the owning entity to absorb logic (like credential validation) that does not actually belong to it.

`username`, `email`, and similar concerns are modeled as independent, self-contained abstractions with their own validation and behavior. A composition-layer construct (typically a GUI widget or page, though this is the common case, not the only one) assembles whichever subset of these independent abstractions a specific use case actually needs, and is responsible only for that assembly — not for absorbing the internal logic of the concerns it aggregates. Per [Module Identity and Responsibility](./modularity.md#module-identity-and-responsibility)'s decomposition signal — enforced syntactically for method bodies at the language layer, without redefinition here — if an aggregator's body starts doing more than its one named responsibility (e.g. a `RegisterComment` widget that also resolves "who is the current user"), that is the signal to split out a separate, dedicated widget (e.g. one that returns only an `ActiveUserID`), pushing that sub-concern's own validation and error-handling down into that separate widget rather than leaving it in the original caller.

A common misunderstanding is to interpret decomposition as merely extracting fields from a larger structure. For example, an `ActiveUserID` returned by a dedicated widget is not itself the concern being modeled. The actual concern is active-user resolution and selection: maintaining the currently active identity, enforcing any rules that govern identity switching, validating permissions, and exposing the selected identity to other parts of the system. The returned identifier is only an output of that concern, not the concern itself. This distinction is important because Memar decomposes systems around responsibilities and behavioral boundaries, not around individual pieces of data. A data value may appear in many places, but the responsibility that governs its creation, validation, and lifecycle should exist in exactly one place.

There is no language-level "aggregate root" or "entity" construct distinct from an ordinary abstraction realization. Any abstraction realization that happens to compose several other realizations is, structurally, just another realization — its role as an "aggregator" is a naming/architectural convention applied by the developer, not a special grammar feature.

An abstraction is not justified by the existence of data. An abstraction is justified by the existence of an independent Responsibility, behavioral boundary, or lifecycle — see [System → Responsibility](./system.md#system) for the general definition and [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) for what "independent" can actually be checked against, rather than asserted. Data decomposition is a consequence of responsibility decomposition, not the objective of modeling.

An aggregator should be named after the use case it serves (e.g. `RegisterComment`, `LocalLoginForm`, `OAuthCallbackHandler`), not after the domain concept it assembles (e.g. `User`). This convention reinforces that the aggregator is a composition-layer construct with a single named responsibility, not a domain-owned entity.

This is closely related to, but distinct from, established critiques of Anemic/God-object Aggregate Roots within the DDD community itself; it also resonates with component-composition patterns common in modern frontend frameworks, where a "page" or "widget" composes several independent, narrowly-scoped pieces of state rather than a single monolithic model object. The principle that aggregation should happen at the composition layer rather than within the domain model also has parallels in the ports-and-adapters (hexagonal) architecture, where the domain core defines capabilities and the application layer assembles them into use cases.

### One Authoritative Location per Concern's Data
A concern's authoritative data — the data whose truth the concern owns and enforces — has exactly one location: the memory in which it is held is part of how the concern's identity and lifecycle are realized, and a boundary realized twice is two boundaries. A copy of that data held elsewhere is a *derived copy*: never a second authority, and if it carries no defined re-derivation path, not even a copy — a second, diverging original.

The modeling failures this rule prevents are worked out in the framework's protocol documents, which own the retention concepts involved; at modeling time it is enough to hold the rule and to recognize its two recurring violations — one concern's data split across multiple locations, and a faster retention tier standing in front of the authoritative location as if it were infrastructure rather than what it is, a derived copy. Which products, technologies, or tiers realize the locations is an implementation-phase concern; naming any of them in a modeling principle would date the principle and invite readers to argue products instead of concepts.

As with several other implementation-adjacent questions that surface during modeling — retention properties, reclamation, connection lifetimes, time — the rule itself belongs to modeling while its working-out belongs to the framework: either Memar's own libraries and protocol documents carry the answer, or the organization developing the system reads those documents and builds its own library against them. Modeling records the question and the boundary; the protocol documents answer it.



### Extensible Behavior Belongs to Pluggable Modules
Not every requirement that touches a concept belongs inside that concept's own model. The full architectural treatment of this — what a pluggable Module is, why *pluggable* does not mean *dynamically loaded plugin*, and why the provisional term Rule names a Module's optional relationship to another Module rather than a conditional expression — now lives in [Modularity](./modularity.md#pluggable-behavior). This section keeps only the modeling-level consequence and the `Invoice` illustration this document has used since before that document existed.

A discount mechanism on an `Invoice` is a useful illustration: one organization wants a simple percentage discount; another wants a multi-tier discount that reduces an invoice by 10% the first time a customer uses it, 20% the second, and 30% the third; another wants a location-restricted discount that only applies at specific branches, or only to specific products. Memar's answer is not to keep extending `Invoice` itself to absorb every new variation. `Invoice` connects to any number of independently modeled, pluggable Modules through an ordinary reference edge, without needing to know, at the level of its own model, what kind of Module it is connected to — `Invoice` does no more than expose the point at which one may attach; it does not change shape to accommodate whatever a new one needs.

This document's modeling-level consequence is: a concern's model should expose attachment points for pluggable Modules rather than growing new fields or branches to absorb every variation one might need.

This mirrors the plugin/extension-point pattern common across many mature software systems, and the strategy pattern from object-oriented design generally; it is also simply a restatement, at the model level, of the open/closed principle. Outside software, it parallels how a legal system separates a stable constitutional core from more easily amended regulations and bylaws that plug into it without altering the core itself.

### Separating Structure (Code) from Policy (Rule)
Domains that look structurally identical across organizations often differ only in the *conditions* attached to them, not in the underlying graph shape. A trip's price depends on traffic level and time window, but the relationship — a purchase of a transport product — is structurally identical across all trips. A tax obligation depends on jurisdiction and self-declaration process, but the invoice relationship is structurally identical to any other commercial invoice. Becoming staff of an organization may require a prerequisite (e.g., an authenticated OTP token) in one organization but not another, without changing the underlying edge type.

Each domain is therefore modeled in two layers:

- **Code** answers *what kinds of things and connections can exist at all* — the fixed structural shape of a domain: node types, edge types, and their mandatory relationships.
- **Rule** answers *under what conditions a given instance of that structure is valid, required, or triggered* — the conditional, context-dependent policy logic that governs how a structural element behaves in a given situation.

The modeling-level requirement is that a Rule is not embedded as a hardcoded conditional inside application code, and not treated as an external, non-graph configuration: it is modeled as a first-class node in the graph, connected by an edge to the Code element (node type, edge type, or specific instance) it governs. This keeps the graph queryable as a single source of truth — "which entities are subject to Rule X" must be answerable by traversing the model, not by reading code. Executing a Rule (evaluating at runtime whether its condition is met) belongs to a separate rule-engine component that reads Rule nodes from the graph; the engine is the interpreter, not part of the structural model, and it is justified only after the responsibility is modeled (see [Event, Rule, and Mechanism-First Design](./modularity.md#event-rule-and-mechanism-first-design)).

The distinction parallels how legal systems separate **statute** (the general, stable law) from **executive bylaw/regulation** (the situational implementation, which can vary by locality and change without amending the statute itself).

The statute/bylaw distinction in legal systems; business rule engines (e.g., Drools) and policy-as-code systems (e.g., Open Policy Agent/Rego), which separate decision logic from application code but typically do not represent rules as first-class nodes in the same graph as the data they govern.
