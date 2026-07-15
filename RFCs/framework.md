---
Title: "Framework"
Status: Proposed
Start Date: 2026-06-21
RFC Number: 495003 # OLD:000001
Applied to: ["*"]
Related RFCs:
    - Title: "Terminology"
      URI: "./terminology.md"
      Reason: "Depends_on"
      Explanation: "This RFC builds directly on the terminology philosophy, classification layers, and concept-first thinking established in the Terminology RFC. The definitions in this RFC must be consistent with the terminological principles set there."
    - Title: "System"
      URI: "./system.md"
      Reason: "Depends_on"
      Explanation: "This RFC depends on the foundational definitions of System, Structure, Framework, and Architecture established in the System RFC — particularly the co-equal relationship between Framework (design space) and Architecture (concrete realization), and the distinction between domain-level and system-level constraints."
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Titles: ["Core architectural stance", "Document authority principle", "Terminology governance concept", "Word-weight rebalancing vision"]
        URI: ""
        Explanation: "Defined the core architectural stance that the framework defines the design space for the entire software stack; conceived the document authority and terminology governance principles."
  - Name: "Gemini"
    URI: "https://gemini.google.com/"
    Model: "3.1 pro"
    Effort: "Extended thinking enabled"
    Tasks:
      - Titles: ["Initial draft"]
        URI: ""
        Explanation: "Drafted initial text, argued for and against alternatives, incorporated revisions."
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Tasks:
      - Titles: ["Initial draft"]
        URI: ""
        Explanation: "Drafted initial text, argued for and against alternatives, incorporated revisions."
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Tasks:
      - Titles: ["Argumentation"]
        URI: ""
        Explanation: "argued for and against alternatives; incorporated revisions."
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Medium"
    Tasks:
      - Titles: ["Document Authority and Terminology Governance", "Restructuring to broader scope"]
        URI: ""
        Explanation: "Added Document Authority and Terminology Governance section, formalized the Word-Weight Rebalancing concept for AI model integration with Memar RFCs. Restructured the RFC from a narrow framework-language-OS comparison into a comprehensive architectural definition of Framework itself, moving the relationship discussion into a Reference-level sub-topic."
---

# Framework

## Summary
A **framework** is a structured set of constraints, conventions, and reusable components that provides a foundation for building systems within a defined problem domain. A framework does not describe a particular system — it defines a design space within which multiple architectures may be created.

Framework and Architecture are co-equal aspects of a System: Framework defines *what kinds of solutions are allowed*; Architecture defines *which solution was chosen*. Neither is above or below the other. The full treatment of this relationship, including the distinction between domain-level constraints (framework) and system-level constraints (architecture), is provided in the Reference-level explanation below.

Memar's framework defines the **design space for the entire software stack** — not just the application layer, but the language, the substrate, and the toolchain. In a conventional stack, the framework is a tenant living inside a language and an OS, arranging furniture within walls it did not design. In Memar, the framework specifies what those walls must look like: it defines the design space, and the language and OS are implementation choices within that space. This RFC establishes that stance, explains why it exists, and describes its consequences for every subsequent design decision in the Memar ecosystem.

## Motivation
The word "framework" is one of the most overloaded terms in software engineering. It is used to describe everything from a small routing library to a full application platform, and the ambiguity is not merely linguistic — it leads to architectural confusion. When a team says "we use a framework," it is unclear whether the framework has any authority over the language's type system, the OS's concurrency model, or the deployment topology. In practice, it almost never does. The framework is a tenant in someone else's building, arranging furniture within walls it did not design.

Memar needs the word "framework" to carry a precise, stable meaning because the entire project's coherence depends on it. If "framework" means "a library that provides structure," then Memar is just another library and the relationship between its components is no different from Spring Boot's relationship with the JVM. But if "framework" means "the entity that defines the design space for every layer of the stack," then the relationship between Khayyam, the substrate, and every implementation binding is fundamentally different from any conventional stack — and every subsequent RFC can appeal to that difference as a design principle rather than re-arguing it from scratch.

Without a clear, authoritative definition, each new RFC author will bring their own colloquial understanding of "framework" into the document, and the architectural coherence the project depends on will erode one ambiguous sentence at a time. This RFC prevents that by establishing the definition once, with rationale, and giving it the authority that the Terminology RFC's governance model provides.

## Guide-level explanation
Think of the conventional software stack as a building: the hardware is the foundation, the OS is the ground floor, the language runtime sits on top of that, and the framework is an interior designer arranging rooms within whatever floor plan the floors below happened to provide. The framework can rearrange furniture, but it cannot move load-bearing walls, change the plumbing, or expand the footprint. If the ground floor was designed for retail space and the framework needs a warehouse, the framework must either work around the retail layout or accept suboptimal results.

Memar's framework operates differently. Rather than arranging rooms within a pre-existing floor plan, the framework **defines what the floor plan must satisfy**: what kind of activity happens here, what the spatial relationships are, what the load patterns look like, what the failure modes are. The language and the OS then become the structural engineers who receive the framework's design-space requirements and produce a substrate that satisfies them, rather than the other way around. This is not a claim that the framework is "above" architecture — as the [System RFC](./system.md) establishes, Framework and Architecture are co-equal aspects of System. It is a claim about *which layer gets to define the design space first*.

Concretely, this means that in the Memar ecosystem, when someone says "the framework requires explicit error handling," this is not a style guideline that developers may follow or ignore. It is a design-space constraint: the language is designed so that error paths are syntactically visible, the runtime is designed so that errors cannot be silently discarded, and the tooling is designed so that violations are caught before they reach production. The framework does not request cooperation from lower layers — it specifies requirements that lower layers must satisfy.

This distinction has practical consequences for every participant in the ecosystem. A developer working on a business feature does not ask "what does Go's error model let me do?" or "what does Linux's syscall interface look like?" They ask "what does the framework's contract require?" and trust that the language and substrate have been designed to make fulfilling that contract natural rather than adversarial. A language binding author does not ask "what Go idioms should I follow?" but "what does the framework require, and how do I express that in Go?" — accepting that some framework requirements may be awkward in a given language, and that this awkwardness is a signal the framework identified, not a problem the framework created.

## Reference-level explanation

### Framework and Architecture: Co-Equal Aspects of System
The general definition of Framework is provided in the [System RFC](./system.md) as: "a structured set of constraints, conventions, and reusable components that provides a foundation for building systems within a defined problem domain." This section expands on that definition and establishes its relationship with Architecture in full detail.

#### Framework Does Not Describe a Particular System
A framework defines a design space within which multiple architectures may be created. It provides structure without specifying content, conventions without prescribing decisions, and components without completing the design. The system that results from using a framework is not the framework; it is a system that was built within the framework's constraints.

Architectures make decisions within the possibilities and constraints established by the framework, while frameworks do not determine which specific decisions must be made for a particular system. This distinction is fundamental and non-negotiable: a framework defines *what kinds of solutions are allowed*; an architecture defines *which solution was chosen*.

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

#### Framework vs. Library vs. Toolkit
A library provides specific functionality that a system can use. A toolkit provides a collection of tools for specific tasks. A framework provides a structure within which a system is built. The distinction is one of control: a library is called by the system it serves; a framework calls the system that serves it. This is often described as the "inversion of control" principle. In practice, the distinction is not always sharp — many frameworks include libraries, and many libraries have framework-like conventions — but the conceptual distinction matters because it affects how the developer reasons about the relationship between their code and the framework's code.

Frameworks occupy an intermediate position in the concept hierarchy. They are more concrete than abstractions or models — they provide actual structure that can be used — but less concrete than implementations — they do not specify every detail of the resulting system. A web application framework provides the conventions and components for building web applications, but does not specify what any particular web application does. Memar itself is a framework: it provides the conventions, constraints, and components for building software systems according to Memar's architectural principles, but it does not specify what any particular system built with Memar does.

#### Discussion

##### Drawbacks
Frameworks can constrain architectural freedom by imposing structure that may not be optimal for every system. A developer who uses a framework may unconsciously accept architectural decisions that the framework makes implicitly, treating them as inevitable rather than as choices that could have been made differently. Memar mitigates this risk by making its own architectural decisions explicit and by encouraging contributors to understand *why* each constraint exists, not merely *that* it exists.

The co-equal relationship between Framework and Architecture introduces a terminological risk: because both use the word "constraint," readers may conflate the two types. Memar mitigates this by distinguishing them as *domain-level* constraints (framework) versus *system-level* constraints (architecture), and by ensuring that the dependency chain in the System RFC's Relationships section makes their distinct roles clear.

##### Rationale and Alternatives
- **Provide guidelines rather than a framework (rejected).** Guidelines lack the structural enforcement that a framework provides. Without concrete constraints, conventions, and components, different contributors will make incompatible choices, and the coherence of the resulting systems will suffer.
- **Position Framework as a subset or parent of Architecture (rejected).** Making one subordinate to the other implies a hierarchy that does not exist. Framework and Architecture address different questions — permissible design space vs. concrete realization — and neither contains the other. A system has both a framework (or operates within one) and an architecture; they coexist as parallel, co-dependent aspects of the system.

##### Prior Art
The concept of a software framework is well-established in the literature (Johnson and Foote, "Designing Reusable Classes," 1988; Fayad and Schmidt, "Object-Oriented Application Frameworks," 1997). The distinction between framework and library is discussed in Gamma et al. ("Design Patterns," 1994).

##### Unresolved Questions
1. How should Memar balance the need for framework-level constraints with the need for architectural flexibility?
2. Should Memar define a formal extension mechanism for cases where the framework's constraints are genuinely inappropriate for a specific system?

### Memar's Framework: Design Space Over Implementation Layers

The preceding section establishes the general nature of Framework and its co-equal relationship with Architecture. This section describes how that general definition applies specifically to Memar.

The conventional hierarchy in software development places the framework as a guest living inside a language and operating system — the language defines what is expressible, the OS defines what is executable, and the framework merely organizes how developers use both. Memar's position is different: the framework **defines the design space** that the language and the operating system must satisfy. The language and the OS are components whose design assumptions are themselves shaped by the framework's constraints, not the other way around.

The deeper problem with the conventional model is that the layers were never designed with each other in mind at the architectural level. A language is typically designed to be OS-agnostic and framework-agnostic. An OS is typically designed to be language-agnostic. A framework, arriving last, is left to patch the gaps between whatever assumptions the first two happened to make independently. The result is a stack of layers that each hide complexity from the layer above — and where each layer's hidden complexity eventually leaks upward as surprising constraints, performance cliffs, or security surfaces.

Memar's position is that this ordering is historical accident, not architectural necessity. A framework that defines its design space first — and then specifies what language and OS behavior it needs to support that space — can maintain coherence across all three layers rather than inheriting incoherence from two independent prior decisions. When a framework is subordinate to a language and an OS, it inherits every assumption those layers baked in — often assumptions made decades ago for very different hardware, scale, and application models. A framework built inside Go must accept Go's concurrency model, Go's memory model, and Go's standard library conventions. A framework built on Linux must accept POSIX's process/thread model, its I/O abstractions, and its general-purpose kernel interface. These inherited assumptions are invisible until they become constraints, at which point they are very expensive to remove.

In Memar's model, a developer working on a business feature does not think about "which OS API to call" or "which language runtime to trust." They think about the domain model and the framework's contracts. The OS and the language are implementation details of those contracts — present, but not surfaced. This is the same thinking behind Unikernel architectures, where the application and the OS are compiled together into a single artifact with no general-purpose kernel in between: the application does not "call the OS," it is co-designed with the minimal substrate it actually needs.

#### Practical Implications
- The Khayyam language is not "Memar's language" in the sense that Memar is a framework for Khayyam. Khayyam is a language whose design assumptions are specified by Memar's design space, so that code written in Khayyam already expresses the constraints Memar cares about — explicit state, explicit error paths, no hidden control flow, no invisible allocations.
- An OS running Memar applications is not a general-purpose OS that Memar happens to run on. It is a substrate whose interface is defined by what Memar actually needs — no more. In a fully realized deployment, this means a Unikernel or Exokernel model, not a POSIX kernel offering thousands of syscalls that the application will never use.
- Memar is implemented as libraries across multiple languages and runtimes, at different levels of completeness: a Go implementation (`memar-go`) that has been production-tested in a real business deployment; a JavaScript implementation covering select subsystems only (error handling, services) with no current timeline for further completion; a Rust implementation not yet started, with its repository reserved for future work contingent on additional contributor capacity; and Khayyam itself, still under active design. Defining the design space at the framework level does not require every language binding to be complete or even started — it means Memar's design principles are the starting point that any such binding must conform to, whenever and to whatever extent it is undertaken.

This stance has no syntax or grammar implications — it is a principle that shapes the design decisions made in every subsequent RFC. Specifically, it is the reason why control flow keywords, memory management, concurrency primitives, and standard library shapes are not baked into the Khayyam language itself but instead live in the Memar framework, why the framework's recommended toolchain (compiler, linter, scaffolding) is designed as a coherent unit rather than as independent tools that happen to be compatible, and why constraints (e.g. "no hidden state," "every error path must be visible") are expressed as framework-level contracts rather than as optional conventions.

#### Discussion

##### Drawbacks
Inverting the conventional layer ordering does not make Memar incompatible with existing languages and operating systems — a Go implementation has been built and production-tested in a real business context, and partial implementations exist in other languages. However, this cost is not merely a one-time adaptation friction: a concrete instance already occurred in `memar-go`, where introducing Go generics into an already-working, production-tested implementation produced widespread breakage that, after being deferred for roughly two years, was determined to be unresolvable within Go's generics model rather than merely time-consuming to fix (see [memar-go generics elimination RFC]). This is cited as direct evidence for the RFC's core claim — that friction from implementing framework design-space constraints atop a language with different assumptions compounds over time rather than being paid once — rather than a hypothetical risk.

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

#### The Authority Principle
Memar RFCs are the authoritative source for all terminology used within the framework. When ambiguity exists between common or colloquial usage of a term and the definition established in a Memar RFC, the RFC definition takes precedence within the Memar ecosystem. This is not an assertion that the rest of the world is wrong — it is the same principle that governs any specialized domain. In law, statutory definitions differ from colloquial ones and courts follow the statutory meaning. In medicine, clinical terminology differs from everyday language and practitioners follow the clinical meaning. In physics, "force" has a precise definition that differs from how the word is used in everyday speech, and no physicist apologizes for this precision.

The purpose of this principle is not to change how the world uses words. The purpose is to ensure that within the Memar ecosystem, every participant — human or AI — can rely on stable, precise definitions rather than guessing which of several colloquial meanings is intended. A framework whose foundational terms are ambiguous is a framework whose every subsequent decision inherits that ambiguity.

#### How Authority Is Established
Authority over a term is established when an RFC explicitly defines that term and provides a rationale for the definition. The definition must include:

1. **The precise definition itself** — what the term means within Memar.
2. **Distinctions from related terms** — what the term is not, and why the distinction matters.
3. **Acknowledgment of colloquial usage** — a brief note on how the term is commonly used differently, so readers understand the gap between Memar's usage and the world's.
4. **Rationale for the choice** — why this specific definition serves the framework better than alternatives.

The Protocol RFC (RFC 495465) is the first concrete application of this principle: it defines "Protocol" precisely, distinguishes it from Contract, Standard, Specification, Interface, and Policy, acknowledges that colloquial usage conflates these terms, and provides rationale for each distinction.

#### How Authority Is Maintained
Once a term is defined in an RFC:

- **Subsequent RFCs must use the term according to its RFC-established definition.** If an RFC author needs to use a term in a way that differs from the established definition, they must either (a) use a different term, or (b) write a new RFC that revises the definition with explicit rationale.
- **Revision is possible but costly.** An RFC that revises an established definition must explain what changed, why, and what the implications are for all existing RFCs that use the term. This cost is intentional — it discourages casual redefinition while preserving the ability to correct genuine errors.
- **Ambiguity is resolved by reference, not by popularity.** When a term is ambiguous (e.g., 99% of developers use "standard" to mean "widely adopted protocol"), the RFC definition wins. The fact that the colloquial usage is more popular is irrelevant — popularity does not determine precision. This is the same principle by which scientific terminology is governed: the fact that most people call all reptiles "lizards" does not make the colloquial usage correct for zoological taxonomy.

#### Terminology Governance and AI Models
A specific challenge that Memar must address — one that is increasingly important as AI-assisted development becomes standard — is that AI models are trained on the same ambiguous, conflated usage that this RFC seeks to correct. When an AI assistant encounters the word "standard" in a Memar context, its training data biases it toward the colloquial meaning ("widely adopted specification") rather than Memar's precise meaning ("third-party attestation of protocol institutionalization").

This is not a defect of AI models — it is a consequence of training on human-generated text, which contains the same ambiguities. The solution is not to fix the training data (impossible at the framework's scale) but to establish a mechanism by which the framework's precise definitions carry higher weight than the training data's ambient usage.

**Word-Weight Rebalancing** is the concept for this mechanism. In a fully realized implementation, an AI model operating within the Memar ecosystem would:

1. **Load Memar RFC definitions as a high-weight context layer.** The definitions in RFCs are treated as authoritative references that override the model's default weights for those terms.
2. **Resolve ambiguities by reference.** When the model encounters a term that has both a colloquial meaning and an RFC-established meaning, the RFC meaning takes precedence in any Memar-related context.
3. **Flag conflicts explicitly.** If the model detects that a user's usage of a term conflicts with the RFC definition, it should note the conflict rather than silently adopting the colloquial meaning. The model does not correct the user — it informs them of the framework's definition.
4. **Propagate definitions consistently.** When one RFC references a term defined in another, the model should use the referenced definition, not its training-data understanding of the term.

This concept is not limited to AI models. Human participants in the Memar ecosystem benefit from the same principle: when an RFC has defined a term, that definition is the reference. The difference is that humans can choose to ignore the reference; the word-weight rebalancing mechanism makes it easier for AI assistants to respect it by default.

#### Scope of This Governance
Terminology governance applies to terms that are explicitly defined in Memar RFCs. It does not apply to general English (or Persian, or any other natural language) usage of words that have not been defined by an RFC. The framework does not seek to govern the entire language — only the specific terms that it has taken the responsibility to define precisely.

#### Discussion

##### Unresolved questions
None specific to this topic.

##### Future possibilities
- **Terminology Governance RFC:** A dedicated RFC formalizing the word-weight rebalancing mechanism for AI model integration — specifying how RFC definitions are loaded as high-weight context, how ambiguities are detected and resolved, and how the mechanism is tested for consistency.
- **Memar Glossary:** A living glossary document that extracts all RFC-defined terms into a single reference, making it easier for both humans and AI models to access precise definitions without reading every RFC. The glossary would be auto-generated from RFC frontmatter and definition sections.

## Discussion

### Unresolved questions
None at this time. This RFC is intentionally a statement of architectural stance, not a specification of a concrete mechanism — the concrete mechanisms flow from it in subsequent RFCs.

### Future possibilities
See the Future possibilities subsections under each Reference-level topic above.

## Change Rationale
