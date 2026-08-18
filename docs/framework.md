---
Title: "Framework"
Status: Proposed
Start Date: "2026-06-21"
ID: 495003
---

# Framework

## Abstract
A **framework** is a description of a system.

Here, **description** carries its ordinary sense: **a statement that represents something in words** (or, more broadly, in any symbolic form). This document does not treat Description as a specialized technical term requiring its own topic — it is used in the same sense the word carries in general usage, and the discriminative work in this document is done by what is being described (a system) and how (see Model, for the closest related concept, and Framework and Model, below, for how the two differ despite both being kinds of description).

Framework descriptions characteristically exist prior to, and independently from, any specific realization of the system they describe. In Memar's terminology, this property is termed *hypothetical* — meaning "assumed before realization," not "imaginary or unrealizable." A framework does not describe a particular realized system; it defines a space within which multiple systems may be created, understood, or evaluated.

Framework and Architecture are co-equal aspects of a System: Framework defines *what kinds of solutions are allowed*; Architecture defines *which solution was chosen*. Neither is above or below the other. The full treatment of this relationship, including the distinction between domain-level constraints (framework) and system-level constraints (architecture), is provided in the Explanation below.

Memar itself, as a project, is domain-agnostic — it is a framework for developing any system, including software, hardware, buildings, and organizations (see the project [README](../README.md) for that broader identity). This document's own scope is narrower: it describes the framework/architecture relationship in general, and then, in *Memar's Framework: Design Space Over Implementation Layers*, describes what that relationship implies specifically for Memar's software instantiation — the design space for the entire software stack, not just the application layer, but the language, the substrate, and the toolchain. In a conventional software stack, the framework is a tenant living inside a language and an OS, arranging furniture within walls it did not design. In Memar's software instantiation, the framework specifies what those walls must look like: it defines the design space, and the language and OS are implementation choices within that space. This document establishes that stance, explains why it exists, and describes its consequences for every subsequent design decision in that part of the Memar ecosystem.

## Introduction

### Motivation
The word "framework" is one of the most overloaded terms in software engineering. It is used to describe everything from a small routing library to a full application platform, and the ambiguity is not merely linguistic — it leads to architectural confusion. When a team says "we use a framework," it is unclear whether the framework has any authority over the language's type system, the OS's concurrency model, or the deployment topology. In practice, it almost never does. The framework is a tenant in someone else's building, arranging furniture within walls it did not design.

Memar needs the word "framework" to carry a precise, stable meaning because the entire project's coherence depends on it. The definition established in this document and in [System](./system.md) — "a framework is a description of a system" — is deliberately minimal and atomic. The discriminative power of the concept comes not from piling adjectives into the definition, but from the explanatory structure that surrounds it: what a framework describes (a design space, not a particular system), how it differs from related concepts (Model, Specification, Architecture), and what properties it exhibits (hypothetical, goal-oriented, possibly implicit).

Without a clear, authoritative definition, each new document's author will bring their own colloquial understanding of "framework" into the document, and the architectural coherence the project depends on will erode one ambiguous sentence at a time. This document prevents that by establishing the definition once, with rationale, and giving it the authority the project's terminology governance provides (see Document Authority and Terminology Governance, below).

## Explanation

### An Illustrative Analogy: Framework as Floor Plan
Think of the conventional software stack as a building: the hardware is the foundation, the OS is the ground floor, the language runtime sits on top of that, and the framework is an interior designer arranging rooms within whatever floor plan the floors below happened to provide. The framework can rearrange furniture, but it cannot move load-bearing walls, change the plumbing, or expand the footprint. If the ground floor was designed for retail space and the framework needs a warehouse, the framework must either work around the retail layout or accept suboptimal results.

Memar's framework operates differently. Rather than arranging rooms within a pre-existing floor plan, the framework **defines what the floor plan must satisfy**: what kind of activity happens here, what the spatial relationships are, what the load patterns look like, what the failure modes are. The language and the OS then become the structural engineers who receive the framework's design-space requirements and produce a substrate that satisfies them, rather than the other way around. This is not a claim that the framework is "above" architecture — as [System](./system.md) establishes, Framework and Architecture are co-equal aspects of System. It is a claim about *which layer gets to define the design space first*.

Concretely, this means that in the Memar ecosystem, when someone says "the framework requires explicit error handling," this is not a style guideline that developers may follow or ignore. It is a design-space constraint: the language is designed so that error paths are syntactically visible, the runtime is designed so that errors cannot be silently discarded, and the tooling is designed so that violations are caught before they reach production. The framework does not request cooperation from lower layers — it specifies requirements that lower layers must satisfy.

This distinction has practical consequences for every participant in the ecosystem. A developer working on a business feature does not ask "what does Go's error model let me do?" or "what does Linux's syscall interface look like?" They ask "what does the framework's contract require?" and trust that the language and substrate have been designed to make fulfilling that contract natural rather than adversarial. A language binding author does not ask "what Go idioms should I follow?" but "what does the framework require, and how do I express that in Go?" — accepting that some framework requirements may be awkward in a given language, and that this awkwardness is a signal the framework identified, not a problem the framework created.

### Framework as Description
The general definition of Framework is provided in [System](./system.md) as: "a description of a system." This topic expands on that definition, clarifies its properties, and establishes Framework's relationship with Architecture in full detail.

#### The Nature of Framework
A framework is, at its essence, a description. It describes a system — not a particular realized instance, but the space of characteristics, boundaries, and possibilities that define what systems within that space may be. A framework description characteristically exists prior to, and independently from, any specific realization of the system it describes.

In Memar's terminology, this property is termed **hypothetical**. This word requires careful clarification because its colloquial meaning — "imaginary" or "unrealizable" — is misleading in this context. In Memar, *hypothetical* means "assumed before realization": the description exists prior to, and independently from, any specific realization of the system. It does not imply that the described system is imaginary or that it cannot be built. Even a widely realized framework such as Linux retains this property: when Linux is considered as a framework (a sub-framework, per the distinction below), the relevant description is the design space it defines — the space of all systems that may be built within Linux's boundaries — not any particular realized system.

This distinction preserves an important boundary: **Framework ≠ Realized System**. A framework may itself be a realized system (Memar is both a framework and a realized system), but the *descriptive function* of a framework always addresses systems that do not yet exist as specific realizations. This is what distinguishes a framework from a mere documentation of an existing system.

#### Framework Does Not Describe a Particular System
A framework defines a space within which multiple systems may be created. The system that results from using a framework is not the framework; it is a system that was built within the framework's described space.

Architectures make decisions within the possibilities established by the framework, while frameworks do not determine which specific decisions must be made for a particular system. This distinction is fundamental and non-negotiable: a framework defines *what kinds of solutions are allowed*; an architecture defines *which solution was chosen*.

#### The Co-Equal Relationship
Framework and Architecture are not in a hierarchical relationship. They do not form a chain where one is a parent of the other. They are two distinct, co-equal aspects of a System — each answering a fundamentally different question:

- **Framework** answers: *What kinds of solutions are allowed?* It defines the permissible design space — what assumptions may be made, what patterns are required or forbidden, what components are available, and what the boundaries of the design space are. Framework constraints are *domain-level*: they define what is possible within the domain the framework addresses, independent of any particular system.

- **Architecture** answers: *Which solution was chosen, and why?* It defines the concrete realization — what components were selected for this specific system, how they were connected, what trade-offs were accepted, and how specific requirements were satisfied. Architecture constraints are *system-level*: they are limitations that arise from the particular decisions made for a particular system.

```
System
├─ Framework
│    └─ Defines permissible design space (Constraint Space)
│       "What kinds of solutions are allowed?"
│
└─ Architecture
     └─ Defines concrete realization (Decision Space)
        "Which solution was chosen?"
```

#### Two Kinds of Constraints
This co-equal relationship means that a framework's constraints and an architecture's constraints, while both called "constraints," are of fundamentally different kinds:

- A **framework constraint** such as "no hidden control flow" defines the boundary of the design space — it says *no system built within this framework may have hidden control flow*. It exists before any particular system is designed.

- An **architecture constraint** such as "all write operations must go through the event-sourced command bus" defines a specific decision within that space — it says *this particular system chose event sourcing as its write model*. It exists only within the context of a specific system's design.

The residential building example illustrates this concretely: the *framework* might specify that "no dwelling unit may assume a private kitchen" — a design-space constraint that eliminates a category of assumption. The *architecture* then decides that a central kitchen with a meal-ordering system will serve all 100 units — a concrete realization within the space the framework defined. The framework did not choose the central kitchen; it only ensured that the question "should we have private kitchens?" was asked explicitly rather than assumed by default.

#### Framework and Model
A model is a representation of a system. A framework is a description of a system. Both involve describing a system, but the distinction between them is not one of size or level of abstraction — a model can describe something vast (a model of the observable universe is still a model), and a framework can describe something small (a framework with only two admissible design choices is still a framework). The distinction lies instead in **what kind of thing is being described**: a particular instance, or a space of possible instances.

A model describes a *particular* system, or a particular predicted or hypothesized state of one — even when that particular is enormous in scale or scope. A cosmological model describes one universe (the one we are trying to understand), not a class of possible universes; a model of a specific building describes that building, not the class of buildings that could occupy its site. A model is a representation of a *this*, however large the *this* is.

A framework describes a *space* of possible instances, however small that space is. A framework that admits only two valid configurations is still describing a class — "systems that satisfy configuration A or configuration B" — not a particular member of that class. A framework is a representation of a *kind*, not of a *this*, regardless of how many or how few instances the kind actually contains.

This particular-versus-space distinction is what actually does the discriminative work; level of abstraction does not, because both models and frameworks can be produced or read at any level of abstraction. A model provides a simplified, purpose-driven view of a system's structure, behavior, or properties. It is a tool for reasoning: the model stands in for the system for the purpose of understanding or predicting its behavior. A model is *of* a system.

A framework, by contrast, defines a space — a design space — within which systems may be created, understood, or evaluated. A framework is itself a description, and as such, it inherently employs descriptions in forming that definition. Every descriptive statement within a framework constitutes, at some level of abstraction, a model. In this sense, all frameworks employ models, but not all models constitute frameworks. A framework *uses* models; a model *is* a representation.

This means the relationship between Framework and Model is not one of containment or hierarchy. A framework is not "a collection of models." It is a description whose internal composition may include models, but whose essence — its purpose and function — is distinct from any individual model it contains. A model describes what a system *is* (or what it is *predicted to be*); a framework describes what systems *may be* within a defined space.

#### Explicit and Implicit Frameworks
A framework may be explicit — formally documented in written specifications, documents, or design records — or it may be implicit, emerging from the accumulated decisions, conventions, and design choices of a system without ever being formally codified as a description.

Linux's "everything is a file" principle is an example of an implicit framework element. This principle is not merely a documentation convention — it shapes the design space of every system built on Linux. A developer building on Linux may not have read any document that states "everything is a file," yet their architectural decisions are constrained by it: the assumption influences how they model I/O, how they design security boundaries, and how they reason about system resources. The principle functions as a framework element — it defines part of the design space — whether or not it is explicitly documented.

From a systems-theory perspective, the distinction between explicit and implicit frameworks is not a difference in kind but in accessibility. What matters is whether the framework's description produces observable effects on the systems built within its scope. A formally documented framework whose constraints are routinely ignored is, in practice, less of a framework than an undocumented one whose conventions are consistently followed. The `constrained_by` edge in [System](./system.md)'s conceptual graph captures this: what constrains a system is the framework's actual influence on that system's Structure, not the framework's documentation status.

This influence is best understood as Framework-as-Aspect: Linux's "everything is a file" principle does not merely constrain systems built on Linux from outside — it becomes part of those systems' own Structure, shaping what capabilities and constraints they expose to their users. This does not require asserting that Linux itself is a System in order to make sense; the aspect relationship holds regardless of whether Linux, considered on its own terms, independently qualifies as a System by the criteria [System](./system.md) establishes (see System → Framework as Aspect, and Framework Considered as a System). System-hood, where it applies to a particular framework, is a secondary fact about that framework, not a precondition for the framework to constrain the systems built within it.

#### Framework and Development Framework
The word "framework" covers a general concept. A **development framework** is a specialization: a framework whose described system is specifically intended to guide the development of other systems.

Linux, as a sub-framework, is a framework: it describes a design space for operating-system-level capabilities. When it is used to guide the development of applications, it functions as a development framework. But a framework can also describe a system without being oriented toward development — Classical Architecture, for example, describes a design space for buildings without itself being a development methodology.

The distinction matters because not every property of development frameworks applies to frameworks in general. Goal-orientation (see below), for instance, is particularly salient for development frameworks: a development framework should have explicit goals for the systems it intends to help develop, and those goals should be specific enough that different readers would not arrive at incompatible interpretations. A non-development framework may be less explicitly goal-oriented, though it still shapes a design space.

In colloquial usage, "framework" almost always means "development framework." This document acknowledges the colloquial usage while maintaining the terminological distinction: when the broader concept is intended, "framework" is used; when the specialization is intended, "development framework" is used. Future documents should follow this convention.

#### Goal-Oriented Frameworks and Purpose Space
Frameworks are not merely constraint spaces. They are also **purpose spaces** — they exist toward one or more goals, and those goals shape the design space the framework defines.

A framework that defines a design space for 100-unit residential buildings might have goals such as "optimize for communal living" or "minimize per-unit construction cost." These goals are not decorative — they determine which constraints are imposed and which capabilities are enabled. A framework oriented toward communal living will define a different design space than one oriented toward privacy maximization, even if both address the same nominal problem domain (100-unit residential buildings).

This goal-orientation is particularly important for **development frameworks**. A development framework should state its goals explicitly, and those goals should be specific enough that different readers arrive at compatible interpretations. A goal stated as "provide a healthy lifestyle for residents" is too ambiguous — different readers will interpret "healthy lifestyle" differently, producing incompatible architectural decisions. A goal stated as "ensure every dwelling unit has access to natural light and ventilation without requiring mechanical systems" is specific enough to constrain the design space meaningfully.

A further consistency requirement applies: a development framework's goals should be achievable both by the systems developed within it *and* by the framework's own development processes. A framework that claims to provide "the fastest method for executing ideas" but itself is developed using slow, cumbersome processes fails this consistency test. Similarly, a framework that advocates graph-based modeling but itself relies on traditional table-centric design methods contradicts its own stated approach.

A framework constraint does not only rule things out — it can also force a *prior* process into existence that would not otherwise have been necessary. Consider a framework constraint such as **"no aspect of the design space may be assumed by default; every assumption must be the outcome of an explicit decision."** Applied to the 100-unit residential example, this constraint means that the question "should each unit have a private kitchen?" cannot simply be decided at the architecture stage by habit or convention — because a habitual answer is, by definition, an unexamined default. The constraint forces an *upstream* process to happen first: a detailed, explicit description of the residents' intended lifestyle, specific enough that the private-kitchen question (and others like it) can be evaluated against it rather than assumed. The framework did not answer the kitchen question, and it did not perform the lifestyle-description process itself — but by refusing to let the question go unexamined, it made that upstream process necessary in a way it otherwise would not have been. This is a second, distinct way a framework's Purpose Space shapes what happens before Architecture makes its decisions: not only by stating goals directly, but by imposing constraints whose only way of being satisfied is the prior existence of a clarifying process.

The relationship between a framework's goals and its design space is not yet fully formalized in Memar; see Unresolved questions below.

#### Framework vs. Library vs. Toolkit
A library provides specific functionality that a system can use. A toolkit provides a collection of tools for specific tasks. A framework provides a structure within which a system is built. The distinction is one of control: a library is called by the system it serves; a framework calls the system that serves it. This is often described as the "inversion of control" principle. In practice, the distinction is not always sharp — many frameworks include libraries, and many libraries have framework-like conventions — but the conceptual distinction matters because it affects how the developer reasons about the relationship between their code and the framework's code.

Frameworks occupy an intermediate position in the concept hierarchy. They are more concrete than abstractions or models — they provide actual structure that can be used — but less concrete than implementations — they do not specify every detail of the resulting system. A web application framework provides the conventions and components for building web applications, but does not specify what any particular web application does. Memar itself is a framework: it provides the conventions, constraints, and components for building software systems according to Memar's architectural principles, but it does not specify what any particular system built with Memar does.

#### Discussion

##### Drawbacks
Frameworks can constrain architectural freedom by imposing structure that may not be optimal for every system. A developer who uses a framework may unconsciously accept architectural decisions that the framework makes implicitly, treating them as inevitable rather than as choices that could have been made differently. Memar mitigates this risk by making its own architectural decisions explicit and by encouraging contributors to understand *why* each constraint exists, not merely *that* it exists.

The co-equal relationship between Framework and Architecture introduces a terminological risk: because both use the word "constraint," readers may conflate the two types. Memar mitigates this by distinguishing them as *domain-level* constraints (framework) versus *system-level* constraints (architecture), and by ensuring that the dependency chain in [System](./system.md)'s Relationships topic makes their distinct roles clear.

##### Rationale and alternatives
- **Provide guidelines rather than a framework (rejected).** Guidelines lack the structural enforcement that a framework provides. Without concrete constraints, conventions, and components, different contributors will make incompatible choices, and the coherence of the resulting systems will suffer.
- **Position Framework as a subset or parent of Architecture (rejected).** Making one subordinate to the other implies a hierarchy that does not exist. Framework and Architecture address different questions — permissible design space vs. concrete realization — and neither contains the other. A system has both a framework (or operates within one) and an architecture; they coexist as parallel, co-dependent aspects of the system.

##### Prior art
The concept of a software framework is well-established in the literature (Johnson and Foote, "Designing Reusable Classes," 1988; Fayad and Schmidt, "Object-Oriented Application Frameworks," 1997). The distinction between framework and library is discussed in Gamma et al. ("Design Patterns," 1994).

##### Unresolved questions
1. How should Memar balance the need for framework-level constraints with the need for architectural flexibility?
2. Should Memar define a formal extension mechanism for cases where the framework's constraints are genuinely inappropriate for a specific system?
3. Should the Framework-as-Aspect relationship be relabeled as a distinct edge type (e.g., `constrains` rather than `is an aspect of`), to more precisely capture that a Framework does not become a part of a System but rather constrains a System's Structure from outside? The current "aspect" framing captures the structural consequence (the Framework's constraints appear *within* the System's Structure) but may be misread as implying that the Framework itself is *inside* the System. A future revision should evaluate whether the edge-type language from [System](./system.md)'s conceptual graph provides a more precise framing.
4. Should a framework's goals be formalized as a named section within the framework's description, or is an informal statement sufficient?
5. How should conflicts between a framework's goals be resolved when they pull in different directions (e.g., "minimize cost" vs. "maximize resilience")?
6. Should the Purpose Space / Constraint Space distinction be reflected in [System](./system.md)'s conceptual graph as two distinct edge types, or is the current single `constrained_by` edge sufficient?
7. How does the goal-orientation of a framework relate to System's Purpose and to System's newly-added Responsibility (a part's Purpose expressed relative to a containing System — see [System → Responsibility](./system.md#system))? Is a framework's goal the same as a System's purpose, is it closer to a Responsibility, or is there a meaningful distinction from both? This document does not yet check its own use of "goal" against either definition.

##### Future possibilities
- A dedicated document or section that formalizes the relationship between a framework's stated goals and the design space it produces — potentially including a notation for expressing framework goals and a method for evaluating whether a given design space is consistent with its stated goals.
- Integration with the Terminology Governance mechanism (see Document Authority and Terminology Governance below) to ensure that a framework's goals are treated as authoritative definitions within the Memar ecosystem.
- A dedicated **Sub-Framework document** that formally defines the boundary between frameworks and sub-frameworks, provides evaluation criteria, and assesses common industry systems against those criteria. This would be particularly valuable for contributors who need to understand whether adopting an external system introduces sub-framework-level gaps into their design space.

### Framework and Sub-Framework
The distinction between a framework and a sub-framework is not about size, popularity, or the number of features it provides. It is about **completeness of guidance for a development domain** — or, to put it differently, about the degree of *silence* a framework leaves for the developer.

#### What Is a Sub-Framework?
A **sub-framework** is a system that provides structural guidance within a specific, bounded area of development, but that does not cover the full breadth of decisions a developer must make to produce a complete system. Using a sub-framework, the developer will regularly encounter questions that the sub-framework does not answer — and must therefore turn to other sub-frameworks, external documentation, or personal judgment to fill the gaps.

The practical consequence of this is that sub-frameworks rarely operate in isolation. A real-world software stack typically combines several sub-frameworks, each covering a different slice of the development space. The resulting system's Structure is shaped not by a single, coherent design philosophy, but by the often-incompatible assumptions of multiple sub-frameworks that were never designed to work together. This is the root cause of many integration difficulties in conventional software development: when two sub-frameworks make incompatible assumptions about error handling, state management, or concurrency, the developer must write glue code — ad-hoc Structure that exists solely to bridge gaps between sub-frameworks that neither anticipated the other.

Examples of systems that are sub-frameworks by this definition:

- **Linux** (as a development substrate): it provides constraints and capabilities for process management, file I/O, and system calls, but it does not guide how a developer should design an application's architecture, model its domain, or structure its communication patterns. A language or runtime built on Linux inherits Linux's constraints (e.g., the "everything is a file" principle becomes part of the system's Structure), but Linux does not specify how that language should be designed. Linux is a sub-framework because it leaves significant areas of the development space silent.
- **POSIX**: a subset of Linux's interface, defining portable operating-system interfaces. It is even more clearly a sub-framework — it constrains what system calls look like but says nothing about application architecture, data modeling, or deployment.
- **SQL**: provides a structured way to query and manipulate relational data, but does not address application structure, communication patterns, or error handling beyond the database boundary.
- **HTTP**: defines how messages are structured and exchanged between network endpoints, but does not specify how a system using HTTP should be internally organized.
- **Spring, Angular, .NET**: in conventional industry terminology, these are called "frameworks," but under this document's definition, each covers a specific layer of the stack (application structure, UI componentry, runtime environment) and requires the developer to make fundamental decisions outside its scope. They are sub-frameworks: valuable, widely used, but incomplete as guides for full system development.

#### What Makes a Framework Complete?
A **framework**, as distinct from a sub-framework, is a system that provides sufficient guidance for a developer to build a complete system within its domain without routinely needing to go outside the framework for fundamental decisions. This does not mean the framework makes every decision for the developer — it means the framework defines the *space* within which those decisions are made, and provides enough structure that the developer's attention stays on domain-specific problems rather than on foundational questions the framework should have already settled.

The key metric is the degree of silence: a framework that leaves large, recurring areas of silence — areas where the developer must independently resolve questions that the framework should have anticipated — is, by that measure, a sub-framework. A framework that minimizes silence, so that the developer's effort is spent on the unique problems of their specific system rather than on bridging gaps between incompatible sub-frameworks, is closer to what this document means by "framework."

Memar aspires to be a framework in this full sense — not merely a sub-framework for building software, but a framework for building *any* system, including the transfer of processes from the real world to the virtual world. Whether it achieves this is a question for its own architectural evaluation, not for this definitional topic. The aspiration, however, is what distinguishes Memar's self-conception from the self-conception of a sub-framework.

#### Terminology Caveat
In current industry usage, the word "framework" is applied to both complete frameworks and sub-frameworks without distinction. Spring, Angular, and .NET are universally called "frameworks," and calling them "sub-frameworks" will feel unfamiliar or even dismissive to many developers. This document is not claiming that these systems are poorly designed or unimportant. It is making a structural claim: by the definition established in this document and in [System](./system.md), these systems cover a bounded slice of the development space and do not provide complete guidance for building a system. The structural claim is independent of the quality of the systems themselves.

This is an instance of a broader pattern [System](./system.md) identifies: common industry terminology often conflates distinct concepts, and Memar's definitions may intentionally diverge from common usage when common usage is ambiguous, inconsistent, or misleading. The divergence should be acknowledged explicitly — which this paragraph does — rather than left for the reader to discover through confusion.

#### Discussion

##### Drawbacks
The framework/sub-framework distinction introduces a terminological cost. Every existing system called a "framework" in the industry must now be re-evaluated: is it a framework or a sub-framework? This re-evaluation is labor-intensive and may be perceived as gatekeeping — as Memar declaring that most of the industry's "frameworks" are not "real" frameworks. The mitigation is the same as for all of Memar's terminological divergences: the distinction exists because it captures a real structural difference that affects how systems are built, and the cost of not making the distinction (silent gaps in guidance, integration friction between incompatible sub-frameworks) is higher than the cost of the unfamiliar terminology.

##### Unresolved questions
1. Should the framework/sub-framework distinction be formalized as a labeled property on the `constrained_by` edge in [System](./system.md)'s conceptual graph, so that documents can state explicitly whether a given `constrained_by` relationship involves a framework or a sub-framework?
2. Is there a useful intermediate category between "framework" and "sub-framework" — a system that is more complete than a typical sub-framework but not as comprehensive as a full framework?
3. Should this distinction receive its own dedicated document, given that it has practical implications for how Memar evaluates and integrates with external systems?

##### Future possibilities
- A dedicated **Sub-Framework document** that formally defines the boundary between frameworks and sub-frameworks, provides evaluation criteria, and assesses common industry systems against those criteria. This would be particularly valuable for contributors who need to understand whether adopting an external system introduces sub-framework-level gaps into their design space.

### Memar's Framework: Design Space Over Implementation Layers
The preceding topic establishes the general nature of Framework and its co-equal relationship with Architecture. This topic describes how that general definition applies specifically to Memar's **Computer** system category — the software-implementation instantiation of Memar, as distinguished from Memar's other, non-software system categories in the project [README](../README.md). Memar's identity as a project is not software-specific: it is meant for developing any system — technology, software, hardware, apps, gadgets, buildings, organizations and society, and more. What follows is scoped to the software case; a parallel topic for Memar's other system categories, if and when they reach the same level of detail, belongs alongside this one rather than folded into it.

The conventional hierarchy in software development places the framework as a guest living inside a language and operating system — the language defines what is expressible, the OS defines what is executable, and the framework merely organizes how developers use both. Memar's position is different: the framework **defines the design space** that the language and the operating system must satisfy. The language and the OS are components whose design assumptions are themselves shaped by the framework's constraints, not the other way around.

The deeper problem with the conventional model is that the layers were never designed with each other in mind at the architectural level. A language is typically designed to be OS-agnostic and framework-agnostic. An OS is typically designed to be language-agnostic. A framework, arriving last, is left to patch the gaps between whatever assumptions the first two happened to make independently. The result is a stack of layers that each hide complexity from the layer above — and where each layer's hidden complexity eventually leaks upward as surprising constraints, performance cliffs, or security surfaces.

Memar's position is that this ordering is historical accident, not architectural necessity. A framework that defines its design space first — and then specifies what language and OS behavior it needs to support that space — can maintain coherence across all three layers rather than inheriting incoherence from two independent prior decisions. When a framework is subordinate to a language and an OS, it inherits every assumption those layers baked in — often assumptions made decades ago for very different hardware, scale, and application models. A framework built inside Go must accept Go's concurrency model, Go's memory model, and Go's standard library conventions. A framework built on Linux must accept POSIX's process/thread model, its I/O abstractions, and its general-purpose kernel interface. These inherited assumptions are invisible until they become constraints, at which point they are very expensive to remove.

In Memar's model, a developer working on a business feature does not think about "which OS API to call" or "which language runtime to trust." They think about the domain model and the framework's contracts. The OS and the language are implementation details of those contracts — present, but not surfaced. This is the same thinking behind Unikernel architectures, where the application and the OS are compiled together into a single artifact with no general-purpose kernel in between: the application does not "call the OS," it is co-designed with the minimal substrate it actually needs.

#### Practical Implications
- The Khayyam language is not "Memar's language" in the sense that Memar is a framework for Khayyam. Khayyam is a language whose design assumptions are specified by Memar's design space, so that code written in Khayyam already expresses the constraints Memar cares about — explicit state, explicit error paths, no hidden control flow, no invisible allocations.
- An OS running Memar applications is not a general-purpose OS that Memar happens to run on. It is a substrate whose interface is defined by what Memar actually needs — no more. In a fully realized deployment, this means a Unikernel or Exokernel model, not a POSIX kernel offering thousands of syscalls that the application will never use.
- Memar is implemented as libraries across multiple languages and runtimes, at different levels of completeness: a Go implementation (`memar-go`) that has been production-tested in a real business deployment; a JavaScript implementation covering select subsystems only (error handling, services) with no current timeline for further completion; a Rust implementation not yet started, with its repository reserved for future work contingent on additional contributor capacity; and Khayyam itself, still under active design. Defining the design space at the framework level does not require every language binding to be complete or even started — it means Memar's design principles are the starting point that any such binding must conform to, whenever and to whatever extent it is undertaken.

This stance has no syntax or grammar implications — it is a principle that shapes the design decisions made in every subsequent document. Specifically, it is the reason why control flow keywords, memory management, concurrency primitives, and standard library shapes are not baked into the Khayyam language itself but instead live in the Memar framework, why the framework's recommended toolchain (compiler, linter, scaffolding) is designed as a coherent unit rather than as independent tools that happen to be compatible, and why constraints (e.g. "no hidden state," "every error path must be visible") are expressed as framework-level contracts rather than as optional conventions.

#### Discussion

##### Drawbacks
Inverting the conventional layer ordering does not make Memar incompatible with existing languages and operating systems — a Go implementation has been built and production-tested in a real business context, and partial implementations exist in other languages. However, this cost is not merely a one-time adaptation friction: a concrete instance already occurred in `memar-go`, where introducing Go generics into an already-working, production-tested implementation produced widespread breakage that, after being deferred for roughly two years, was determined to be unresolvable within Go's generics model rather than merely time-consuming to fix. This is cited as direct evidence for the document's core claim — that friction from implementing framework design-space constraints atop a language with different assumptions compounds over time rather than being paid once — rather than a hypothetical risk. (This event is not yet recorded as a linkable document in this project's own documentation system; see Unresolved questions at the end of this document.)

##### Rationale and alternatives
The conventional model (framework lives inside language and OS) was rejected because it guarantees that the framework will eventually be constrained by assumptions it did not make and cannot change. The cost of that constraint compounds over time — each new capability the framework needs must be negotiated against what the language and OS already decided, rather than being specified from first principles. Memar's approach accepts a higher initial cost (no incremental adoption, no reuse of existing language/OS tooling without design review) in exchange for eliminating that compounding constraint cost.

##### Prior art
- **Unikernel projects** (MirageOS, IncludeOS, Nanos): the closest architectural parallel, specifically in their treatment of the OS as a consequence of the application's requirements rather than a given substrate.
- **Singularity (Microsoft Research)**: an OS research project that co-designed the language (Sing#) and the OS from shared first principles, rather than fitting a language onto an existing OS.
- **Erlang/BEAM**: a language+runtime that is, in practice, its own OS-like substrate — the BEAM VM defines process scheduling, memory isolation, and fault tolerance in ways that make the underlying OS largely irrelevant to application code.
- **General-purpose OS + framework combinations** (Spring Boot on JVM on Linux, Rails on Ruby on Linux): the conventional prior art being explicitly rejected, not because they are bad engineering for their context, but because their inherited-assumption problem is well-documented and the cost of navigating it is visible in every large codebase that has lived long enough.

##### Unresolved questions
None specific to this topic.

##### Future possibilities
- **Minimal OS Interface Specification:** A formal specification of the minimal OS interface Memar applications actually require (the boundary between "what the framework's design space requires from a substrate" and "what a substrate provides") would be the natural follow-up to this topic at the OS-design layer.

### Document Authority and Terminology Governance
Memar documents are the authoritative source for the terms they define, and this governs how "framework," "architecture," and every other term this document uses are meant to be read. The general principle — a document's Definition takes precedence over colloquial usage once established, how that authority is established and maintained, and its consequences for AI systems working within Memar (Word-Weight Rebalancing) — is stated once, in full, in [Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance) and [Terminology → Word-Weight Rebalancing](./terminology.md#word-weight-rebalancing), rather than restated here. The [Protocol document](./protocol.md) remains the clearest existing example of a Definition built to that standard.

## Results

## Discussion

### Unresolved questions
1. The [memar-go generics elimination] event cited under *Memar's Framework* as evidence has no linkable document in this project's own documentation system yet — it is described in prose only. If this event is meant to stand as citable evidence for the document's core claim, it may deserve its own short record (in `memar-go`'s own changelog, or referenced from there) rather than remaining a parenthetical description here.
2. *Memar's Framework: Design Space Over Implementation Layers* now scopes itself explicitly to Memar's Computer (software) system category, per the project README's System Categories. Memar's other, non-software system categories do not yet have a comparable design-space treatment anywhere. Whether they need one, and if so whether it belongs in this document as a sibling topic or somewhere else entirely, is open.
3. The [Protocol document](./protocol.md) reference under *Document Authority and Terminology Governance* previously carried an explicit identifier ("RFC 495465") in this document's prose. That identifier is not repeated here, since a document's identifier is assigned at creation and is not a stable citation form on its own — but if a stable way to cite a specific document's current identity is needed (beyond a relative link, which can go stale if a file is renamed), that is an open question for the documentation system generally, not specific to Framework.

### Future possibilities
See the Future possibilities subsections under each Explanation topic above.
