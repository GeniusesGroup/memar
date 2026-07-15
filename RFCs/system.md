---
Title: "System"
Status: Proposed
Start Date: 2026-07-14
RFC Number: 495576
Applied to: []
Related RFCs:
    - Title: "Terminology"
      URI: "./terminology.md"
      Reason: "Depends_on"
      Explanation: "This RFC builds directly on the terminology philosophy, classification layers, and concept-first thinking established in the Terminology RFC. The definitions in this RFC must be consistent with the terminological principles set there."
    - Title: "Protocol"
      URI: "./protocol.md"
      Reason: "Reference"
      Explanation: "This RFC includes a brief pointer to Protocol's definition. The Protocol RFC is the authoritative source."
    - Title: "Modeling"
      URI: "./modeling.md"
      Reason: "Extends"
      Explanation: "This RFC defines Model and Abstraction at the conceptual level. The Modeling RFC builds on those definitions to specify how Memar performs modeling as an architectural activity."
    - Title: "Framework"
      URI: "./framework.md"
      Reason: "Depends_on"
      Explanation: ""
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Titles: ["Architect"]
        URI: ""
        Explanation: "Initiated the need for a foundational concepts RFC; provided the core definition of Technology as applied knowledge; articulated the inseparability of System and Architecture as concepts; supplied the lived-experience critique and the connection between technology and lifestyle; contributed the position that war, discourse, and governance are technologies."
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Tasks:
      - Titles: ["Initial draft"]
        URI: ""
        Explanation: "Proposed the initial RFC structure; drafted candidate definitions for System, Architecture, Technology, Protocol, and Abstraction; proposed the relationship structure between concepts; identified the problem statement regarding inconsistent usage across disciplines."
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "High"
    Tasks:
      - Titles: ["Initial draft"]
        URI: ""
        Explanation: "Synthesized contributor inputs with the Terminology RFC's principles and the RFC Template's structure into a single coherent document; expanded definitions with cross-disciplinary grounding; added Knowledge, Model, Framework, and Implementation sections; composed the Relationships Between Concepts section and Discussion."
---

# System

## Summary
This RFC establishes explicit, foundational definitions for the core concepts that all other Memar RFCs depend on: **System** and related word such as **Architecture**, **Technology**, **Knowledge**, **Model**, **Abstraction**, **Protocol**, **Framework**, and **Implementation**. These terms are widely used across disciplines, yet their meanings are often inconsistent, context-dependent, and sometimes contradictory. Within a single conversation, two participants may use the word "system" to refer to entirely different categories of entity, or the word "protocol" to mean anything from a network handshake to an entire organizational constitution. Misunderstandings at this level propagate upward and create ambiguity throughout the entire development process.

Memar therefore defines these foundational concepts explicitly and precisely before introducing higher-level architectural guidance. This RFC does not claim to invent new meanings for these words; rather, it selects, from the space of existing usage, definitions that are scientifically grounded, maximally general, and internally consistent with one another and with the Terminology RFC's principles. The goal is not to override other communities' usage, but to ensure that within the Memar ecosystem, every reader and contributor shares the same understanding of what these words mean.

This RFC is deliberately positioned before all other conceptual RFCs. The Terminology RFC establishes *why* precise terminology matters and *how* to evaluate it; this RFC establishes *what* the key terms actually mean. All subsequent RFCs that use these concepts — Modeling, Protocol, Capsule, Widget, and any future RFC — should depend on this RFC, not the reverse.

## Motivation
The immediate motivation for this RFC emerged from a concrete, observed problem: during the drafting of earlier Memar RFCs, the same term was repeatedly interpreted differently by different contributors, and sometimes differently by the same contributor at different points in the discussion. Specifically:

- **System** was assumed to be one kind of entity by one contributor and a different kind by another.
- **Architecture** was assumed to concern only high-level design decisions by some, and to span the entire development lifecycle by others.
- **Protocol** was assumed to be a communication contract by some, and a broader conceptual umbrella by others.
- **Technology** was assumed by many readers to mean tools, software, or physical devices — a narrow interpretation that excludes methods, processes, organizational practices, social mechanisms, and cognitive techniques, all of which are technologies by any complete definition.

Each of these misunderstandings, in isolation, is minor. In aggregate, they produce a conceptual foundation that is unstable: reasoning built on ambiguous terms produces ambiguous results, and the ambiguity compounds as higher-level concepts are defined in terms of lower-level ones.

The deeper motivation is structural. Memar's Terminology RFC establishes that terminology shapes mental models, and that mental models shape architecture. If the most fundamental terms in the ecosystem — System, Architecture, Technology — are left undefined, every RFC that uses them implicitly imports whatever interpretation each reader happens to carry. This is the same mechanism the Terminology RFC describes under "conceptual leakage": a general concept (System) becomes understood only through its most familiar exemplar (a software system), and the broader meaning is lost. The result is that architectural reasoning becomes unconsciously constrained by whatever subset of each concept's meaning is most locally familiar, rather than by the concept's full scope.

A foundational RFC that defines these terms explicitly is therefore not a philosophical luxury. It is a structural prerequisite for the coherence of every RFC that follows.


## Guide-level Explanation

### Why This RFC Exists
Every Memar RFC that discusses how to build, model, or reason about software systems uses words like "system," "architecture," and "technology." These words are so common that their meaning feels obvious — until two contributors discover they have been using the same word to mean different things. This RFC prevents that discovery from happening late and expensively, by establishing clear, agreed-upon definitions at the earliest possible point.

The definitions in this RFC are not arbitrary. They are selected to satisfy three constraints simultaneously:

1. **Scientific grounding.** Each definition is grounded in established academic or philosophical traditions where such traditions exist, and is stated with enough precision to survive criticism. This is consistent with the Terminology RFC's preference for Scientific-layer terminology as the foundation for architectural reasoning.

2. **Maximal generality.** Each definition is broad enough to encompass the full range of entities the term is used to describe across disciplines — physical systems, conceptual systems, social systems, computational systems, and organizational systems — without becoming so vague that it ceases to be useful.

3. **Internal consistency.** The definitions are mutually consistent: System is defined independently of its implementation, and Architecture is defined in terms of System; Technology is defined as applied knowledge directed at systems, not as artifacts; and the relationships between all concepts form a coherent graph rather than a collection of independent assertions.

### How to Read This RFC
The Guide-level explanation you are reading now provides a high-level overview of what each concept means and why it matters. The Reference-level explanation that follows provides the full, authoritative definitions, organized by concept, with drawbacks, rationale, and open questions for each.

A contributor who has read the Guide-level explanation should have a working understanding of every concept. A contributor who needs to evaluate edge cases, resolve ambiguities, or understand why a definition was chosen over alternatives should consult the Reference-level explanation.


### Concepts at a Glance
Before the detailed definitions, a brief orientation to how the key concepts relate:

- A **System** is what is being built or studied — a collection of interacting elements organized toward a purpose.
- **Architecture** is the collection of processes involved in the design and development of a system — one of several co-equal lenses through which a system is understood and evolved.
- **Technology** is the knowledge applied to create, modify, or evolve systems — not the artifacts themselves, but the know-how behind them.
- **Knowledge** and **Science** are the broader epistemic foundations from which technology is derived.
- A **Model** is a simplified representation of a system or aspect of reality, used to reason about it.
- An **Abstraction** is the mechanism by which models reduce complexity — preserving what matters and discarding what does not, relative to a specific purpose.
- A **Protocol** (defined in detail in its own RFC) is a structured body of knowledge that enables participants within a system to interact, coordinate, and evolve consistently.
- A **Framework** is a structured set of constraints, conventions, and reusable components that provides a foundation for building systems within a defined domain. A framework does not describe a particular system — it defines a design space within which multiple architectures may be created. See the [Framework RFC](./framework.md) for Memar's specific application of this concept.
- An **Implementation** is a concrete realization of a system's design, expressed in specific technologies, languages, and tools.

These concepts are not independent. They form a web of relationships — directional influences, mutual dependencies, and co-equal pairings — rather than a linear chain or hierarchy. Science produces knowledge; knowledge is applied as technology; technology enables system development; and systems are shaped by both framework and architecture as co-equal aspects. But these directional influences are only one dimension of the picture: modeling, abstraction, and process operate across the entire structure, and every concept influences others in ways that cannot be captured by a single ordering. Each concept exists in relation to the others, and understanding any one of them precisely requires understanding its relationships to the rest.


## Reference-level Explanation

### System
A **system** is a collection of interacting elements organized to achieve one or more purposes.

The elements of a system may be physical, conceptual, organizational, social, cognitive, or computational. A system is not defined by what it is made of, but by the existence of relationships between its elements that produce coherent behavior.

A family, a government, a software application, a legal process, a scientific theory, a transportation network, a market, a language, a biological organism, and an organizational culture may all be considered systems. The defining characteristic is not the material substrate but the relational structure: elements that interact in ways that produce behavior the individual elements alone would not produce.

This definition is deliberately general. It is drawn from and consistent with the systems theory tradition (von Bertalanffy, 1968; Boulding, 1956; Checkland, 1981), which treats systemhood as a property of relational organization rather than of material composition. A system, in this view, is identified by asking not "what is it?" but "what does it do, and how do its parts interact to do it?"

#### Key Properties
**Purpose.** A system exists toward one or more purposes. A purpose is not necessarily an intentional goal held by a conscious designer; it may be an emergent property of the system's organization. A biological ecosystem is a system whose "purpose," in this sense, is the maintenance of its own stability and the cycling of its constituent processes, even though no agent designed it toward that end. The term "purpose" is therefore used here in a functional sense — a system's purpose is what the system's organization causes it to achieve or tend toward — rather than in a strictly teleological sense.

**Boundary.** A system has a boundary that distinguishes its internal elements from its external environment. The boundary is not necessarily a physical barrier; it is the point at which the criteria for system membership change. In a software system, the boundary may be defined by a deployment unit, a module, or an API surface. In an organizational system, the boundary may be defined by membership, role, or contractual relationship. The boundary is an analytical choice made by the observer, not an inherent property of the system's material — the same collection of elements may be analyzed as one system or as multiple overlapping systems depending on where the observer places the boundary.

**Emergence.** A system exhibits behavior that emerges from the interaction of its elements but is not reducible to the properties of any individual element. This is a core insight of systems theory and is what distinguishes a system from a mere collection. A pile of sand is a collection; a sand dune — which has shape, stability properties, and responses to wind that no individual grain possesses — is a system.

**Interdependence.** The elements of a system are interdependent: a change in one element may propagate to others through the relationships that connect them. This interdependence is what makes systems both powerful (coordinated behavior) and fragile (cascading failure).

#### What a System Is Not
A system is not its implementation. The same system — understood as a collection of interacting elements organized toward a purpose — may be implemented in radically different ways. A government may be implemented as a democracy, a monarchy, or a technocracy without ceasing to be a system for governing. A financial system may be implemented with physical currency, digital ledgers, or barter without ceasing to be a system for facilitating exchange. Confusing a system with its implementation is a specific instance of the concept-vs-representation confusion that the Terminology RFC identifies as a primary source of architectural error.

A system is not a product. A product is one possible implementation of one possible system. The product "Microsoft Excel" is not the system "spreadsheet-based computation and data organization." The former is an artifact; the latter is a functional abstraction that could be realized by any number of products, past, present, or future.

A system is not a technology. A technology is knowledge applied to develop systems. The system is the entity that results from, or is modified by, the application of that knowledge. Confusing these two categories leads to reasoning of the form "we need a new system" when what is actually needed is new knowledge about how to modify the existing system — a distinction that matters because the solution path is different in each case.

#### Discussion

##### Drawbacks
The generality of this definition means it applies to almost anything that can be described as having parts that interact. Some contributors may find this so broad as to be unhelpful: if everything is a system, does the term carry any useful discriminative power? The answer is that the term's usefulness comes not from narrowing the set of things it applies to, but from providing a common analytical lens — relationships, boundaries, emergence, purpose — through which very different entities can be compared, reasoned about, and designed. A definition that excluded, say, social systems would force Memar to treat software architecture and organizational architecture as fundamentally different activities, when in practice they share deep structural similarities that the general definition makes visible.

##### Rationale and Alternatives
- **Restrict "system" to computational or software entities (rejected).** This would be consistent with much industry usage but would sever the conceptual connection between software architecture and other forms of system design (organizational, infrastructure, process) that Memar explicitly recognizes as architecturally relevant. It would also contradict the Terminology RFC's principle that concepts should outlive technologies.

- **Restrict "system" to entities with clearly defined boundaries (rejected).** Many real-world systems (ecosystems, markets, organizational cultures) have fuzzy, contested, or observer-dependent boundaries. Excluding them would impoverish Memar's conceptual vocabulary for describing the environments in which software systems operate.

- **Adopt a purely mathematical definition from dynamical systems theory (rejected).** While mathematically precise, this would exclude many systems that are architecturally relevant but do not have easily formalizable state spaces — organizational systems, governance systems, and social mechanisms being primary examples.

##### Prior Art
The definition is consistent with general systems theory as articulated by von Bertalanffy ("General System Theory," 1968), Boulding ("The World as a Total System," 1985), and Checkland ("Systems Thinking, Systems Practice," 1981). It is also consistent with the IEEE standard definition of a system as "a collection of components organized to accomplish a specific function or set of functions" (IEEE Std 610.12), though the definition in this RFC is broader in that it does not restrict the function to be specified in advance and does not require the components to be physical.

##### Unresolved Questions
1. Should Memar eventually adopt a more formal treatment of system boundaries, perhaps drawing on the distinction between open and closed systems from thermodynamics and information theory?
2. How should this RFC's definition of "purpose" interact with systems that have conflicting or internally contested purposes — for example, a political system in which different actors have genuinely incompatible goals?

### Structure
**Structure** is the set of capabilities and limitations (constraints) a System exposes and enforces.

Capabilities are what the System *can* do — the operations, transitions, and interactions available to those who interact with it. Constraints are what the System *cannot* do, or the conditions under which a capability is available, valid, or forbidden.

#### Structure Is Not Arrangement
Structure does not merely describe the arrangement of parts — the component hierarchy, module layout, or dependency graph. In common engineering usage, "structure" often carries this connotation: a static blueprint of how pieces are organized. Memar uses the word in a fundamentally different sense. Structure here is closer to **operational shape**: what a System can and cannot do. A system's component layout is one *projection* of its structure, but it is not the structure itself. Confusing the projection with the thing projected leads to the same class of error the Terminology RFC identifies under concept-vs-representation confusion: treating the map (layout) as the territory (operational shape).

#### The Inseparability of Capability and Constraint
Capabilities and constraints are not independent properties that happen to coexist in a structure. They are two aspects of the same thing — inseparable, like two sides of a coin. Every capability implies limitations. Every limitation enables capabilities.

Consider a system that enforces **no shared mutable state**. This is a constraint: it forbids a certain kind of interaction. But that same constraint enables **thread safety** — a capability that would not exist without the limitation. Or consider a residential building designed with a **central kitchen** instead of private kitchens. This is a constraint: it removes the freedom to cook privately. But it simultaneously enables **economy of scale, quality control, and operational efficiency** — capabilities that would be impossible or prohibitively expensive in a building with 100 private kitchens.

This inseparability has a practical consequence for how structures are reasoned about: a proposed structural change cannot be evaluated by looking only at the capabilities it adds or only at the constraints it removes. Every addition of capability also adds constraint, and every removal of constraint also removes capability. Sound architectural reasoning accounts for both sides of every structural decision.

#### Structure, Behavior, and Implementation
Structure cannot be defined independently of behavior: describing what a System does inherently requires knowing what it is permitted to do and what it is restricted from doing. A definition of Structure that omits behavior collapses into a description of static shape — fields, storage layout — which Memar treats as a symptom of premature implementation-oriented thinking, not as Structure itself.

### Process
A **process** is an organized sequence of activities or interactions that occurs *within* a system, involving one or more of the system's elements and contributing to the system's behavior or purposes.

A process is not an independent entity that exists in isolation. It acquires its meaning from the system within which it occurs: the same sequence of activities may be a well-defined process in one system and an irrelevant description in another, depending on whether the system's elements, boundaries, and purposes give the sequence coherent meaning. A sequence of chemical reactions is a process within a metabolic system; the same reactions, described outside any biological context, are merely a list of events.

Processes may be nested: a process may contain sub-processes, and a sub-process may itself contain further sub-processes, to any depth. A surgical operation (a process within a healthcare system) contains the anesthesia-induction process, the incision process, the tissue-repair process, and the recovery-monitoring process — each of which contains its own sub-processes. A software request-handling pipeline (a process within a web application) contains authentication, authorization, validation, business logic, and response-serialization processes. Nesting is not limited to a fixed depth; the appropriate level of analysis depends on the decision being made.

Processes may be concurrent, sequential, overlapping, or iterative. They may involve all of a system's elements or only a subset. They may be governed by protocols or unstructured. What makes a sequence of activities a process within a system, rather than a random series of events, is that the activities are organized — they follow a discernible pattern, serve a discernible function within the system, and produce behavior that is meaningfully related to the system's purposes.

#### Process and System
The relationship between process and system is one of containment and co-definition, analogous to the relationship between architecture and system discussed above:

- A **system without processes** is not a system in the systems-theory sense. A collection of elements with no organized interactions is a heap, not a system. The interactions — which are processes — are what make the collection a system.
- A **process without a system** has no defined scope, no boundary, and no purpose. The sequence of activities may occur, but it cannot be evaluated, reasoned about, or designed, because there is no system to provide the context that gives the process its meaning.
- A **system is defined by its processes** as much as by its elements. Two systems with identical elements but different processes are different systems, because they exhibit different behavior.

This inseparability is why Process is defined in this RFC rather than in a standalone document: any attempt to define Process without reference to System either silently assumes System's meaning or produces a definition that floats free of the context that gives it coherence.

#### Discussion

##### Drawbacks
Defining Process in this RFC increases the scope of an already broad document. The alternative — a dedicated Process RFC — was considered but rejected for the same reason that Architecture is defined here rather than separately: the definition is not meaningfully separable from System.

##### Rationale and Alternatives
- **Define Process as a standalone RFC (rejected).** Process cannot be defined without reference to System. A standalone Process RFC would either duplicate System's definition or silently depend on it, creating the same circular dependency problem this RFC exists to prevent.
- **Define Process as a sub-concept under Protocol (rejected).** Protocol governs processes, but Process is not a sub-concept of Protocol. Processes exist whether or not they are governed by protocols; many processes in natural, social, and organizational systems operate without any formal protocol governing them. Process is a foundational concept that Protocol depends on, not the reverse.

##### Prior Art
The concept of process within systems is central to systems theory and process philosophy (Whitehead, "Process and Reality," 1929). In software engineering, process thinking is foundational to workflow engines, process algebra (e.g., CSP, π-calculus), and business process management (BPM). The nesting property is well-established in process hierarchy theory.

##### Unresolved Questions
1. Should Memar eventually develop a more formal treatment of process composition — how processes combine, constrain, or interfere with one another?
2. How should the relationship between Process and State be characterized? A process transforms state, but state is not yet formally defined in Memar.

### Architecture
**Architecture** is the collection of processes involved in the design and development of a system.

Architecture is not limited to high-level decisions made early in a development process. It spans the entire lifecycle of system development, from the initial identification of what system is needed, through the selection and application of technologies, to the ongoing processes by which the system is maintained, measured, and evolved. What makes an activity architectural is not when it occurs or where it sits in a process, but the nature and impact of the decisions it involves — specifically, decisions that shape the system's structure, behavior, or long-term properties.

This definition is deliberately broader than the definition most commonly encountered in the software industry, where "architecture" is often restricted to high-level structural decisions (component decomposition, deployment topology, technology selection) made during an early design phase. The restriction is understandable as a practical shorthand, but it is misleading as a definition, because it implies that decisions made later in the lifecycle — about error handling patterns, data migration strategies, operational runbooks, or team communication structures — are not architectural, when in fact they often have profound effects on the system's behavior, evolvability, and longevity.

#### What Architecture Is Not
Architecture is not a phase. It is not something that happens before implementation and then stops. The architectural consequences of a decision are determined by the decision's impact on the system, not by when the decision was made. A decision about how to handle concurrent writes to a database, made during implementation, is architectural if it affects the system's consistency guarantees, performance characteristics, or failure modes — which it almost certainly does. Treating architecture as a phase encourages the false belief that architectural thinking can be "completed" before implementation begins.

Architecture is not a document. An architecture document describes architectural decisions; it is not the decisions themselves. Confusing the description with the thing described leads to a situation where the document is maintained but the actual system has drifted away from it — a common and well-documented problem in large-scale software development.

Architecture is not the structure of a system. The structure of a system is one output of architectural processes. But those processes extend beyond producing structure: they involve the reasoning by which constraints were evaluated and some accepted while others were rejected, the decisions about what to model and at what level of abstraction, and the principles that will guide future evolution. Structure without this processual context is a snapshot that cannot be reasoned about or adapted; it can only be copied or replaced.

#### The Relationship Between Architecture and System
Architecture does not exist independently of the system it addresses. There is no such thing as "architecture in general" — only architecture *of* a particular system, *for* a particular purpose, *under* a particular set of constraints. This is why System is defined before Architecture in this RFC, and why the two concepts could not meaningfully be separated into independent RFCs: every statement about architecture is implicitly a statement about the system being architected, and every statement about how to understand a system is implicitly an architectural statement about what aspects of the system matter.

This does not mean that architectural knowledge is not transferable between systems. Patterns, principles, and heuristics learned from one system may apply to another. But the applicability must be evaluated each time, because the system's purpose, constraints, and context determine which architectural decisions are appropriate, and these differ from system to system.

#### Discussion

##### Drawbacks
The breadth of this definition means that nearly any decision about a system could be classified as architectural, which risks the term becoming vacuous. Memar mitigates this by not treating "architectural" as a binary label but as a spectrum: a decision's architectural significance is proportional to its impact on the system's behavior, evolvability, or properties. Low-impact decisions — such as the choice of a local variable name — are architectural in the trivial sense that they are part of system development, but they carry negligible architectural weight. High-impact decisions — such as the choice of consistency model, communication pattern, or module boundary — carry substantial architectural weight and deserve proportionally more deliberation, documentation, and review.

##### Rationale and Alternatives
- **Restrict architecture to "high-level design" (rejected).** This is the most common industry definition, but it creates a false distinction between "architectural" decisions and "implementation" decisions that does not hold under scrutiny. Many decisions made during implementation have architectural consequences, and excluding them from the architectural domain means those consequences go unexamined.

- **Define architecture as "the structure of a system" (rejected).** This confuses a system's structure with the process and decisions that produced it. A system's structure is a snapshot; architecture is the reasoning, constraints, and trade-offs that the snapshot embodies.

- **Define architecture as "the decisions that are expensive to change" (rejected).** While pragmatically useful as a heuristic, this is a consequence-based definition that can only be applied retrospectively. A decision is not known to be expensive to change until after it has been made and the attempt to change it has been evaluated. Architecture, as a discipline, needs a definition that can be applied prospectively — before the consequences of a decision are known.

##### Prior Art
ISO/IEC 42010:2022 defines architecture as "the fundamental concepts or properties of a system in its environment embodied in its elements, relationships, and in the principles of its design and evolution." This RFC's definition is consistent with that standard but emphasizes the process dimension more explicitly: architecture is not only what the system is, but how it came to be that way and how it will continue to change.

##### Unresolved Questions
1. Should Memar develop a more formal framework for assessing the architectural weight of a decision, or is the proportional-impact heuristic sufficient?
2. How should architectural decisions made by different contributors at different times be reconciled when they conflict?


### Technology
**Technology** is the knowledge used to create, modify, operate, or evolve systems in pursuit of specific goals.

Technology is not limited to tools, machines, or software. Methods, processes, skills, organizational practices, social mechanisms, communication techniques, governance structures, and cognitive strategies may all be technologies. A technology may be physical, conceptual, organizational, or cognitive.

Technology should therefore be understood as applied knowledge rather than as a collection of artifacts. The artifact — the phone, the database, the building — is a product of technology, not technology itself. The technology is the knowledge that made the artifact possible: the understanding of materials, the engineering methods, the design processes, the organizational coordination, and the accumulated practical experience that together enable the artifact's creation and operation.

This definition is consistent with the Technology Terms layer in the Terminology RFC, which defines technology as "the application of knowledge — techniques, skills, methods, and processes — to develop systems, whether those systems are tools, artifacts, or bodies of engineering knowledge, in order to achieve a specific goal." It extends that definition by making explicit that the systems technology develops are not limited to physical or computational artifacts. A legal system, a governance process, a method of scientific peer review, a classroom pedagogy, and a cultural norm of polite disagreement are all systems, and the knowledge used to create, maintain, or evolve them is technology.

#### The Scope of Technology

The breadth of this definition may initially appear to stretch the word "technology" beyond its everyday usage, where it typically connotes devices, software, or industrial processes. However, the broader usage is well-established in the philosophy of technology and in the academic study of technological systems. Ellul ("The Technological Society," 1964) treats technology as "the totality of methods rationally arrived at and having absolute efficiency in every field of human activity." Mumford ("Technics and Civilization," 1934) distinguishes between "technics" (the body of techniques and methods) and the specific artifacts those techniques produce. Both perspectives treat technology as fundamentally about *how* things are done — the knowledge, methods, and processes — rather than about the specific things that result.

Within Memar, this broader view has practical consequences. It means that:

- A **lifestyle** is a technology: it is a body of knowledge, habits, and practices organized to achieve certain goals (quality of life, social integration, personal fulfillment). When a governance system attempts to change citizens' lifestyle through legislation, it is attempting to modify a technology — and it should apply the same rigor to understanding that technology's structure, dependencies, and failure modes that it would apply to any other system-modification effort. Changing one aspect of a lifestyle (e.g., pet ownership) without understanding its relationships to other aspects (family structure, privacy, social well-being) is analogous to changing one component in a software system without understanding its dependencies — a recipe for unintended consequences.

- **War** is a technology: it is a body of knowledge, methods, and organized processes directed at achieving specific goals through coercive means. Understanding war as technology, rather than as a natural disaster or an inevitable force, highlights that it is produced by knowledge and can, in principle, be addressed by better knowledge — by understanding the systems that produce it and the architectures that sustain it, rather than by developing more powerful artifacts within it.

- **Discourse** and **governance** are technologies: they are structured bodies of knowledge about how people coordinate, communicate, and make collective decisions. The quality of these technologies directly affects the quality of the systems they govern. A governance system that does not learn from its own outcomes — that relies on lived experience rather than on systematic analysis — is analogous to a software system that does not monitor its own failure modes: it will accumulate technical debt, produce unreliable outcomes, and eventually fail in ways that were both predictable and preventable.

#### Technology vs. Artifact
The distinction between technology and artifact is one of the most consequential conceptual distinctions in this RFC, because confusing the two leads directly to Tool-First Thinking — the anti-pattern identified in the Terminology RFC where reasoning begins from a familiar tool rather than from the underlying problem.

When technology is understood as artifacts, the reasoning chain becomes:

```
Artifact → What it does → Problem it solves
```

When technology is understood as knowledge, the reasoning chain becomes:

```
Problem → What kind of system would address it → What knowledge is needed → Which artifacts embody that knowledge
```

The second chain is the Concept-First sequence that the Terminology RFC advocates. The first chain produces architectures that are shaped by the capabilities and limitations of whatever artifacts the reasoner happens to be familiar with, rather than by the actual structure of the problem.

#### Discussion

##### Drawbacks
The breadth of this definition means that "technology" becomes nearly synonymous with "applied knowledge," which may seem to drain the word of specific meaning. Memar accepts this trade-off deliberately. The alternative — restricting "technology" to physical or computational artifacts — creates a conceptual blind spot: it makes it impossible to reason precisely about the technological character of governance, discourse, lifestyle, and other non-artifact systems, even though these systems are developed, maintained, and evolved through the same kind of applied knowledge that produces physical artifacts. The cost of missing this connection is higher than the cost of using a broad definition.

##### Rationale and Alternatives
- **Restrict technology to physical artifacts and software (rejected).** This is the most common usage but excludes methods, processes, organizational practices, and social mechanisms that are clearly developed through applied knowledge and directed at specific goals — the defining features of technology.

- **Define technology as "tools and their application" (rejected).** This conflates the tool (artifact) with the knowledge that produced it, perpetuating the Tool-First Thinking pattern the Terminology RFC identifies as a primary source of architectural error.

- **Define technology as "the application of science" (rejected).** While historically suggestive, this implies that technology requires prior scientific understanding, which is not always the case. Many technologies predate the scientific understanding of why they work. Craft knowledge, trial-and-error engineering, and empirical refinement can produce effective technologies without a fully developed scientific theory.

##### Prior Art
The definition is consistent with the philosophy of technology as articulated by Ellul, Mumford, Heidegger ("The Question Concerning Technology," 1954), and the UNESCO definition of technology as "the know-how and creative process that may assist people to exploit tools, resources and systems to solve problems and to enhance their control over the natural and made environment in an endeavor to improve the human condition." It is also consistent with the Terminology RFC's definition of Technology Terms.

##### Unresolved Questions
1. Should Memar develop a more granular taxonomy of technology types (physical, conceptual, organizational, cognitive) with specific guidance for each?
2. How should the relationship between technology and power be addressed, if at all, within a software architecture framework?


### Knowledge and Science
**Knowledge** is a justified, structured understanding of a domain, acquired through observation, reasoning, experimentation, or critical discourse, that enables reliable prediction, explanation, or action within that domain.

**Science** is the methodology — the set of practices, norms, and institutions — by which knowledge is produced, tested, revised, and accumulated. Science is not a body of facts; it is a process. The body of facts is the current, provisional output of that process.

Within Memar, the relationship between science, knowledge, and technology follows a directional influence:

Science produces knowledge. Knowledge, when applied toward specific goals, becomes technology. Technology is applied through system development, where systems are shaped by both framework (which defines the design space) and architecture (which defines the concrete realization). This directional influence is what the Terminology RFC's Concept-First Thinking establishes, and it is the reason that Memar prefers scientific terminology as the foundation for architectural reasoning: the closer a term is to the scientific end of this influence chain, the more likely it is to have been subjected to explicit definition, falsifiability, criticism, and revision — the mechanisms that produce reliable knowledge. But this is one directional influence among many; it does not imply a simple linear chain from science to implementation, as the Relationships Between Concepts section makes clear.

#### The Role of Science in Memar
Memar does not claim that science is always correct. It claims that science is currently the strongest known methodology for constructing reliable knowledge — a pragmatic claim, not an ideological one, as the Terminology RFC states. Scientific knowledge evolves. Models are replaced. Theories are revised. What distinguishes science from other knowledge-production methods is not that it is immune to error, but that it has built-in mechanisms for detecting and correcting error: reproducibility, peer review, falsifiability, and cumulative revision.

For Memar, this has a concrete implication: when a concept has a well-established scientific treatment, that treatment should be the starting point for reasoning, not a technology's interpretation of it. A graph should be understood through graph theory before it is understood through a graph database. A constraint should be understood through constraint satisfaction theory before it is understood through a specific solver. Heat transfer should be understood through thermodynamics before it is understood through a product called an "air conditioner."

#### Discussion

##### Drawbacks

Basing architectural reasoning on scientific foundations increases the learning burden on contributors. Not every contributor needs to become a domain scientist, but every contributor needs enough scientific literacy to distinguish a concept from its implementation and to evaluate whether a technology's claims about a concept are grounded in the underlying science or are marketing-level simplifications. This is a non-trivial investment, and Memar acknowledges it as a real cost.

##### Rationale and Alternatives
- **Base architectural reasoning on practical experience alone (rejected).** Practical experience is valuable but is subject to cognitive biases, survivorship bias, and the difficulty of distinguishing correlation from causation in complex systems. Science provides mechanisms for correcting these biases that practical experience alone does not.

- **Treat all knowledge sources as equally valid (rejected).** This would eliminate the ability to evaluate the quality of evidence behind a claim. The Terminology RFC's distinction between Scientific, Technology, and Business terminology exists precisely because different knowledge sources have different validation mechanisms and different levels of reliability.

##### Prior Art
The relationship between science, knowledge, and technology is explored extensively in the philosophy of science (Popper, "The Logic of Scientific Discovery," 1959; Kuhn, "The Structure of Scientific Revolutions," 1962; Lakatos, "The Methodology of Scientific Research Programmes," 1978) and the philosophy of technology (as cited above in the Technology section).

##### Unresolved Questions
1. How should Memar handle concepts that have scientific treatments in multiple disciplines, where the treatments conflict?
2. At what level of scientific rigor should Memar's own terminology be held, given that it is a software framework and not an academic publication?


### Model
Every model is a model *of* a system — or of an aspect of reality relevant to a system. The relationship between model and system is therefore one of representation: a model provides a simplified, purpose-driven view of a system's structure, behavior, or properties that enables reasoning, communication, and transformation at a level of detail appropriate to the decision being made.

Modeling is the activity by which such representations are constructed, validated, and evolved. Within Memar, modeling is not a preliminary sketch that is discarded once implementation begins — it is a continuous architectural activity that accompanies every stage of system development. The model remains the source of truth; implementations are projections of that truth into specific technological contexts.

Model, Abstraction, and the full treatment of Modeling as an architectural discipline are defined in the [Modeling RFC](./modeling.md).


### Abstraction
An **abstraction** is a simplified representation of a selected aspect of reality that preserves information relevant to a particular purpose while deliberately omitting information that is not.

Abstraction is the primary mechanism by which complexity is managed in system design. Without abstraction, every system design decision would need to account for the full complexity of the underlying reality — every electronic circuit would need to account for quantum electrodynamics, every software module would need to account for processor microarchitecture, every organizational design would need to account for individual psychology. Abstraction allows reasoning to proceed at the level of detail that is appropriate to the decision being made.

Abstractions are not inherent properties of reality. They are constructs created by observers for specific purposes. A useful abstraction for one purpose may be useless or misleading for another. The abstraction "temperature" is useful for designing a heating system but useless for designing a chemical reaction — the latter requires knowledge of molecular kinetic energy, which temperature abstracts away. The same principle applies in software: the abstraction "user" is useful for designing an authentication system but may be misleading for designing a recommendation engine, where the relevant entity is closer to "a sequence of observed preferences over time" than to "a person with an identity."

#### Abstraction and Leaky Boundaries
Abstractions inevitably leak. The information they omit does not cease to exist; it continues to affect the system's behavior in ways that the abstraction does not represent. A database abstraction that hides concurrency semantics will leak when two transactions conflict. A network abstraction that hides latency and failure will leak when the network partitions. An organizational abstraction that hides team communication patterns will leak when coordination failures occur.

Recognizing that abstractions leak — and designing with that leakage in mind rather than pretending it does not exist — is a hallmark of mature engineering. Within Memar, abstractions should be chosen not only for what they hide but for how predictably they leak. An abstraction that leaks in well-understood, well-documented ways is preferable to one that appears clean but fails catastrophically when the hidden complexity becomes relevant.

#### Discussion

##### Drawbacks
Teaching abstraction as a first-class concern adds conceptual overhead to the learning process. Contributors must learn not only how to use abstractions but how to evaluate their boundaries, their leakage patterns, and their suitability for specific purposes. This is a real cost, particularly for newcomers who are accustomed to treating abstractions as opaque, leak-proof boundaries provided by a framework or language runtime.

##### Rationale and Alternatives
- **Treat abstraction as an implementation detail (rejected).** This is the default in many software frameworks, where abstractions are provided by the framework and treated as opaque by the user. This works until the abstraction leaks, at which point the user is unable to reason about the failure because they were never expected to understand what the abstraction hides. Memar considers this unacceptable for a framework whose stated goal is to improve reasoning quality.

##### Prior Art
The theory of abstraction in computer science is developed in detail in the literature on abstract data types, information hiding (Parnas, "On the Criteria to Be Used in Decomposing Systems into Modules," 1972), and abstraction barriers. The philosophical treatment of abstraction as a cognitive process is developed in the cognitive science literature (e.g., Hofstadter, "Gödel, Escher, Bach," 1979).

##### Unresolved Questions
1. Should Memar provide explicit mechanisms for documenting abstraction leakage, or should this be left to informal documentation?
2. How should the choice of abstraction level be guided in Memar's modeling process?


### Protocol
Protocols exist *within* systems. A protocol governs one or more processes within a system, and the system provides the boundary that gives the protocol its scope. This relationship is foundational rather than incidental: a system without protocols governing its internal processes is not a system in the systems-theory sense — it is merely a collection of independent elements with no defined interactions. Protocol, Process, and System co-arise; you cannot meaningfully discuss one without the others.

Protocol's full definition, ontology, and relationship to Process are defined in the [Protocol RFC](./protocol.md).

### Framework
A **framework** is a structured set of constraints, conventions, and reusable components that provides a foundation for building systems within a defined problem domain.

A framework does not describe a particular system. It defines a design space within which multiple architectures may be created. It provides structure without specifying content, conventions without prescribing decisions, and components without completing the design. The system that results from using a framework is not the framework; it is a system that was built within the framework's constraints.

Framework and Architecture are co-equal aspects of a System — neither is "above" or "below" the other. They answer different questions: Framework defines *what kinds of solutions are allowed*; Architecture defines *which solution was chosen*. The full treatment of this relationship, including the distinction between domain-level constraints (framework) and system-level constraints (architecture), is provided in the [Framework RFC](./framework.md).


### Implementation
An **implementation** is a concrete realization of a system's design, expressed in specific technologies, languages, and tools.

An implementation is the point at which abstract architectural decisions become executable artifacts: source code, configuration files, infrastructure definitions, deployment scripts, and the other artifacts that, taken together, constitute a runnable or operable system.

The Terminology RFC's Concept-First Thinking principle requires that concepts be understood before technologies are selected, and that technologies be selected before implementations are written. When this sequence is reversed — when an implementation is written first and the concepts are reverse-engineered from it — the resulting architecture is shaped by the implementation's incidental characteristics rather than by the system's actual requirements. This does not mean that implementation is derivative in a hierarchical sense; in the graph of conceptual relationships, implementation feeds back into modeling, architecture, and even technology through the experience gained from building and operating concrete systems. The directional influence from concepts to implementation is a matter of epistemic priority, not a linear pipeline.

#### Implementation Is Not Architecture
A common source of confusion in software development is the belief that architecture becomes visible only in implementation — that the architecture "is" the code. This is a conflation of two genuinely different things: the design decisions that shape the system (architecture) and the concrete artifacts that express those decisions (implementation). The same architectural decisions can produce different implementations in different languages, on different platforms, or under different constraints. The architecture is what remains constant across these variations; the implementation is what changes.

This distinction matters because it determines what can be changed without architectural review and what cannot. Changing a variable name, refactoring a function, or optimizing a query are implementation changes: they affect how the system is expressed but not what the system does or how it is organized. Changing a module boundary, a communication pattern, or a data model is an architectural change: it affects the system's structure, behavior, or properties in ways that ripple across the implementation. Being able to distinguish between these two kinds of change — and being able to explain why a particular change belongs in one category rather than the other — is a core architectural competency.

#### Discussion

##### Drawbacks
Emphasizing the distinction between architecture and implementation can create a perceived separation between "architects" and "developers" that may not be healthy for a project. Memar does not endorse this separation. Every contributor who makes decisions that affect the system's structure or behavior is, to that extent, engaging in architectural activity, regardless of their title. The distinction between architecture and implementation is a distinction between kinds of decisions, not between kinds of people.

##### Rationale and Alternatives
- **Treat implementation as part of architecture (rejected).** While every implementation decision has some architectural dimension, treating all implementation as architecture would eliminate the useful distinction between decisions that affect the system's properties and decisions that do not. The distinction is not about importance — an implementation bug can be as consequential as an architectural flaw — but about the kind of reasoning required to evaluate and make each type of decision.

##### Prior Art
The distinction between architecture and implementation is discussed in the software architecture literature (Bass, Clements, and Kazman, "Software Architecture in Practice," various editions) and is implicit in the ISO/IEC 42010 standard.

##### Unresolved Questions
1. Should Memar define explicit criteria for when an implementation change requires architectural review?
2. How should architectural decisions be documented in a way that remains accessible to contributors who primarily work at the implementation level?


### Relationships Between Concepts
The concepts defined in this RFC are not independent, but their relationships cannot be captured by a linear ordering, a tree, or a taxonomy. They form a conceptual graph — a network of nodes (concepts) connected by different types of edges (relationships). This section makes those edge types explicit, because in a graph, ambiguity lives not in the nodes but in the edges: if the types of relationships between concepts are not clearly distinguished, readers will fill in the gaps with assumptions — often hierarchical ones — that the RFC does not intend.

#### Meta-Principle: Concepts Are Themselves Systems
Architecture, Framework, Protocol, Model, Process, Structure, and similar concepts defined in this RFC are themselves Systems. Each is a collection of interacting elements organized toward a purpose. This has a important consequence: when we say that Architecture shapes a System, or that a Framework constrains a System, we are really saying that one System influences, constrains, describes, or shapes another System. The relationship between any two concepts in this RFC is, at the deepest level, a relationship between two Systems.

This principle prevents a common source of confusion: the assumption that these concepts belong to fundamentally different metaphysical categories. They do not. A Framework is a System that constrains other Systems. A Model is a System that represents other Systems. A Protocol is a System that governs processes within other Systems. The edge types described below are therefore not category differences but specific modes of systemic influence.

#### A Conceptual Map
The following diagram shows the central concept (System) and the primary relationship types connecting it to related concepts. Each arrow label denotes a distinct type of relationship:

```
                               Science
                                 │
                                 │ produces
                                 ▼
                              Knowledge
                                 │
                                 │ applied as
                                 ▼
                             Technology
                                 │
                                 │ enables
                                 ▼
                          System Development
                                 │
                                 │ creates / modifies
                                 ▼

    ┌────────────────────────── System ──────────────────────────┐
    │                                                            │
    │   ┌──────────┐  ┌──────────┐  ┌──────────┐                │
    │   │ Framework │  │Architecture│  │ Process  │                │
    │   └─────┬────┘  └─────┬────┘  └─────┬────┘                │
    │         │             │             │                       │
    │    constrained    shaped by    expressed by                 │
    │       by            │             │                       │
    │         │             │             │                       │
    │         └──────┬──────┘──────┬──────┘                       │
    │                │             │                              │
    │         co-equal      continuously                          │
    │         aspects        influence                             │
    │         of System      each other                           │
    │                                                            │
    │   ┌──────────┐  ┌──────────┐  ┌──────────┐                │
    │   │ Structure │  │  Model   │  │ Protocol │                │
    │   └─────┬────┘  └─────┬────┘  └─────┬────┘                │
    │         │             │             │                       │
    │   described by  represented by governed by                  │
    │         │             │             │                       │
    │         └──────┬──────┴──────┬──────┘                       │
    │                │             │                              │
    │         System contains, is described by,                   │
    │         represented by, and governed by                     │
    │         all of these simultaneously                        │
    │                                                            │
    └────────────────────────────────────────────────────────────┘

                           Implementation
                                 │
                                 │ realizes
                                 ▼
                             System (as
                           concrete artifacts)

    Cross-Cutting (operate across the entire graph):
    ┌─────────────┐  ┌──────────┐  ┌──────────┐
    │ Abstraction │  │  Model   │  │ Process  │
    └─────────────┘  └──────────┘  └──────────┘
    Not stages; mechanisms that pervade
    the entire conceptual structure.
```

#### Edge Types: What Kinds of Relationships Exist?
The diagram above uses distinct relationship labels rather than a single "depends on" arrow. This is deliberate. The relationships between these concepts are not all of the same kind, and treating them as if they were — as a single "dependency" type — is what produces the hierarchical misunderstandings this RFC seeks to prevent. The primary edge types are:

**contains**: A System contains Processes and Structures. A city contains streets; a body contains metabolic processes. This is a structural/compositional relationship — the part exists within the whole and contributes to its behavior.

**described by**: A System can be described through its Structure or its Processes. This is not the same as containing them. A city *contains* streets, and it can also be *described by* those streets. Both statements are true, but they express different relationships: one is about composition, the other is about epistemic access.

**shaped by**: Architecture shapes a System. This is an active, transformative relationship — architecture participates in determining what the system becomes. Crucially, Architecture is itself a System, so "shaped by" is really one System influencing the development of another.

**constrained by**: A Framework constrains the design space of Systems built within it. Constraints are not descriptions or predictions — they are active limitations on what is possible.

**expressed by**: A System is expressed by its Processes. This relationship is about manifestation: processes are how a system's structure and purpose become observable in time.

**represented by**: A Model represents a System (or an aspect of it). Representation is an epistemic relationship: the model stands in for the system for the purpose of reasoning.

**governed by**: Protocols govern Processes within a System. Governance is a regulatory relationship: the protocol defines what interactions are valid, in what order, and under what conditions.

**realized by**: An Implementation realizes a System's design as concrete artifacts. Realization is the relationship between abstract design and executable form.

**influences**: A general-purpose relationship that captures mutual effects between concepts. Architecture and Process continuously influence one another. Implementation experience influences Modeling. Technology influences Architecture.

**produces**: Science produces Knowledge. This is a generative relationship — one concept is the output of another's activity.

**enables**: Technology enables System Development. Knowledge enables Technology. This is a capability relationship — one concept makes another possible without fully determining it.

#### Epistemic Influence vs. Structural Containment
A critical distinction pervades the graph above, and failing to recognize it is the primary reason readers mistakenly place Architecture "above" other concepts:

- **Epistemic influence** is directional and non-symmetric. Science produces knowledge (not the reverse). Technology enables system development (not the reverse). These are directional influences that reflect the order in which concepts should be understood for sound reasoning — the Concept-First sequence.

- **Structural containment** is about what is part of what. A System contains Processes. A System contains Structures. These are not hierarchical rankings among concepts; they are statements about how the concepts compose.

- **Perspective relationships** are about how we access or interact with a concept. A System can be described by its Structure, represented by a Model, or realized by an Implementation. These do not compete; they coexist.

The error of reading Architecture as an "uber-concept" comes from conflating these relationship types — specifically, from interpreting "Architecture shapes a System" as "Architecture contains or is above Structure, Process, and Model." It does neither. Architecture shapes a System. Structure describes a System. Process expresses a System. Model represents a System. These are different edge types, not a hierarchy.

#### Cross-Cutting Concepts
Several concepts do not occupy a single position in the graph but operate across the entire conceptual structure:

- **Abstraction** is not a stage; it is a mechanism used at every point in the graph. Scientists abstract reality into models, architects abstract systems into structures, and implementers abstract details into interfaces. Abstraction is the cognitive tool by which complexity is managed at every level.

- **Model** is not a stage that precedes implementation. Scientists model phenomena, architects model systems, and implementers model behavior. Modeling is a continuous activity that accompanies every stage of system development. The "Model → Protocols → Implementation" sub-chain is therefore misleading; modeling operates everywhere, not just between architecture and implementation.

- **Process** is not subordinate to Architecture. Architecture and Process continuously influence one another — architecture shapes processes, and processes in turn reveal, validate, and reshape architecture. Process pervades the entire graph: systems contain processes, architecture governs processes, technology enables processes, and implementation realizes processes.

#### Co-Equal Aspects of System
**Framework and Architecture** are co-equal aspects of System, not in a parent/child hierarchy. They are related but distinct: Framework defines *what is possible*; Architecture defines *what was chosen*. Both produce constraints, but of different kinds (domain-level vs. system-level). See the Framework section for the full treatment of this relationship, including examples.

#### System as Central Node
Every other concept in this RFC exists in relation to a System: architecture is the architecture *of* a system, a framework provides the design space *for* systems, a process occurs *within* a system, technology is knowledge applied *to* systems, a model is a model *of* a system (or of an aspect of reality relevant to a system), and an implementation is an implementation *of* a system's design. This is why System is defined first in this RFC and why it is the node to which the most edges connect.

#### Discussion

##### Drawbacks
A graph-based model is inherently more complex to communicate than a linear chain. Readers who expect a simple ordering may find the multiple edge types and cross-cutting relationships harder to internalize. Memar accepts this cost because the simplicity of a linear chain is deceptive: it creates false confidence in a hierarchy that does not exist, and that false confidence propagates into architectural reasoning as an unconscious assumption that some concepts are "above" others.

##### Rationale and Alternatives
- **Present the concepts as a linear dependency chain (rejected).** A linear chain implies that concepts can be ordered from "most fundamental" to "most derived," and that each concept depends on exactly one predecessor. This is false: Architecture depends on System, but also on Knowledge, Technology, and Process. Modeling depends on Architecture but also on Abstraction and System. The real relationships form a graph, and presenting them as a chain forces a tree-shaped mental model that the rest of the RFC contradicts.

- **Present the concepts as a flat list with cross-references (rejected).** A flat list does not convey the relationship structure at all. It leaves readers to infer the relationships themselves, which produces exactly the kind of hierarchical misunderstanding this section exists to prevent.

- **Present the concepts as a taxonomy (rejected).** A taxonomy implies mutually exclusive categories, but these concepts overlap. Modeling and Architecture overlap; Protocol and Framework overlap; Technology and Implementation overlap. A graph accommodates overlap naturally through multiple edge types.

##### Unresolved Questions
1. Should this conceptual graph be formalized as part of Memar's development process, or should it remain as guidance?
2. Are there important relationship types missing from this model that should be added in future revisions?
3. Should Memar develop a formal notation for these edge types that can be used in other RFCs?


## Discussion

### Why a Single RFC for These Concepts?
During the initial discussion that motivated this RFC, the possibility of separating System and Architecture into independent RFCs was considered and rejected. The reason is practical: every statement about architecture is implicitly a statement about the system being architected, and every statement about how to understand a system is implicitly an architectural statement. Attempting to define System without reference to Architecture produces a definition that is inert — it describes what a system is but not why the distinction matters or how the concept is used. Attempting to define Architecture without a prior definition of System requires Architecture to define its own object, which either duplicates System's definition or silently assumes it. A single RFC that defines both concepts and their relationship is therefore more coherent than two RFCs that each pretend the other does not exist.

The same argument applies, with diminishing force, to the other concepts included in this RFC. Technology could plausibly be separated into its own RFC, but its definition is so closely tied to System (technology develops systems) and to Knowledge/Science (technology is applied knowledge) that separating it would create circular dependencies. Model and Abstraction are included because they are the primary mechanisms through which architectural reasoning operates, and because the Modeling RFC depends on both being defined. Protocol is included only as a brief pointer to its own RFC, to complete the conceptual map. Framework is included here with a brief definition and a link to its dedicated RFC (RFC 495003), which provides the full treatment of the Framework-Architecture co-equal relationship and Memar's specific application of the concept. Implementation is included because distinguishing it from Architecture is a frequent source of confusion and because it plays a central role in the conceptual relationship structure.

### Terminology Layer Placement
Consistent with the Terminology RFC's classification:

- **System**, **Abstraction**, and **Model** are treated as Scientific Terms: their meanings are grounded in established academic traditions (systems theory, cognitive science, philosophy of science), defined with explicit boundaries, and intended to be falsifiable and open to criticism and revision.
- **Technology** and **Architecture** are treated as Technology Terms: they name applied practices and engineering approaches rather than freestanding scientific concepts, though both are defined with more precision than typical technology terminology.
- **Framework** and **Implementation** are treated as Technology Terms for similar reasons.
- **Protocol** is treated as a Scientific Term by the Protocol RFC's own argument; this RFC defers to that classification.
- **Knowledge** and **Science** are treated as Scientific Terms by the nature of the concepts themselves.

### Naming Conventions
This RFC proposes no naming conventions for code-level identifiers. The concepts defined here are foundational and their names (System, Architecture, Technology, Model, Abstraction, Protocol, Framework, Implementation) are treated as common English words whose meaning within Memar is defined by this RFC, not by any naming convention.

### Drawbacks
This RFC attempts to define a large number of concepts in a single document. The risk is that some definitions receive less scrutiny than they would in a dedicated RFC. This risk is accepted because the alternative — defining each concept in isolation — creates the circular dependency problem described above, and because the primary purpose of this RFC is to establish a shared vocabulary, not to provide the final, exhaustive treatment of each concept. Concepts that require deeper treatment already have or are expected to receive their own dedicated RFCs: Protocol (RFC 495465), Framework (RFC 495003), and Modeling (modeling.md).

### Rationale and Alternatives
- **Define only System and Architecture, leaving the other concepts to their own RFCs (rejected).** The concepts in this RFC form a coherent conceptual graph. Defining System and Architecture without defining the concepts they relate to and that relate to them would produce an RFC that is internally incomplete and that forces each subsequent RFC to independently establish its own conceptual context.

- **Use existing standard definitions without adaptation (rejected).** While this RFC's definitions are grounded in existing traditions, no single existing standard provides a complete, mutually consistent set of definitions for all the concepts Memar needs. Synthesizing from multiple sources, with explicit attention to internal consistency and to the Terminology RFC's principles, produces a more useful result than uncritically adopting any single source.

### Prior Art
The approach of establishing a shared vocabulary before proceeding to domain-specific specifications is common in standards-setting bodies. The ISO/IEC 42010 standard for architecture description provides definitions of "system" and "architecture" that are broadly consistent with this RFC, though this RFC's definitions are broader in several respects (particularly the inclusion of non-computational systems and the lifecycle-spanning definition of architecture). The IEEE standard glossary of software engineering terminology provides definitions that are narrower, being restricted to software. This RFC draws on both traditions but is not bound by either.

### Unresolved Questions
1. Should this RFC eventually be split into multiple, more focused RFCs as the concepts mature, or should it remain as a single foundational document?
2. How should this RFC's definitions interact with definitions established by other standards bodies (ISO, IEEE, W3C) when those definitions conflict?
3. Should the conceptual graph's edge types be formalized into a notation that other RFCs can reference?

### Future Possibilities
- A dedicated RFC for **Constraint** as a first-class concept, since both Framework and Architecture depend on it and the distinction between domain-level and system-level constraints may warrant deeper formal treatment.
- A terminology registry that maps each term defined across all Memar RFCs to its definition, its terminology layer, and its relationships to other terms.
- A visual diagram of the conceptual graph suitable for inclusion in onboarding material.


## Change Rationale

### Initial Version
Introduces foundational definitions for System, Structure, Architecture, Technology, Knowledge, Science, Model, Abstraction, Protocol (by reference), Framework (by reference to RFC 495003), and Implementation. Establishes the conceptual graph — a network of nodes (concepts) and typed edges (relationship types) — that relates these concepts to one another. Positions this RFC as a prerequisite for all subsequent conceptual RFCs in the Memar ecosystem.

The definitions are synthesized from multiple sources — systems theory (von Bertalanffy, Boulding, Checkland), philosophy of technology (Ellul, Mumford, Heidegger), philosophy of science (Popper, Kuhn, Lakatos), and software architecture (ISO/IEC 42010, IEEE 610.12) — with explicit attention to internal consistency and to the Terminology RFC's principles of concept-first thinking, terminological precision, and scientific methodology.

The key architectural decisions in this RFC are:

1. Defining System before other concepts, in a single RFC, to avoid circular dependencies and to anchor the conceptual graph.
2. Defining Technology as applied knowledge rather than as artifacts, to prevent Tool-First Thinking.
3. Including non-computational examples (family, government, lifestyle, discourse, war) to ensure the definitions are maximally general.
4. Presenting the relationships between concepts as a typed graph rather than a linear dependency chain, flat list, or taxonomy — making explicit that the concepts are connected by multiple distinct relationship types (contains, described by, shaped by, constrained by, represented by, etc.) and that no concept is "above" another.
5. Establishing the meta-principle that concepts like Architecture, Framework, Protocol, and Model are themselves Systems, so that relationships between concepts are ultimately relationships between Systems.
6. Including Knowledge and Science to anchor the epistemic influence dimension of the graph.
7. Defining Structure as the set of capabilities and limitations a System exposes — explicitly distinguishing it from the common engineering connotation of "arrangement of parts" — and establishing the inseparability of capability and constraint.
8. Defining Framework and Architecture as co-equal aspects of System (Constraint Space vs. Decision Space), with a compact treatment here and a full treatment in the dedicated Framework RFC (RFC 495003).
