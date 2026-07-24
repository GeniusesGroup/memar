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
      - Works: ["Architect", "Initiated the need for this RFC", "Core definition of Technology as applied knowledge", "Inseparability of System and Architecture", "Lived-experience critique connecting technology and lifestyle", "War/discourse/governance as technologies", "ISA example as a test case for Architecture-as-System", "'Reality is the best guess one System can make of another' as the grounding intuition for structural abstraction", "Framework vs. Sub-Framework distinction", "Working test for Architecture legitimacy", "Original proposal to reintroduce open/closed/isolated systems classification, later expanded into the System Openness subsection"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Tasks:
      - Works: ["Initial draft", "Candidate definitions for System, Architecture, Technology, Protocol, Abstraction", "Bidirectional phrasing for the 'shaped by' edge", "Conceptual vs. Graph Centrality distinction", "Identified Edge Types as an emerging topic", "Argued against premature dedicated RFCs for Edge Types and Abstraction", "Pressed for explicit statement of the ISA-legitimacy departure from industry usage", "Connected this RFC to the Terminology RFC's mental-models principle"]
        URI: ""
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "High"
    Tasks:
      - Works: ["Initial draft", "Critical review and refinement", "Synthesized contributor inputs into a coherent document", "Added Knowledge, Model, Framework, Implementation sections", "Composed Relationships Between Concepts and Discussion"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Tasks:
      - Works: ["Critical review", "Structural critique", "Identified Abstraction/Model front-matter contradiction", "Framework-as-System vs. Framework-as-Aspect distinction", "Reformulated the Meta-Principle", "Structural vs. Purposive Abstraction, grounded in Maturana and Varela", "Expanded Omid's open/closed/isolated proposal into the full System Openness subsection", "Reconciliation pass with the Framework RFC (removed the residual 'Framework is a System' claim)", "Corrected contributor-attribution errors"]
        URI: ""
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

A foundational RFC that defines these terms explicitly is therefore not a philosophical luxury. It is a structural prerequisite for the coherence of every RFC that follows. The purpose of these definitions is not merely semantic consistency — it is to improve the quality of mental models used to reason about systems. Terminology debt, as the Terminology RFC argues, is a root cause of architectural debt: imprecise terms produce imprecise mental models, and imprecise mental models produce imprecise architectures. This RFC intervenes at the earliest possible point in that chain.


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

### A Note on Systems Thinking
Readers will notice, across this RFC and others, that many things — a person, a team, a company, a programming language, a habit, a conversation — can plausibly be described as a System, depending on the observer's purpose and level of analysis. This is not a flaw in these definitions; it is a basic feature of systems theory itself. System-hood is not an intrinsic property that some things have and others lack. It is a lens that can be applied to almost anything a person interacts with, because almost anything a person interacts with has interacting parts, a boundary an observer can draw around it, and behavior that depends on how those parts relate.

This has a direct consequence for how this RFC, and Memar's RFCs generally, should be read. At the level of casual explanation — in conversation, in code comments, in reasoning out loud — saying "X is a System" about nearly anything (a framework, a team, a habit) is rarely wrong, precisely because the lens is so widely applicable. Where this RFC is careful is at the level of formal *definition*: no concept's core identity is defined as System (see Relationships Between Concepts > Meta-Principle), because a definition that could apply equally to everything loses its power to distinguish anything from anything else. A definition and an explanatory aside are held to different standards for this reason, not because the explanatory aside is wrong.

Readers who have not previously encountered systems theory or systems thinking are encouraged to read at least an introductory treatment of the field — von Bertalanffy's *General System Theory* or Meadows's *Thinking in Systems* are reasonable starting points — not because this RFC requires specialist knowledge, but because the intuition that "almost everything can be viewed as a System" is easier to apply correctly, without either over- or under-using it, once it has been encountered outside the specific context of Memar.


### Concepts at a Glance
Before the detailed definitions, a brief orientation to how the key concepts relate:

- A **System** is what is being built or studied — a collection of interacting elements organized toward a purpose.
- **Architecture** is the collection of processes involved in the design and development of a system — one of several co-equal lenses through which a system is understood and evolved.
- **Technology** is the knowledge applied to create, modify, or evolve systems — not the artifacts themselves, but the know-how behind them.
- **Knowledge** and **Science** are the broader epistemic foundations from which technology is derived.
- A **Model** is a simplified representation of a system or aspect of reality, used to reason about it.
- An **Abstraction** is the mechanism by which models reduce complexity — preserving what matters and discarding what does not, relative to a specific purpose.
- A **Protocol** (defined in detail in its own RFC) is a structured body of knowledge that enables participants within a system to interact, coordinate, and evolve consistently.
- A **Framework** is a description of a system. It characteristically exists prior to, and independently from, any specific realization of the system it describes. A framework does not describe a particular realized system; it defines a space within which multiple systems may be created, understood, or evaluated. See the [Framework RFC](./framework.md) for Memar's specific application of this concept.
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

#### System Openness: Open, Closed, and Isolated
A System's relationship to another System, with respect to a specific channel of influence, may be one of three kinds:

- **Open**: influence flows in both directions. Each System can affect, and be affected by, the other.
- **Closed**: influence flows in one direction only. One System affects the other without being affected back, for the channel under consideration.
- **Isolated**: no influence crosses between the two Systems, for the channel under consideration.

These are not fixed, permanent properties of a System in general. They describe a specific relationship, with respect to a specific kind of influence, at a specific point in time — and all three can change. The same pair of Systems may be open with respect to one channel and closed with respect to another. A relationship that is closed at one point in time may become open later, and vice versa.

For example, a contributor shaping a framework's design may, for a period, act as a system that is closed with respect to that framework — influencing its design without incorporating anything back from it. Later, the same contributor may shift to an open relationship with the framework: incorporating feedback derived from using the framework, or from other contributors' critique of it, back into how they think and act. This shift does not require redefining either System; it is a change in the *type* of relationship between two Systems that are already connected by an "influences" edge (see Relationships Between Concepts). This is also why a directional statement like "Technology enables System Development" (an epistemic-influence edge) does not preclude experience from System Development later influencing Technology — the two Systems may simply have moved from a closed relationship to an open one, or have always been open with respect to a different channel than the one the directional statement describes.

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
3. Should System Openness (open/closed/isolated) be formalized as a labeled property on the "influences" edge type in the conceptual graph, so that RFCs can state explicitly which kind of relationship they mean rather than leaving it implicit?

### Structure
**Structure** is the set of capabilities and limitations (constraints) a System exposes and enforces.

Capabilities are what the System *can* do — the operations, transitions, and interactions available to those who interact with it. Constraints are what the System *cannot* do, or the conditions under which a capability is available, valid, or forbidden. Structure, in this sense, defines the space of admissible operations for a System: what is permitted, what is forbidden, and under what conditions a given capability applies.

#### Structure Is Not the Arrangement of Parts
Structure is not the arrangement of a system's parts — its component hierarchy, module layout, or dependency graph. That is a separate concern: how a system is composed or assembled. Much of the confusion around the word "structure" in general usage traces back to the construction industry, where "structure" and "building" are used almost interchangeably to mean the physical arrangement of a construction — walls, beams, floors. That usage describes composition, not capability and constraint, and Memar does not inherit it.

Memar does not yet have a dedicated, formalized term for "the arrangement of a system's parts" as a first-class concept (candidate names, and whether it warrants a concept of its own, are left open — see Unresolved Questions). What matters for this RFC is only the negative claim: whatever that concept turns out to be called, it is not Structure. A system's component layout may be *one input* that determines its Structure — how parts are arranged can affect what the system can and cannot do — but the layout itself is not the Structure. Confusing the two is the same class of error the Terminology RFC identifies under concept-vs-representation confusion: treating a description of parts as though it were a description of capability and constraint.

#### The Inseparability of Capability and Constraint
Capabilities and constraints are not independent properties that happen to coexist in a structure. They are two aspects of the same thing — inseparable, like two sides of a coin. Every capability implies limitations. Every limitation enables capabilities.

Consider a system that enforces **no shared mutable state**. This is a constraint: it forbids a certain kind of interaction. But that same constraint enables **thread safety** — a capability that would not exist without the limitation. Or consider a residential building designed with a **central kitchen** instead of private kitchens. This is a constraint: it removes the freedom to cook privately. But it simultaneously enables **economy of scale, quality control, and operational efficiency** — capabilities that would be impossible or prohibitively expensive in a building with 100 private kitchens.

This inseparability has a practical consequence for how structures are reasoned about: a proposed structural change cannot be evaluated by looking only at the capabilities it adds or only at the constraints it removes. Every addition of capability also adds constraint, and every removal of constraint also removes capability. Sound architectural reasoning accounts for both sides of every structural decision.

#### Structure, Behavior, and Implementation
Structure cannot be defined independently of behavior: describing what a System does inherently requires knowing what it is permitted to do and what it is restricted from doing. A definition of Structure that omits behavior collapses into a description of static shape — fields, storage layout — which Memar treats as a symptom of premature implementation-oriented thinking, not as Structure itself.

#### Discussion

##### Unresolved Questions
1. Does "the arrangement of a system's parts" warrant a dedicated, formally defined concept of its own within Memar, and if so, what should it be called? Until this is resolved, Structure's definition can only state what it excludes, not what the excluded concept positively is.
2. How does Structure relate to the layout-related vocabulary already in use elsewhere in Memar (for example, package and module layout in memar-go), and should this RFC's Structure be renamed if it turns out to conflict with established usage rather than merely with general-industry usage?

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

#### Process and Structure
Structure and Process describe a System from two different vantage points, and the distinction between them is easiest to state precisely as follows: **Structure defines the space of admissible operations** a System exposes and enforces — what is permitted, forbidden, or conditionally available; **Process is the concrete, temporal enactment of one path through that space** — the specific sequence of activities that actually occurs, in a specific order, at a specific time.

A Structure can exist without any particular Process ever occurring — a System may expose a capability that is never invoked. A Process, conversely, cannot occur outside the space its System's Structure admits: a Process that attempts an operation the Structure forbids is not a different kind of Process, it is a failure, a violation, or evidence that the Structure was mis-specified. This is a one-directional dependency: Structure bounds what Process can do; Process does not bound what Structure permits, though repeated observation of Process may reveal that a Structure's stated bounds do not match its enforced bounds, which is itself useful information for refining the Structure.

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

#### Shape Is Not Control, and Not One-Way
Throughout this RFC, Architecture is described as "shaping" a System. This word is chosen deliberately — it captures the active, transformative role architecture plays in determining what a system becomes. But "shapes" does not mean "controls," and it does not mean the influence is one-way.

Consider classical architecture as a System: it permits certain choices (grand columns, ornate detailing, specific proportions) and forbids others (minimalist blank walls, uniform white surfaces). In doing so, it shapes what the resulting building can express — grandeur, authority, permanence. But it also creates constraints: high cost, specialized labor, long construction timelines. A decision-maker who encounters these constraints during the architectural process may revise their original goals, which in turn re-invokes the goal-selection process and reshapes the architecture itself. The influence is bidirectional and iterative, consistent with the System Openness model (see System > System Openness: Open, Closed, and Isolated).

The same bidirectionality holds in software. An architecture that mandates a specific consistency model shapes every subsequent design decision — but the experience of implementing that consistency model may reveal that it is too expensive for the system's actual workload, which feeds back into architectural revision. Architecture shapes the System; the System, through its behavior under real conditions, reshapes Architecture. This is not a defect of the definition — it is how real development works, and the definition is designed to accommodate it rather than to pretend it does not happen.

#### A Working Test: Does This Deserve to Be Called Architecture?
The ISA example above (see Prior Art) is used deliberately as a calibration point, not merely as an illustration. Memar's position is that something earns the name Architecture only if it exhibits, at some meaningful scale, the properties System itself requires: purpose, boundary, emergence, and interdependence — the same bar the Meta-Principle applies when asking whether a concept may be modeled as a System (see Relationships Between Concepts > Meta-Principle). An ISA clears this bar: it has purpose, produces emergent trade-offs no single decision fully explains, and cannot be understood in isolation from what it depends on and constrains. A one-paragraph note justifying a single naming choice does not clear this bar, no matter how confidently it is labeled "architecture."

This has a consequence that Memar states explicitly rather than leaving implicit: much of what is commonly called "Software Architecture," "Service Architecture," or "Microservice Architecture" in industry usage may not qualify as Architecture in this RFC's sense. Some of it does — a genuinely evolving, multi-contributor body of decisions with real emergent consequences clears the bar regardless of what domain it is applied to. But some of it is better described, in Memar's vocabulary, as Design, Structure, Pattern, or a Sub-Framework (see the Framework RFC for the Framework/Sub-Framework distinction) that has borrowed the word "architecture" for its perceived weight rather than earned it. This is not a claim that such artifacts are worthless — a well-chosen pattern or a well-scoped sub-framework is valuable on its own terms — only that calling them Architecture, in Memar's sense, overstates what they are.

This is a direct, intentional departure from a large body of common software engineering usage, not an incidental side effect of a stricter definition, and Memar states it as such rather than letting a reader discover the implication on their own. It is also, at the time of this writing, a position that has been argued for but not yet stress-tested against a wide range of real cases (see Unresolved Questions below) — it should be read as Memar's current working criterion, not as a settled classification that every future RFC must defer to without question.

#### Discussion

##### Drawbacks
The breadth of this definition means that nearly any decision about a system could be classified as architectural, which risks the term becoming vacuous. Memar mitigates this by not treating "architectural" as a binary label but as a spectrum: a decision's architectural significance is proportional to its impact on the system's behavior, evolvability, or properties. Low-impact decisions — such as the choice of a local variable name — are architectural in the trivial sense that they are part of system development, but they carry negligible architectural weight. High-impact decisions — such as the choice of consistency model, communication pattern, or module boundary — carry substantial architectural weight and deserve proportionally more deliberation, documentation, and review.

##### Rationale and Alternatives
- **Restrict architecture to "high-level design" (rejected).** This is the most common industry definition, but it creates a false distinction between "architectural" decisions and "implementation" decisions that does not hold under scrutiny. Many decisions made during implementation have architectural consequences, and excluding them from the architectural domain means those consequences go unexamined.

- **Define architecture as "the structure of a system" (rejected).** This confuses a system's structure with the process and decisions that produced it. A system's structure is a snapshot; architecture is the reasoning, constraints, and trade-offs that the snapshot embodies.

- **Define architecture as "the decisions that are expensive to change" (rejected).** While pragmatically useful as a heuristic, this is a consequence-based definition that can only be applied retrospectively. A decision is not known to be expensive to change until after it has been made and the attempt to change it has been evaluated. Architecture, as a discipline, needs a definition that can be applied prospectively — before the consequences of a decision are known.

##### Prior Art
ISO/IEC 42010:2022 defines architecture as "the fundamental concepts or properties of a system in its environment embodied in its elements, relationships, and in the principles of its design and evolution." This RFC's definition is consistent with that standard but emphasizes the process dimension more explicitly: architecture is not only what the system is, but how it came to be that way and how it will continue to change.

**Instruction Set Architecture (ISA)** provides a concrete and instructive example of Architecture-as-System. An ISA is not an implementation (it is not a particular chip design), not a tool (it is not a compiler or an assembler), and not a mere description (a document describing an ISA is not the ISA itself — the ISA is the body of decisions that the document records). An ISA is the collection of processes by which the boundary between hardware and software is designed: which operations are defined, how memory is addressed, what the calling conventions are, how exceptions propagate. An ISA has purpose (enabling software-hardware coordination), constraints (what instructions are and are not available), dependencies (on the physics of transistor behavior, on manufacturing capabilities), and evolution (x86, ARM, RISC-V each represent a distinct evolutionary path shaped by different architectural trade-offs). An ISA that is defined without reference to the electronic substrate that will implement it is difficult to evaluate — understanding *why* an ISA made certain choices requires understanding the constraints of the substrate, even though the ISA itself is not that substrate. This is precisely the relationship this RFC describes: Architecture is Architecture *of* a System, *for* a purpose, *under* constraints — and an ISA exhibits all of these properties in a form that can be examined directly.

##### Unresolved Questions
1. Should Memar develop a more formal framework for assessing the architectural weight of a decision, or is the proportional-impact heuristic sufficient?
2. How should architectural decisions made by different contributors at different times be reconciled when they conflict?
3. The ISA-level legitimacy test (see A Working Test, above) has been argued for but checked against only a handful of examples. Does it hold up against a wider range of cases — for instance, a small but genuinely long-lived and multi-contributor open-source library's design decisions, which may be smaller in scope than an ISA but still exhibit real emergence and interdependence? Where exactly is the line, and should it be a hard boundary or a graded one, consistent with the Drawbacks discussion above treating "architectural weight" as a spectrum rather than a binary?


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

The conceptual definitions of Model and Abstraction are established in this RFC, since both are used pervasively across the entire conceptual graph and cannot wait on a document that depends on this one. The full treatment of Modeling as an ongoing architectural activity — how Memar performs, validates, and evolves models in practice — is defined in the [Modeling RFC](./modeling.md), which builds on the definitions established here.


### Abstraction
An **abstraction** is a simplified representation of a selected aspect of reality that preserves information relevant to a particular purpose while deliberately omitting information that is not.

Abstraction is the primary mechanism by which complexity is managed in system design. Without abstraction, every system design decision would need to account for the full complexity of the underlying reality — every electronic circuit would need to account for quantum electrodynamics, every software module would need to account for processor microarchitecture, every organizational design would need to account for individual psychology. Abstraction allows reasoning to proceed at the level of detail that is appropriate to the decision being made.

Abstractions are not inherent properties of reality. They are constructs created by observers for specific purposes. A useful abstraction for one purpose may be useless or misleading for another. The abstraction "temperature" is useful for designing a heating system but useless for designing a chemical reaction — the latter requires knowledge of molecular kinetic energy, which temperature abstracts away. The same principle applies in software: the abstraction "user" is useful for designing an authentication system but may be misleading for designing a recommendation engine, where the relevant entity is closer to "a sequence of observed preferences over time" than to "a person with an identity."

#### Abstraction and Leaky Boundaries
Abstractions inevitably leak. The information they omit does not cease to exist; it continues to affect the system's behavior in ways that the abstraction does not represent. A database abstraction that hides concurrency semantics will leak when two transactions conflict. A network abstraction that hides latency and failure will leak when the network partitions. An organizational abstraction that hides team communication patterns will leak when coordination failures occur.

Recognizing that abstractions leak — and designing with that leakage in mind rather than pretending it does not exist — is a hallmark of mature engineering. Within Memar, abstractions should be chosen not only for what they hide but for how predictably they leak. An abstraction that leaks in well-understood, well-documented ways is preferable to one that appears clean but fails catastrophically when the hidden complexity becomes relevant.

#### Structural Abstraction vs. Purposive Abstraction
The examples above — temperature, user — describe **purposive abstraction**: a deliberate choice, made for a specific reasoning goal, about what to preserve and what to discard. But not all abstraction is chosen. A second, more fundamental kind of abstraction is imposed on any observing System by its own Structure, before any purpose is even considered.

Every System that observes another System is itself a System, with its own capabilities and limitations. What it can perceive of the observed System is bounded by those limitations, whether or not it intends to abstract anything at all. A human eye responds to a narrow band of electromagnetic wavelengths and is structurally incapable of registering the rest; this is not a simplification chosen for a purpose, the way an engineer chooses to reason about "temperature" instead of molecular kinetic energy — it is a constraint of the observing System's own Structure, present before any purpose is chosen. Purposive abstraction operates on top of, and is bounded by, this prior structural abstraction: a reasoner can choose to discard information it structurally had access to, but it cannot choose to include information its own Structure never made available in the first place.

One practical consequence follows directly: what any System knows of another System is never the observed System directly, but the observing System's best available reconstruction of it, shaped by the observer's own Structure. This is consistent with, and reinforces, the fallibilist position already established in the Knowledge and Science section — that scientific knowledge does not claim certainty, only mechanisms for detecting and correcting error. Those mechanisms are necessary precisely because no observing System has unmediated access to another System; every account of a System is itself the output of some other System's abstraction process, structural and purposive together, and is therefore always provisional and open to revision as the observing System's own capabilities change.

#### Discussion

##### Drawbacks
Teaching abstraction as a first-class concern adds conceptual overhead to the learning process. Contributors must learn not only how to use abstractions but how to evaluate their boundaries, their leakage patterns, and their suitability for specific purposes. This is a real cost, particularly for newcomers who are accustomed to treating abstractions as opaque, leak-proof boundaries provided by a framework or language runtime.

##### Rationale and Alternatives
- **Treat abstraction as an implementation detail (rejected).** This is the default in many software frameworks, where abstractions are provided by the framework and treated as opaque by the user. This works until the abstraction leaks, at which point the user is unable to reason about the failure because they were never expected to understand what the abstraction hides. Memar considers this unacceptable for a framework whose stated goal is to improve reasoning quality.

##### Prior Art
The theory of abstraction in computer science is developed in detail in the literature on abstract data types, information hiding (Parnas, "On the Criteria to Be Used in Decomposing Systems into Modules," 1972), and abstraction barriers. The philosophical treatment of abstraction as a cognitive process is developed in the cognitive science literature (e.g., Hofstadter, "Gödel, Escher, Bach," 1979). The distinction between structural and purposive abstraction is consistent with Maturana and Varela's concept of structural coupling ("Autopoiesis and Cognition," 1980; "The Tree of Knowledge," 1987), in which an observing system's own structure determines which perturbations from another system it is even capable of registering, independent of any purpose the observer might later apply to what it registers.

##### Unresolved Questions
1. Should Memar provide explicit mechanisms for documenting abstraction leakage, or should this be left to informal documentation?
2. How should the choice of abstraction level be guided in Memar's modeling process?
3. Should the distinction between structural and purposive abstraction be reflected as two separate, formally named concepts in a future revision, or is it sufficient as an explanatory distinction within a single Abstraction concept?


### Protocol
Protocols exist *within* systems. A protocol governs one or more processes within a system, and the system provides the boundary that gives the protocol its scope. This relationship is foundational rather than incidental: a system without protocols governing its internal processes is not a system in the systems-theory sense — it is merely a collection of independent elements with no defined interactions. Protocol, Process, and System co-arise; you cannot meaningfully discuss one without the others.

Protocol's full definition, ontology, and relationship to Process are defined in the [Protocol RFC](./protocol.md).

### Framework
A **framework** is a description of a system.

Here, **description** carries its ordinary sense: **a statement that represents something in words** (or, more broadly, in any symbolic form). This RFC does not treat Description as a specialized technical term requiring its own Reference-level definition — it is used in the same sense the word carries in general usage, and the discriminative work in this RFC is done by what is being described (a system) and how (see Model, above, for the closest related concept, and Framework and Model, below, for how the two differ despite both being kinds of description).

A framework does not describe a particular realized system. It defines a space within which multiple systems may be created, understood, or evaluated. Framework descriptions characteristically exist prior to, and independently from, any specific realization of the system they describe — a property this RFC and the Framework RFC term *hypothetical* (meaning "assumed before realization," not "imaginary or unrealizable").

Framework and Architecture are co-equal aspects of a System — neither is "above" or "below" the other. They answer different questions: Framework defines *what kinds of solutions are allowed*; Architecture defines *which solution was chosen*. The full treatment of this relationship, including the distinction between domain-level constraints (framework) and system-level constraints (architecture), the distinction between frameworks and sub-frameworks, the relationship between Framework and Model, the explicit/implicit framework distinction, and the goal-oriented nature of frameworks, is provided in the [Framework RFC](./framework.md).

#### Framework as Aspect, and Framework Considered as a System
A framework's core identity, per this RFC and the Framework RFC, is that of a description — not a System. This distinction matters because it is easy to slide from "a framework constrains a system" into treating "being a System" as part of what a framework fundamentally is. It is not — in the same way that Technology's core identity is applied knowledge, not System (see Technology, above). System is never baked into a concept's core definition in this RFC; at most, it is a secondary lens that may or may not apply to a given instance of a concept, and Framework is no exception to that rule.

**Framework Considered as a System.** Independently of the aspect relationship above, a specific framework may, in a given instance, also be examined as a System in its own right. Khayyam, considered as an evolving body of RFCs, contributors, and conventions, can be studied this way — it has its own Architecture, its own contributors, its own emergent design outcomes — quite apart from any System built using it. But this is a fact about Khayyam specifically (and about any sufficiently mature, evolving, multi-contributor framework), not a claim built into what the word "Framework" means. A framework does not need to be a System, or to be studied as one, for the Framework-as-Aspect relationship above to hold: even a small, single-author, never-revised framework still constrains the Structure of systems built within it, whether or not it independently qualifies as a System by the criteria in the Meta-Principle (see Relationships Between Concepts > Meta-Principle, below).

**Framework as Aspect.** When a System S is built within a framework F, F's description functions as an aspect of S — specifically, the part of S's Structure that S inherited from F rather than chose for itself. This is what "Framework and Architecture are co-equal aspects of a System" means: S's Structure is partly shaped by decisions made within S (Architecture) and partly shaped by constraints inherited from F (Framework-as-aspect). Whether this relationship is best described as F becoming "an aspect of" S, or as F constraining S's Structure from outside without F entering S in any sense, is an open question the Framework RFC leaves for future revision (see the Framework RFC, Unresolved Questions) rather than one this RFC settles.
This mirrors the pattern already established for Architecture: the concept's definition does not require System-hood, but a sufficiently rich, ongoing instance of the concept may be modeled as a System when that lens is useful for reasoning about it. The relationship is also not one-to-one: a single framework can be an aspect of many different Systems simultaneously (Khayyam is an aspect of the Structure of every system built with it) while, from its own vantage point and only when the System lens is applied to it, remaining one System.


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

#### Meta-Principle: Some of These Concepts Are Themselves Systems
Some, but not all, of the concepts defined in this RFC are themselves Systems. A concept qualifies as a System only if it independently satisfies System's own criteria — interacting elements, a boundary, emergent behavior, and interdependence (see System > Key Properties) — not merely because it can be described using System-like vocabulary such as "a collection" or "a set."

**Architecture and Framework may qualify, when considered as ongoing activities.** Architecture — when understood not as a static description but as the evolving collection of processes, contributors, feedback loops, and decisions by which a system is designed and developed — may itself be modeled as a System. It has interacting elements (contributors, tools, processes), a boundary (the scope of architectural concern for that system), emergent behavior (design outcomes that no single contributor intended), and interdependence (a change in one architectural decision propagates to others). The same applies to Framework, considered as an evolving body of constraints, conventions, contributors, and processes. Khayyam, considered as an evolving body of RFCs, contributors, and conventions, is a System in its own right, with its own Architecture, quite apart from any system built using it. Protocol's status as a System is addressed by the Protocol RFC.

However, this is not an unconditional claim that *every* architecture is necessarily a System. A very small, purely descriptive architecture — a brief note documenting a single design choice — may not independently exhibit emergence or interdependence in a meaningful sense. The claim is that Architecture, as Memar understands and practices it (a continuous, evolving, multi-contributor process), does qualify; and that any architecture substantial enough to shape a System's long-term properties will typically exhibit the characteristics that make the System model useful for reasoning about it.

**Structure, Process (a single instance), and Model do not qualify on their own.** Structure is a *set* of capabilities and limitations — a description, not itself a collection of interacting elements producing emergent behavior. A single Process is a sequence of activities that acquires its meaning entirely from the System it occurs within (see Process > Process and System) — it has no independent boundary or purpose of its own. A Model is a representation constructed by an observing System, not an independent System that could be said to have its own emergent behavior. These three remain what the rest of this RFC treats them as: mechanisms and descriptions used *to characterize* Systems, not additional Systems standing alongside the ones they characterize.

This has a practical consequence for reading the relationships below: when we say that Architecture shapes a System, or that a Framework constrains a System, we are describing one System influencing another (see System Openness, above, for how the direction and mutuality of that influence can itself change over time). But when we say a Structure describes a System, or a Model represents a System, we are not describing a relationship between two Systems — we are describing how a single System is characterized, from a particular vantage point, by something that is not itself a System. Conflating these two kinds of statement is a more subtle version of the same hierarchical misreading this section exists to prevent: it is possible to over-correct against a false hierarchy by inventing Systems that do not independently earn the label, which is its own source of confusion.

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

This diagram depicts Framework in its role as *Framework-as-aspect* — the part of a System's Structure inherited from the framework it was built within. It does not depict a framework considered as a System in its own right, which is an optional, instance-specific lens rather than part of what the diagram's edges assert. See Framework > Framework as Aspect, and Framework Considered as a System.

#### Edge Types: What Kinds of Relationships Exist?
The diagram above uses distinct relationship labels rather than a single "depends on" arrow. This is deliberate. The relationships between these concepts are not all of the same kind, and treating them as if they were — as a single "dependency" type — is what produces the hierarchical misunderstandings this RFC seeks to prevent. The primary edge types are:

**contains**: A System contains Processes and Structures. A city contains streets; a body contains metabolic processes. This is a structural/compositional relationship — the part exists within the whole and contributes to its behavior.

**described by**: A System can be described through its Structure or its Processes. This is not the same as containing them. A city *contains* streets, and it can also be *described by* those streets. Both statements are true, but they express different relationships: one is about composition, the other is about epistemic access.

**shaped by**: Architecture shapes a System, while feedback from the System continuously reshapes the Architecture. This is an active, transformative relationship — architecture participates in determining what the system becomes — but it is not one-way. Architecture, when considered as an ongoing, evolving, multi-contributor process rather than a static description, may itself be modeled as a System (see Meta-Principle, below); read that way, "shaped by" is one System-like process influencing the development of another, and the System Openness model (see System > System Openness) determines whether that influence is open (bidirectional), closed (one-way), or isolated at any given time. This reading is a useful lens, not a requirement: the edge holds regardless of whether, in a given case, Architecture is substantial enough to independently qualify as a System.

**constrained by**: A Framework constrains the design space of Systems built within it. A framework is a description of a system; the `constrained_by` relationship captures the effect of that description on another System's Structure. The constraint is not necessarily documented or explicit — an implicit framework element (e.g., Linux's "everything is a file" principle) can constrain a System's Structure just as effectively as a formally specified one.

**expressed by**: A System is expressed by its Processes. This relationship is about manifestation: processes are how a system's structure and purpose become observable in time.

**represented by**: A Model represents a System (or an aspect of it). Representation is an epistemic relationship: the model stands in for the system for the purpose of reasoning.

**governed by**: Protocols govern Processes within a System. Governance is a regulatory relationship: the protocol defines what interactions are valid, in what order, and under what conditions.

**realized by**: An Implementation realizes a System's design as concrete artifacts. Realization is the relationship between abstract design and executable form.

**influences**: A general-purpose relationship that captures mutual effects between concepts. Architecture and Process continuously influence one another. Implementation experience influences Modeling. Technology influences Architecture.

**produces**: Science produces Knowledge. This is a generative relationship — one concept is the output of another's activity.

**enables**: Technology enables System Development. Knowledge enables Technology. This is a capability relationship — one concept makes another possible without fully determining it.

These edge types are first-class concepts in the conceptual graph — the relationships between nodes carry as much meaning as the nodes themselves. Their precise semantics, compositional rules, and constraints on valid usage remain an evolving area. As the node definitions stabilize, the primary source of remaining ambiguity in the graph is migrating from the nodes to the edges, and a dedicated formal treatment (see Unresolved Questions, item 4, and Future Possibilities) may become necessary before the graph can serve as a reliable reasoning tool across multiple RFCs. For now, the definitions above serve as a working taxonomy — sufficient to prevent the most common misreadings, but not yet a complete formalism.

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
**Framework and Architecture** are co-equal aspects of System, not in a parent/child hierarchy. They are related but distinct: Framework defines *what is possible*; Architecture defines *what was chosen*. A framework is a description of a system that defines a design space; architecture applies processes to realize a particular system within that space. Both produce constraints, but of different kinds (domain-level vs. system-level). See the Framework section and the Framework RFC for the full treatment of this relationship, including the Framework-Model distinction, the explicit/implicit framework distinction, and the goal-oriented nature of frameworks.

#### System as Central Node
Every other concept in this RFC exists in relation to a System: architecture is the architecture *of* a system, a framework provides the design space *for* systems, a process occurs *within* a system, technology is knowledge applied *to* systems, a model is a model *of* a system (or of an aspect of reality relevant to a system), and an implementation is an implementation *of* a system's design. This is why System is defined first in this RFC and why it is the node to which the most edges connect.

This centrality reflects two distinct things that should not be conflated:

- **Conceptual centrality**: System is the concept that gives meaning to the others. Without a System to architect, to model, to implement, or to constrain, the other concepts have no object. This is not an artifact of this RFC's organization — it is a feature of the domain itself. Just as "knowledge" and "science" are central nodes in any epistemological model because all reasoning about justification, evidence, and belief presupposes them, "system" is central in any architectural model because all reasoning about design, structure, and process presupposes an entity being designed, structured, or processed.

- **Graph centrality** (as in graph theory): the node with the most edges. System has this property in the conceptual graph, but that is a *consequence* of conceptual centrality, not a cause. Some concepts (Knowledge, Science, Abstraction) are meaningful independently of any particular System — knowledge exists before any system is built using it, and scientific methodology operates on domains far removed from system design. The graph should not be read as implying that nothing exists outside System, only that within this RFC's scope — which is architectural reasoning — System is the entity with respect to which the other concepts are defined.

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
4. Should the edge types themselves (contains, described by, shaped by, constrained by, expressed by, represented by, governed by, realized by, influences, produces, enables) receive a dedicated formal treatment — defining their precise semantics, compositional rules, and constraints on valid usage? As the nodes stabilize, ambiguity is increasingly migrating to the edges; a formal edge-type ontology may become necessary before the conceptual graph can serve as a reliable reasoning tool across multiple RFCs.


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
- Add more words like "pattern", "paradigm", "thinking tools", ...
- A dedicated RFC for **Constraint** as a first-class concept, since both Framework and Architecture depend on it and the distinction between domain-level and system-level constraints may warrant deeper formal treatment.
- A dedicated concept (name to be determined) for "the arrangement of a system's parts" — the composition/assembly concept that Structure explicitly excludes but that Memar has not yet formally named (see Structure > Unresolved Questions).
- A terminology registry that maps each term defined across all Memar RFCs to its definition, its terminology layer, and its relationships to other terms.
- A visual diagram of the conceptual graph suitable for inclusion in onboarding material.
- An **Edge Type Ontology RFC** that formally defines the semantics, compositional rules, and valid-usage constraints for each edge type (contains, described by, shaped by, constrained by, expressed by, represented by, governed by, realized by, influences, produces, enables). As the node definitions stabilize, the primary source of remaining ambiguity in the conceptual graph is the edges — and edge ambiguity is harder to detect than node ambiguity because readers tend to fill in edge semantics from context.
- A dedicated RFC for **Abstraction Validation** — the question of what qualifies a concept to be considered valid at a given level of abstraction. Memar is, in practice, performing this validation implicitly (e.g., distinguishing Architecture from Design, Framework from Library, Structure from Arrangement), but the criteria are not yet formally modeled. Making them explicit would transform Memar from a project that defines terms into a project that also provides a framework for evaluating whether any given term is being used at the appropriate level of specificity for the concept it names.
- A dedicated RFC exploring the concept of **Contributor-as-System** — modeling contributors (human or AI) as Systems whose own Structure (capabilities, limitations, available time, cognitive biases) creates bidirectional influence with the Systems they develop (see System Openness). This is explicitly deferred because it introduces a new conceptual layer that deserves careful, focused treatment rather than compression into an existing RFC.


## Change Rationale

### Initial Version
Introduces foundational definitions for System, Structure, Architecture, Technology, Knowledge, Science, Model, Abstraction, Protocol (by reference), Framework (by reference to RFC 495003), and Implementation. Establishes the conceptual graph — a network of nodes (concepts) and typed edges (relationship types) — that relates these concepts to one another. Positions this RFC as a prerequisite for all subsequent conceptual RFCs in the Memar ecosystem.

The definitions are synthesized from multiple sources — systems theory (von Bertalanffy, Boulding, Checkland), philosophy of technology (Ellul, Mumford, Heidegger), philosophy of science (Popper, Kuhn, Lakatos), and software architecture (ISO/IEC 42010, IEEE 610.12) — with explicit attention to internal consistency and to the Terminology RFC's principles of concept-first thinking, terminological precision, and scientific methodology.

The key architectural decisions in this RFC are:

1. Defining System before other concepts, in a single RFC, to avoid circular dependencies and to anchor the conceptual graph.
2. Defining Technology as applied knowledge rather than as artifacts, to prevent Tool-First Thinking.
3. Including non-computational examples (family, government, lifestyle, discourse, war) to ensure the definitions are maximally general.
4. Presenting the relationships between concepts as a typed graph rather than a linear dependency chain, flat list, or taxonomy — making explicit that the concepts are connected by multiple distinct relationship types (contains, described by, shaped by, constrained by, represented by, etc.) and that no concept is "above" another.
5. Establishing the meta-principle that *some* concepts (Architecture and Framework, considered as ongoing bodies of activity) are themselves Systems, while others (Structure, a single Process, Model) are not — a concept must independently satisfy System's own criteria (interacting elements, boundary, emergence, interdependence) to qualify, not merely be describable as "a collection."
6. Including Knowledge and Science to anchor the epistemic influence dimension of the graph.
7. Defining Structure as the set of capabilities and limitations a System exposes — explicitly distinguishing it from the arrangement of a system's parts, a separate, not-yet-formally-named concept in Memar — and establishing the inseparability of capability and constraint.
8. Distinguishing structural abstraction (imposed by an observing System's own Structure, prior to any purpose) from purposive abstraction (a deliberate choice of what to preserve and discard for a specific goal), and establishing that every account one System has of another is mediated by the observing System's own structural limitations.
9. Distinguishing Framework-as-Aspect (the part of another System's Structure inherited from the framework it was built within) from Framework Considered as a System (an optional, secondary lens applicable to a specific, sufficiently rich framework instance, not a claim built into what "Framework" means) — see item 22 below for the revision that arrived at this final framing.
10. Introducing System Openness (open, closed, isolated) as a property of the relationship between two Systems with respect to a specific channel of influence, capable of changing over time — used to explain bidirectional or reversing influence (e.g., between a contributor and a framework) without requiring every intermediate activity to be modeled as its own System.
11. Correcting an internal contradiction in the initial draft, where Abstraction was stated to be deferred to the Modeling RFC (consistent with Model) but was, in fact, already fully defined in this RFC; Abstraction's full definition remains here.
12. Defining Framework and Architecture as co-equal aspects of System (Constraint Space vs. Decision Space), with a compact treatment here and a full treatment in the dedicated Framework RFC (RFC 495003). Framework is defined as "a description of a system" — an atomic definition whose discriminative power comes from the explanatory structure surrounding it (hypothetical nature, goal-orientation, relationship to Model, explicit/implicit distinction, development framework as specialization).
13. Clarifying that "shapes" in "Architecture shapes a System" does not mean one-way control — the relationship is bidirectional and iterative, consistent with System Openness, and classical-architecture and ISA examples are used to demonstrate this.
14. Refining the Meta-Principle from an unconditional claim ("Architecture and Framework are Systems") to a qualified one ("Architecture and Framework *may themselves be modeled as* Systems when they exhibit the requisite properties"), and making explicit that not every trivially small architecture qualifies.
15. Distinguishing Conceptual Centrality (System gives meaning to the other concepts) from Graph Centrality (System has the most edges), to prevent the misconception that nothing meaningful exists outside System in the conceptual graph.
16. Identifying Edge Types as an emerging topic that may require their own dedicated RFC, as the nodes stabilize and ambiguity migrates to the edges.
17. Updating the "shaped by" edge type definition to explicitly state its bidirectional character at the point of definition (not only in Change Rationale), so that readers who do not read the full Discussion still encounter the correct semantics.
18. Adding an explicit bridge to the Terminology RFC's principle that "terminology shapes mental models" — stating that the purpose of these definitions is not merely semantic consistency but the improvement of mental models used to reason about systems, and that terminology debt is a root cause of architectural debt.
19. Adding a lightweight Edge Taxonomy note immediately after the edge-type definitions, establishing that edge types are first-class concepts whose full formal treatment is deferred but whose working definitions are provided here.
20. Adding an explicit, stated-not-implied legitimacy test for Architecture, using the ISA example as a calibration point: something is Architecture, in Memar's sense, only if it independently exhibits System's own properties at meaningful scale. Explicitly acknowledging that this excludes much of what is commonly labeled "Software Architecture," "Service Architecture," or "Microservice Architecture" in industry usage, and marking the test as a current working criterion rather than a settled classification, pending further testing against a wider range of cases.
21. Correcting a contributor-attribution error: the ISA example was introduced by Omid Hekayati, not Claude; the Conceptual Centrality vs. Graph Centrality distinction and the identification of Edge Types as an emerging topic were raised by ChatGPT in a later review round, not by Claude. Contributor Task entries were corrected accordingly.
22. Correcting a regression: an earlier revision of this RFC treated "Framework as System" as one of two equally valid senses of the word Framework, which contradicted the Framework RFC's atomic definition ("a framework is a description of a system") and a general principle established during the Framework RFC's own revision — that System is never baked into a concept's core definition, but is always, at most, a secondary lens that a sufficiently rich instance of a concept may be examined through (the same pattern already applied to Technology, and to Architecture in the Meta-Principle below). Framework as Aspect remains the RFC's account of how a framework's constraints appear within a built System's Structure; Framework Considered as a System is now presented explicitly as optional and instance-specific, not as a co-equal sense of the word. The "shaped by" edge type definition was similarly softened, for consistency, from an unconditional "Architecture is itself a System" to a hedged reading.
23. Correcting a second contributor-attribution error: the original proposal to reintroduce the open/closed/isolated systems classification (System Openness) came from Omid Hekayati, not Claude. Claude's contribution was expanding that proposal into the full subsection, with the contributor example, the "influences" edge connection, and the note that openness can change over time. Both contributions are now recorded separately.
24. Adding a short definition of Description ("a statement that represents something in words, or more broadly in any symbolic form") at the point where Framework's definition first depends on it, since Framework's definition rests on this term without it having been defined anywhere in Memar's RFCs.
25. Adding "A Note on Systems Thinking" (under How to Read This RFC) to address a recurring source of confusion: that many things, examined loosely, can be called a System, and that this is a normal feature of systems theory rather than a sign of imprecision. The note distinguishes this explanatory-level looseness from the definitional discipline the Meta-Principle enforces, and recommends readers unfamiliar with systems theory or systems thinking read an introductory treatment of the field.
