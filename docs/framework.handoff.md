# Framework Handoff

Open work for `framework.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Mental model of the substrate before tool selection
- State: recovered 2026-09-17 from an audit of Omid Hekayati's Telegram-group messages (gopherconf.ir, Gommunity, 2024-2025). A recurring owner position: before selecting any tool, reason from the substrate's own model — know what a hash table is before asking whether Go's `map` fits; design a storage engine by deciding which layer must know the schema, not by comparing database products; and see the whole data path through the machine (even to CPU/cache behavior) as the architecture under design. Relatedly: pursue requirements through **protocols, not tool features**. The framework's documents draw the protocol/implementation distinction and make framework-versus-tool the load-bearing [definition](./framework.md#framework-as-description), but the working rule "reason from the substrate's mental model first, tools second" is stated nowhere; it is also the practical grounding for the [reinvent-the-wheel](../README.md#goals) goal.
- Next: state the rule when the framework document next grows its practice/rationale layer (or route it to [Modeling](./modeling.md) if it proves to be modeling-method rather than framework doctrine); the substrate examples above are the owner's own and can be cited as evidence.

### Balancing framework constraints against architectural flexibility
How should Memar balance the need for framework-level constraints with the need for architectural flexibility?

### Formal extension mechanism for inappropriate constraints
Should Memar define a formal extension mechanism for cases where the framework's constraints are genuinely inappropriate for a specific system?

### Relabeling the Framework-as-Aspect edge
Should the Framework-as-Aspect relationship be relabeled as a distinct edge type (e.g., `constrains` rather than `is an aspect of`), to more precisely capture that a Framework does not become a part of a System but rather constrains a System's Structure from outside? The current "aspect" framing captures the structural consequence (the Framework's constraints appear *within* the System's Structure) but may be misread as implying that the Framework itself is *inside* the System. A future revision should evaluate whether the edge-type language from [System](./system.md)'s conceptual graph provides a more precise framing.

### Formalizing framework goals as a named section
Should a framework's goals be formalized as a named section within the framework's description, or is an informal statement sufficient?

### Conflicting framework goals
How should conflicts between a framework's goals be resolved when they pull in different directions (e.g., "minimize cost" vs. "maximize resilience")?

### Purpose Space / Constraint Space as distinct edge types
Should the Purpose Space / Constraint Space distinction be reflected in [System](./system.md)'s conceptual graph as two distinct edge types, or is the current single `constrained_by` edge sufficient?

### Framework → Model relationship as a graph edge
[framework.md](./framework.md) states the relationship only descriptively — every framework employs models ("A framework *uses* models; a model *is* a representation"), since a framework is a description and every descriptive statement within it constitutes a model at some level of abstraction. Decide whether Framework → Model should also appear as an explicit edge in [System](./system.md)'s conceptual graph — and, if so, whether it is a mandatory edge (a Framework without any Model cannot exist) or remains an explanatory relation owned by the Framework document.

### Framework goals versus System Purpose and Responsibility
How does the goal-orientation of a framework relate to System's Purpose and to System's newly-added Responsibility (a part's Purpose expressed relative to a containing System — see [System → Responsibility](./system.md#system))? Is a framework's goal the same as a System's purpose, is it closer to a Responsibility, or is there a meaningful distinction from both? [framework.md](./framework.md) does not yet check its own use of "goal" against either definition.

### Labeled property for framework versus sub-framework on `constrained_by`
Should the framework/sub-framework distinction be formalized as a labeled property on the `constrained_by` edge in [System](./system.md)'s conceptual graph, so that documents can state explicitly whether a given `constrained_by` relationship involves a framework or a sub-framework?

### Intermediate category between framework and sub-framework
Is there a useful intermediate category between "framework" and "sub-framework" — a system that is more complete than a typical sub-framework but not as comprehensive as a full framework?

### Dedicated document for the framework/sub-framework distinction
Should the framework/sub-framework distinction receive its own dedicated document, given that it has practical implications for how Memar evaluates and integrates with external systems?

### Evaluating progress toward Memar's stated goal
How should progress toward the goal stated in *Memar's Purpose Space: From Knowledge to Agency* ([framework.md](./framework.md#memars-purpose-space-from-knowledge-to-agency)) be evaluated — what observable evidence would show that a system built with Memar is approaching the stated capability, and what would show it is not?

### Goal statement in the README for non-software instantiations
Should the goal statement be reflected in the README's System Categories for Memar's non-software instantiations (buildings, organizations, society), or does the chain apply only to cognitive systems?

### Recording the memar-go generics-elimination event as citable evidence
The [memar-go generics elimination](https://github.com/GeniusesGroup/memar-go/blob/main/.agents/docs/Elimination_of_Open_Generic_Type_Parameters.md) event cited under *Memar's Framework* as evidence is documented in the `memar-go` repository, not in this project's own documentation system. If this event is meant to stand as citable evidence for the document's core claim, it may deserve its own short record (in `memar-go`'s own changelog, or referenced from there) rather than remaining a parenthetical description in [framework.md](./framework.md).

### Design-space treatment for Memar's non-software categories
*Memar's Framework: Design Space Over Implementation Layers* ([framework.md](./framework.md#memars-framework-design-space-over-implementation-layers)) scopes itself explicitly to Memar's Computer (software) system category, per the project README's System Categories. Memar's other, non-software system categories do not yet have a comparable design-space treatment anywhere. Whether they need one, and if so whether it belongs in [framework.md](./framework.md) as a sibling topic or somewhere else entirely, is open.

### Stable citation form for a document's current identity
The [Protocol document](./protocol.md) reference under *Document Authority and Terminology Governance* ([framework.md](./framework.md#document-authority-and-terminology-governance)) previously carried an explicit identifier ("RFC 495465") in that document's prose. That identifier is not repeated in the body, since a document's identifier is assigned at creation and is not a stable citation form on its own — but if a stable way to cite a specific document's current identity is needed (beyond a relative link, which can go stale if a file is renamed), that is an open question for the documentation system generally, not specific to Framework.

## Anticipated Work

- A dedicated document or section that formalizes the relationship between a framework's stated goals and the design space it produces — potentially including a notation for expressing framework goals and a method for evaluating whether a given design space is consistent with its stated goals. (From the Goal-Oriented Frameworks and Purpose Space topic in framework.md.)
- Integration with the Terminology Governance mechanism (see [Document Authority and Terminology Governance](./framework.md#document-authority-and-terminology-governance)) to ensure that a framework's goals are treated as authoritative definitions within the Memar ecosystem. (From the Framework-as-Description topic in framework.md.)
- A dedicated **Sub-Framework document** that formally defines the boundary between frameworks and sub-frameworks, provides evaluation criteria, and assesses common industry systems against those criteria. This would be particularly valuable for contributors who need to understand whether adopting an external system introduces sub-framework-level gaps into their design space. (From the Framework-as-Description and Framework-and-Sub-Framework topics in framework.md — the same item appeared identically under both.)
- **Minimal OS Interface Specification:** A formal specification of the minimal OS interface Memar applications actually require (the boundary between "what the framework's design space requires from a substrate" and "what a substrate provides") would be the natural follow-up to the *Memar's Framework: Design Space Over Implementation Layers* topic at the OS-design layer. (From the Memar's-Framework topic in framework.md.)
