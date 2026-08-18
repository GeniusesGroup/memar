---
Title: "Modularity"
Status: Draft
Start Date: "2026-08-15"
ID: 496333
---

# Modularity

## Abstract
Modularity is the organization of a System into independently meaningful Modules with explicit boundaries, responsibilities, and relationships. A Module is itself a System: it has a [Structure](./system.md#structure) — capabilities and constraints — may contain Concepts, Processes, Structures, and other Modules, and interacts with other Modules through explicit relationships rather than through uncontrolled knowledge of their internals.

Modularity is therefore not a property of source files, directories, packages, processes, servers, repositories, containers, or deployment units. Those may represent or host Modules, but none defines what a Module is. A system may be externally perceived as one integrated system while being internally composed of many independent Modules. Conversely, a system may be distributed across many processes or services while still being poorly modularized.

A Module should preserve a coherent responsibility and a stable identity while allowing independently evolving behavior to be attached where the model requires it. Optional Modules are one important form of this extensibility: they may enrich or constrain the behavior of a Module without becoming part of the latter's essential identity. Such Modules may be invoked through existing service requests and responses and, where appropriate, through event-target capabilities already present in the participating Types or Modules. These capabilities do not require introducing a new data model merely because the interaction is described as an Event.

## Introduction

### Motivation
The term *module* is used throughout architecture, programming languages, organizational design, and systems engineering, but its common technical usage is often tied to a particular implementation mechanism. A module may be identified with a package, a directory, a library, a project, a service, a container, or another deployment artifact. These representations are useful, but treating any one of them as the definition of a Module makes the model dependent on the current technology.

Memar requires a more stable concept because Modules appear across many of its other concepts. Modeling needs to determine when behavior belongs to an independently modeled unit rather than being absorbed into another Concept. Protocols need to describe how Modules can interact. Khayyam needs a language-level representation of modularity without allowing file layout, package management, or distribution mechanisms to define the concept itself. Process needs to distinguish behavioral progression from structural boundaries.

The absence of a dedicated definition also causes related ideas such as Rules, Plugins, Events, Packages, Services, and Microservices to be treated as if they were interchangeable with Modules. They are not. A Module is a structural concept; other terms may describe a relationship, capability, mechanism, representation, or deployment arrangement.

This document therefore establishes the conceptual meaning of Modularity and the boundary between Module and the mechanisms commonly used to represent or extend one.

### Methodology
The definition begins from System rather than from programming-language constructs. A Module is examined as a System with a bounded responsibility and explicit relationships to other Systems. Its properties are derived from what such a boundary must accomplish rather than from the terminology or conventions of a particular software ecosystem.

The discussion deliberately distinguishes:

- Concept from representation;
- Module from deployment unit;
- Module from Type;
- Module from Protocol;
- Module from Rule or other domain-specific mechanisms;
- Event as a capability and interaction pattern from Event as a separate data model;
- essential structure from optional extension.

Examples are used to expose distinctions, not to prescribe a universal domain model. A domain example must therefore not be read as asserting that the named concepts or relationships are mandatory in every implementation.

## Explanation

### Module as a System
A Module is a System that provides a coherent structural boundary around capabilities or responsibilities.

Because a Module is a System, the definition of System applies to it. A Module can therefore have its own Concepts, Structures, Processes, Models, Protocols, and relationships. It may itself contain other Modules. Its boundary is meaningful because it determines what belongs to the responsibility of that Module and what is related to it from outside.

The word *module* does not imply a particular physical size. A Module may be represented by a small amount of implementation or by a substantial body of implementation. Size is not the criterion; coherent responsibility and meaningful independence are.

A Module also does not imply isolation. A useful Module is normally part of a larger System and therefore participates in relationships with other Modules. Independence means that the Module retains its own identity and responsibility across those relationships, not that it must operate as a closed system.

#### Module and System
A Module is a System considered under a modular boundary.

This does not mean that every System is automatically a Module. Calling a System a Module asserts an architectural role: the System is being treated as a bounded part of a larger System whose responsibility can remain meaningful independently of the surrounding parts.

The same concrete System can be considered at different levels. A complete organization may be considered as one System, while its accounting capability, sales capability, or other bounded responsibility may be considered as Modules within that System. The choice must follow the relationships and responsibilities being modeled rather than the physical deployment structure.

### Module Identity and Responsibility
A Module is not defined by the list of features currently requested by its consumers.

Its identity comes from its Responsibility — in the sense defined at [System → Responsibility](./system.md#system): its Purpose expressed relative to the larger System that contains it — and the capabilities and constraints it exposes and enforces. New behavior should therefore be added to a Module only when that behavior belongs to the Responsibility that gives the Module its identity.

This distinction is essential for long-lived systems. A stable Module should not continuously change its internal model merely because a new organization, consumer, policy, or contextual variation asks for a different behavior. If the new behavior represents an independent Responsibility, it should be modeled independently and related to the original Module.

This does not imply that every variation must become a separate Module. Creating boundaries has a cost. Whether a variation has enough independent meaning, Responsibility, lifecycle, or evolution to justify its own boundary is not something a Module boundary can settle by being declared — see [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) for what can actually be checked, and [Process → Modeling and Observation Form a Cycle](./process.md#modeling-and-observation-form-a-cycle-not-two-separated-phases) for why this is typically discovered by proposing a boundary and then observing whether it holds, rather than decided correctly in one step. `modeling.md`'s own [Domain Decomposition over Aggregate-Root Modeling](./modeling.md#domain-decomposition-over-aggregate-root-modeling) walks through exactly this cycle for a `username` field originally modeled inside `User`.

#### Type and Module
Type and Module may both use abstraction and encapsulation, but they answer different questions.

A Type defines a kind of thing and the structure or behavior associated with that kind. A Module defines a bounded unit of responsibility within a larger System.

A Module may contain Types, and a Type may participate in the representation of a Module. Neither relationship makes the two concepts interchangeable. Encapsulation and abstraction are general principles that may apply to both; they are not evidence that Type and Module have the same identity.

### Core Structure and Optional Modules
Not every Module has the same role in a particular System.

Some Modules participate in the structure that the System's purpose depends upon. Removing one of them may mean that the resulting System no longer represents the same intended System. Other Modules are optional: removing them may change valuable behavior while leaving the essential purpose and identity of the larger System intact.

This distinction is relative to the System and its purpose. A Module is not inherently mandatory or optional in isolation.

An Optional Module is therefore a Module whose presence is not required for the essential structure of a particular System, while its presence may add, refine, constrain, or otherwise affect the behavior of that System or of another Module.

The distinction should not be confused with physical optionality in a package manager or configuration file. An implementation may make a component technically mandatory even when the conceptual Module is optional, or technically optional even when the conceptual Module is structurally essential.

#### Example: Pricing and Invoice Behavior
Consider a system that records the sale of a Product and produces an Invoice.

Pricing behavior may belong to a Module associated with the Product. The price of a service need not be a fixed value. A transportation service, for example, may have pricing behavior that depends on location, time, route, demand, or other conditions. These may be represented by independently evolving Modules without changing the identity of the Product itself.

An Invoice may then have its own optional Modules that affect the amount payable at the Invoice level. A discount applied to an Invoice does not imply that the underlying Product's price became zero. The Product's pricing and the Invoice's final amount are different concerns at different levels of the model.

This distinction prevents an extension at one level from being incorrectly modeled as a modification of a concept at another level.

### Pluggable Behavior
A Module may expose relationships through which independently modeled Modules can attach behavior to it.

The purpose of such a boundary is not to predict every future extension. It is to allow a stable Module to remain stable while new behavior can be modeled independently when that behavior does not belong to the Module's essential responsibility.

This is the general principle behind the modeling rule that extensible behavior belongs to pluggable Modules. A discount mechanism, for example, need not cause the Invoice model to acquire a new field or branch for every possible discount policy. The Invoice can expose an appropriate relationship, while the independently modeled Module carries its own Concepts, rules, and behavior.

The same principle can apply outside software. A legal system may have a stable constitutional structure while later laws add behavior within the authority permitted by that structure. An organization may have stable institutional responsibilities while optional policies or programs extend how those responsibilities are carried out. The analogy does not make these domains identical; it illustrates the same structural distinction between a stable boundary and independently evolving additions.

#### Pluggable Does Not Mean Plugin
*Pluggable Module* describes an architectural relationship, not necessarily a plugin mechanism.

A Module may be pluggable even when its implementation is compiled into the same artifact, stored in the same repository, or deployed together with the Module to which it relates. Conversely, a dynamically loaded plugin is not necessarily a well-designed Module merely because it can be loaded dynamically.

The architectural question is whether the added behavior has an independent conceptual boundary and can attach through an explicit relationship. The loading, linking, packaging, or deployment mechanism is a separate concern.

### Rules as a Provisional Term
The term *Rule* is commonly used for many different concepts. In software ecosystems it often refers to a conditional expression, a validation predicate, a policy object, or a component executed by a Rule Engine. None of these meanings is sufficient to define the architectural concept under discussion here.

In the modularity model, what has informally been called a Rule may itself be a Module with an optional relationship to another Module. Its distinguishing characteristic is not that it contains an `if` statement or that it is processed by a Rule Engine. It is that the behavior it represents can be attached to an existing Module without becoming part of that Module's essential identity.

The term remains provisional because the project has not yet established that *Rule* is the best name for this role. The architectural property must therefore not depend on the word. A future terminology document may replace it without changing the underlying model.

#### Scope Matters
An extension can act at different levels without becoming the same behavior.

For example:

- a pricing Module can determine the price of a Product or service;
- an Invoice-level Module can alter the amount payable on an Invoice;
- another Module may validate whether a proposed service can be included in an Invoice;
- another may prevent a status transition when a condition is not satisfied.

These behaviors may all be optional Modules, but they do not become one concern merely because they can affect a final outcome. Their boundaries are determined by the Module to which their responsibility relates.

This distinction is particularly important for financial and commercial models. A field such as `discount` on an Invoice may incorrectly collapse a potentially independent family of behaviors into one representation. A model should instead preserve the distinctions that actually exist in the domain.

### Event as a Module Capability
An Event is not necessarily a new data model introduced solely to notify other Modules.

A Type or Module may choose to expose an EventTarget capability. EventTarget indicates that other participants may be able to subscribe to a defined occurrence involving that Type or Module, according to the applicable contract.

The capability belongs to the Type or Module that exposes it. It does not require creating a separate conceptual model for every event.

This preserves the distinction between:

- the thing whose occurrence is relevant;
- the service request or response that carries the relevant data;
- and the communication pattern through which interested participants are informed.

Existing service request and response models can therefore be sufficient for event-related interaction when the domain does not require another distinct concept. The fact that a request is delivered because an event occurred does not, by itself, justify introducing an Event DTO or another parallel data structure.

#### Example: Validating an Invoice Transition
Suppose an Invoice is about to change status and the Invoice exposes an appropriate event-target capability around that transition.

An Optional Module responsible for transportation constraints may receive the relevant request or notification and determine that the selected transportation service cannot be used for the goods in the Invoice. The Module can report the violation before the transition is finalized, preventing the Invoice from reaching the invalid state.

The Invoice model does not need to acquire a new field or branch for every organization-specific transportation rule. The Optional Module remains independently modeled and can be replaced, extended, or omitted according to the System's requirements.

The example does not prescribe a particular event broker, queue, callback mechanism, or programming construct. Those are implementation mechanisms whose suitability depends on the actual Process and System constraints.

### Module, Process, and Protocol
Module, Process, and Protocol describe different dimensions: a Module provides a structural boundary for capabilities or responsibilities; a Process describes progression, interaction, and change; a Protocol describes declarative rules that govern one or more Processes within a System — see [Protocol](./protocol.md#what-is-a-protocol) for the full chain (System contains Processes, governed by Protocols). None of these should be substituted for another merely because a particular implementation represents them using the same programming construct.

The Module-specific consequence is this document's own to state: a Module boundary is not automatically a Process boundary, and a Process is not automatically bounded by any single Module — the same Process may cross several Modules, and the same Module may contain or participate in many Processes. [Process → Process and Boundary](./process.md#process-and-boundary) and [Process → Process Composition](./process.md#process-composition) give the fuller, Process-side treatment of why an implementation boundary (module, function, service, deployment unit) must not be assumed to coincide with a Process boundary; this document does not restate that reasoning, only the corresponding claim from Module's own side.

### Module Among Related Concepts
Module shares tools such as abstraction and encapsulation with several other Memar concepts, which is precisely why its boundary needs to be stated plainly rather than left to be inferred. The table below is a quick-reference summary of distinctions already made in this document and in the documents of the other concepts named; it does not introduce new definitions, does not establish a hierarchy among the rows, and is not a substitute for reading each concept's own document.

| Concept | What It Defines |
| --- | --- |
| Abstraction | The degree to which internal detail is exposed or hidden |
| Encapsulation | The boundary of access to a System's internal state and behavior |
| Type | A kind of thing and the structure or behavior associated with that kind |
| Structure | The capabilities and constraints a System exposes and enforces |
| Responsibility | A part's Purpose expressed relative to the larger System containing it |
| Protocol | Declarative rules that govern one or more Processes within a System |
| Process | Progression, interaction, and change over time |
| Rule (provisional) | Behavior attachable to a Module without becoming part of its essential identity |
| Module | A System considered as a bounded part of a larger System, identified by its Responsibility |

This document does not yet place Module relative to every System-level concept in Memar — Framework in particular is not addressed here even though it was raised as a candidate for the same level as Module during the discussion that led to this document. That omission is intentional rather than an oversight; see Unresolved questions.

### Modularity Is Not Deployment
A Module is independent of the mechanism used to deploy it.

A Module may be:

- represented by one file or many files;
- stored in one repository or several;
- compiled into one artifact or several;
- executed in one process or several;
- deployed together with other Modules or independently;
- represented by a library, package, service, or another implementation artifact.

None of these arrangements defines the Module.

Deployment is a representation and operational concern. Modularity is a conceptual and structural concern.

This distinction is especially important when evaluating architectural descriptions that use deployment boundaries as if they were modular boundaries.

### The Observer's Boundary and the Monolith Misconception
A System may appear integrated or indivisible from one observation boundary while being highly modular from another.

The word *monolithic* is frequently used as if it were the opposite of *modular*. That comparison is misleading when the terms refer to different dimensions.

A system observed from outside a particular boundary is necessarily encountered as one System at that boundary. Its internal modularity is visible only when the observer considers its internal structure.

Consequently, a single deployed artifact can contain many well-defined Modules. Conversely, many independently deployed services can collectively form a system whose internal responsibilities are tightly coupled and difficult to evolve independently.

The relevant architectural distinction is therefore not:

```text
Monolith  vs.  Microservices
```

but whether the system has meaningful modular boundaries and whether those boundaries preserve coherent responsibilities and manageable relationships.

A so-called monolithic implementation can be modular. A distributed implementation can be a Big Ball of Mud.

### Big Ball of Mud and Modularity
The Big Ball of Mud problem is better understood as architectural degradation than as a synonym for monolithic deployment.

A system becomes difficult to evolve when its boundaries and relationships lose meaningful structure: responsibilities become entangled, dependencies become uncontrolled, local changes propagate unpredictably, and the cost of understanding the system increases.

Changing the number of deployment units does not by itself repair this condition.

Splitting an entangled system into many services can preserve the same conceptual problem while adding network boundaries, operational complexity, and failure modes. Conversely, retaining one deployment unit does not prevent a system from having strong internal modularity.

The classic discussion of Big Ball of Mud is therefore relevant to this document as prior art about architectural erosion, not as evidence that a particular deployment style is inherently modular or non-modular.

### OOP, SOA, and Microservices
The history of software architecture contains repeated attempts to express modularity through increasingly visible boundaries.

Object-oriented programming made objects and classes prominent boundaries. Service-oriented architecture made services prominent boundaries. Microservices made independently deployable services prominent boundaries.

These approaches can provide useful mechanisms, but none of the names by itself defines modularity.

A common failure is to move the boundary outward without first establishing the conceptual boundary inward:

```text
Class boundary
    ↓
Service boundary
    ↓
Deployment boundary
```

If the underlying responsibilities and relationships remain poorly modeled, the new boundary can merely relocate the same coupling.

Microservices are therefore not the definition or culmination of modularity. They are one possible implementation and deployment arrangement for some systems.

Likewise, a monolithic deployment is not evidence that modularity is absent.

The important question is always whether the conceptual Modules have coherent responsibilities, explicit relationships, controlled knowledge of one another, and sufficient independence to evolve without unnecessary propagation of change.

### Event, Rule, and Mechanism-First Design
Modularity does not require an ecosystem of specialized mechanisms for every relationship.

A common implementation tendency is to introduce separate abstractions for every communication pattern:

```text
Request
Response
Event
Command
Notification
Message
```

The existence of these names does not establish that all of them represent distinct concepts in the domain.

If an existing service request or response already expresses the required information, creating another model solely because the interaction is asynchronous or event-triggered can duplicate the model rather than clarify it.

Likewise, introducing a Rule Engine merely because a behavior has been called a Rule reverses the preferred direction of reasoning.

The correct direction is:

```text
Conceptual responsibility
        ↓
Required relationship or capability
        ↓
Process and interaction requirements
        ↓
Required properties
        ↓
Possible mechanisms
        ↓
Implementation
```

A mechanism is justified by a property that the System actually requires, not by the popularity of the mechanism's name.

### Modularity and Implementation Representation
The conceptual Module should not be forced to become a first-class programming-language construct merely because it is architecturally important.

A language may represent a Module using files, directories, namespaces, packages, capsules, types, or other constructs. A framework may represent it through manifests or dependency metadata. A deployment system may represent it through processes or services.

These representations are implementations of modularity, not its definition.

Khayyam's modularity treatment therefore belongs to the language and ecosystem layer. It should explain how the language expresses and resolves modular relationships without redefining the architectural concept of Module through filesystem or package conventions.

## Results

## Discussion

### Drawbacks
Strong module boundaries introduce explicit relationships and therefore require discipline. They can also introduce indirection where a small, stable variation could have been implemented directly.

Separating optional behavior into independent Modules can increase the number of concepts that must be understood. If the boundary is invented only to satisfy a pattern, the result can be more complicated than the original design.

Modularity can therefore fail in two opposite directions:

- insufficient separation, where unrelated responsibilities become entangled;
- excessive separation, where trivial responsibilities are fragmented into unnecessary boundaries.

The goal is not to maximize the number of Modules. The goal is to discover boundaries that correspond to real responsibilities and meaningful independence.

The present definition also intentionally leaves some terminology unresolved. In particular, the project has not yet selected a final name for every kind of optional behavior that can attach to a Module. The document does not attempt to prescribe a universal implementation mechanism either; this means it may not immediately answer practical questions such as where a particular Module should be stored in a repository or how a specific runtime should discover it. Those questions belong to the relevant implementation and tooling documents after the conceptual model is settled.

### Rationale and alternatives
The document deliberately does not define Module through packages, services, repositories, processes, containers, or plugins. Each is too dependent on a particular representation or operational arrangement. This is the central alternative rejected by this document: defining modularity through the physical organization of software would make the architectural model unstable whenever languages, build systems, deployment platforms, or repository conventions changed.

Another rejected alternative is to treat Microservices as the natural unit of modularity. Deployment independence can be useful, but it is neither necessary nor sufficient for conceptual modularity.

The document also rejects the assumption that every extensible behavior requires a new domain data model. Existing Concepts, service requests, responses, and capabilities should be reused when they already express the required information.

The document also does not establish a closed taxonomy of Module kinds. Terms such as *Core Module*, *Infrastructure Module*, *Policy Module*, and similar classifications may be useful in particular contexts, but they should not become part of the foundational definition unless the project discovers a real conceptual distinction that requires them.

Optional Module is retained because it expresses a concrete distinction already required by the model: a Module can be structurally non-essential to a particular System while still providing valuable behavior.

The term Rule remains provisional. If a more precise term is discovered, the terminology can change without requiring a change to the underlying modular model.

### Prior art
The discussion of modularity in software has appeared in object-oriented design, component systems, structured programming, package systems, service-oriented architecture, microservices, and Domain-Driven Design. These traditions provide useful mechanisms and observations but do not supply a single definition of Module that is independent of their implementation assumptions. Domain-Driven Design's Core Domain is a particularly relevant case: the term is commonly presented as if criticality were an intrinsic property of a domain, which invites the same confusion this document argues against — a Module's essential or optional status is relative to a particular System's purpose, not an inherent property of the Module itself.

The Big Ball of Mud discussion is also relevant prior art because it demonstrates that architectural degradation is not uniquely associated with a deployment shape. The relevant problem is the loss of coherent structure and controllable relationships, not the number of deployment units a system happens to have.

Memar therefore treats prior architectural terminology as evidence and material for comparison rather than as authority over the definitions used by the project.

### Unresolved questions
1. What is the final terminology for the kind of Optional Module currently discussed provisionally as a Rule?
2. Which properties distinguish an optional extension from an ordinary independently related Module?
3. What exact relationship should a Module expose when it permits optional behavior to attach without changing its own model?
4. What properties of an EventTarget are fundamental enough to define once and reuse across Types and Modules?
5. When an EventTarget exposes a request or response to interested participants, which parts belong to the Type, the Protocol, and the Process?
6. How should Module identity and dependency resolution be represented independently of repository and filesystem conventions?
7. Which modularity properties can be established by modeling alone, and which require implementation or tooling support?
8. How should modularity be evaluated when a single Module intentionally contains multiple lower-level responsibilities that are tightly coupled by the domain?
9. What evidence distinguishes a necessary Module boundary from fragmentation introduced only by implementation convenience?
10. What is the exact formal relationship between Module and Framework? Module was proposed during the discussion leading to this document as peer-level to System, Structure, Protocol, and Framework; this document now positions Module against Type, Structure, Protocol, Process, and Responsibility, but the relationship to Framework specifically remains open and deserves a dedicated consistency review.

### Future possibilities
A dedicated treatment may later define the relationship between Module, Optional Module, Protocol, EventTarget, and the provisional Rule concept in more formal graph terms.

A future document may also define how modular boundaries can be reviewed independently of implementation structure, including checks for responsibility coherence, uncontrolled knowledge, unnecessary coupling, and accidental deployment-driven boundaries.

Once this document is stable, documents that currently define modularity-related behavior locally — including `modeling.md`, `khayyam-modularity.md`, `framework.md`, and `protocol.md` — should be reduced where appropriate and reference this document instead. Each should retain only the consequences specific to its own concerns rather than redefining Module independently.
