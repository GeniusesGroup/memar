# System Handoff

Open work for `system.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### System
1. Should Memar eventually adopt a more formal treatment of system boundaries, perhaps drawing on the distinction between open and closed systems from thermodynamics and information theory?
2. How should [system.md](./system.md)'s definition of "purpose" interact with systems that have conflicting or internally contested purposes — for example, a political system in which different actors have genuinely incompatible goals?
3. Should System Openness (open/closed/isolated) be formalized as a labeled property on the "influences" edge type in the conceptual graph, so that documents can state explicitly which kind of relationship they mean rather than leaving it implicit?
4. Responsibility is newly added in [System → When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent), defined as Purpose relative to a containing System. `modularity.md`, `process.md`, and `modeling.md` all used the word informally before this definition existed; each should be checked against that section rather than continuing to carry its own implicit sense of the word, and that section should be revised if the check surfaces a usage the definition does not actually cover.

### Structure
1. Does "the arrangement of a system's parts" warrant a dedicated, formally defined concept of its own within Memar, and if so, what should it be called? Until this is resolved, [Structure](./system.md#structure)'s definition can only state what it excludes, not what the excluded concept positively is.
2. How does Structure relate to the layout-related vocabulary already in use elsewhere in Memar (for example, package and module layout in existing software systems), and should `system.md`'s Structure be renamed if it turns out to conflict with established usage rather than merely with general-industry usage?

### Architecture
1. Should Memar develop a more formal framework for assessing the architectural weight of a decision, or is the [proportional-impact heuristic](./system.md#architectural-weight-as-a-spectrum) sufficient?
2. How should architectural decisions made by different contributors at different times be reconciled when they conflict?
3. The ISA-level legitimacy test (see [A Working Test: Does This Deserve to Be Called Architecture?](./system.md#a-working-test-does-this-deserve-to-be-called-architecture)) has been argued for but checked against only a handful of examples. Does it hold up against a wider range of cases — for instance, a small but genuinely long-lived and multi-contributor open-source library's design decisions, which may be smaller in scope than an ISA but still exhibit real emergence and interdependence? Where exactly is the line, and should it be a hard boundary or a graded one, consistent with [Architectural Weight as a Spectrum](./system.md#architectural-weight-as-a-spectrum) treating "architectural weight" as a spectrum rather than a binary?

### Technology
1. Should Memar develop a more granular taxonomy of technology types (physical, conceptual, organizational, cognitive) with specific guidance for each?
2. How should the relationship between technology and power be addressed, if at all, within a software architecture framework?

### Knowledge and Science
1. How should Memar handle concepts that have scientific treatments in multiple disciplines, where the treatments conflict?
2. At what level of scientific rigor should Memar's own terminology be held, given that it is a software framework and not an academic publication?

### Abstraction
1. Should Memar provide explicit mechanisms for documenting abstraction leakage, or should this be left to informal documentation?
2. How should the choice of abstraction level be guided in Memar's modeling process?
3. Should the distinction between structural and purposive abstraction be reflected as two separate, formally named concepts in a future revision, or is it sufficient as an explanatory distinction within a single Abstraction concept?

### Implementation
1. Should Memar define explicit criteria for when an implementation change requires architectural review?
2. How should architectural decisions be documented in a way that remains accessible to contributors who primarily work at the implementation level?

### Relationships Between Concepts
1. Should this conceptual graph be formalized as part of Memar's development process, or should it remain as guidance?
2. Are there important relationship types missing from this model that should be added in future revisions?
3. Should Memar develop a formal notation for these edge types that can be used in other documents?
4. Should the edge types themselves (contains, described by, shaped by, constrained by, expressed by, represented by, governed by, realized by, influences, produces, enables) receive a dedicated formal treatment — defining their precise semantics, compositional rules, and constraints on valid usage? As the nodes stabilize, ambiguity is increasingly migrating to the edges; a formal edge-type ontology may become necessary before the conceptual graph can serve as a reliable reasoning tool across multiple documents.

### Document-level
1. Should `system.md` eventually be split into multiple, more focused documents as the concepts mature, or should it remain as a single foundational document?
2. How should `system.md`'s definitions interact with definitions established by other standards bodies (ISO, IEEE, W3C) when those definitions conflict?
3. Should the conceptual graph's edge types be formalized into a notation that other documents can reference?

## Anticipated Work

- Add more words like "pattern", "paradigm", "thinking tools", ...
- A dedicated document for **Constraint** as a first-class concept, since both Framework and Architecture depend on it and the distinction between domain-level and system-level constraints may warrant deeper formal treatment.
- A dedicated concept (name to be determined) for "the arrangement of a system's parts" — the composition/assembly concept that [Structure](./system.md#structure) explicitly excludes but that Memar has not yet formally named (see [Structure's open questions](#structure)).
- A terminology registry that maps each term defined across all Memar documents to its definition, its terminology layer, and its relationships to other terms.
- A visual diagram of the conceptual graph suitable for inclusion in onboarding material.
- An **Edge Type Ontology document** that formally defines the semantics, compositional rules, and valid-usage constraints for each edge type (contains, described by, shaped by, constrained by, expressed by, represented by, governed by, realized by, influences, produces, enables). As the node definitions stabilize, the primary source of remaining ambiguity in the conceptual graph is the edges — and edge ambiguity is harder to detect than node ambiguity because readers tend to fill in edge semantics from context.
- A dedicated document for **Abstraction Validation** — the question of what qualifies a concept to be considered valid at a given level of abstraction. Memar is, in practice, performing this validation implicitly (e.g., distinguishing Architecture from Design, Framework from Library, Structure from Arrangement), but the criteria are not yet formally modeled. Making them explicit would transform Memar from a project that defines terms into a project that also provides a framework for evaluating whether any given term is being used at the appropriate level of specificity for the concept it names.
- A dedicated document exploring the concept of **Contributor-as-System** — modeling contributors (human or AI) as Systems whose own Structure (capabilities, limitations, available time, cognitive biases) creates bidirectional influence with the Systems they develop (see [System Openness](./system.md#system-openness-open-closed-and-isolated)). This is explicitly deferred because it introduces a new conceptual layer that deserves careful, focused treatment rather than compression into an existing document.
