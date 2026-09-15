# Modularity Handoff

Open work for `modularity.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Can Capability Completeness be checked other than by hypothetical removal?
- Hypothetical removal means asking "if this capability were deleted, which Modules would need edits?" Can completeness instead be checked statically, for instance from declared dependencies alone? (From the Capability Completeness topic's retired Discussion.)

### What is the final terminology for the kind of Optional Module currently discussed provisionally as a Rule?

### Which properties distinguish an optional extension from an ordinary independently related Module?

### What exact relationship should a Module expose when it permits optional behavior to attach without changing its own model?

### What properties of an EventTarget are fundamental enough to define once and reuse across Types and Modules?

### When an EventTarget exposes a request or response to interested participants, which parts belong to the Type, the Protocol, and the Process?

### How should Module identity and dependency resolution be represented independently of repository and filesystem conventions?

### Which modularity properties can be established by modeling alone, and which require implementation or tooling support?

### How should modularity be evaluated when a single Module intentionally contains multiple lower-level responsibilities that are tightly coupled by the domain?

### What evidence distinguishes a necessary Module boundary from fragmentation introduced only by implementation convenience?

### What is the exact formal relationship between Module and Framework?
- Module was proposed during the discussion leading to this document as peer-level to System, Structure, Protocol, and Framework; this document now positions Module against Type, Structure, Protocol, Process, and Responsibility, but the relationship to Framework specifically remains open and deserves a dedicated consistency review.

### Where should the Module that owns a cross-boundary relationship live when its endpoints belong to different Modules?
- With one endpoint, with both, or in an independent third home? Hosting chosen mainly for repository convenience encodes false conceptual ownership; see the counterpart open question under [Modeling → Edge Types and Their Traditional Counterparts](./modeling.handoff.md#edge-types-and-their-traditional-counterparts).

## Anticipated Work

- A dedicated treatment may later define the relationship between Module, Optional Module, Protocol, EventTarget, and the provisional Rule concept in more formal graph terms. (From the document-level retired Future possibilities.)
- A future document may define how modular boundaries can be reviewed independently of implementation structure, including checks for responsibility coherence, uncontrolled knowledge, unnecessary coupling, and accidental deployment-driven boundaries. (From the same section.)
- Once this document is stable, documents that currently define modularity-related behavior locally — including `modeling.md`, `khayyam/modularity.md`, `framework.md`, and `protocol.md` — should be reduced where appropriate and reference this document instead. Each should retain only the consequences specific to its own concerns rather than redefining Module independently. (From the same section.)
