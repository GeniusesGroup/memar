# Modularity Handoff
Open work for `modularity.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Can Capability Completeness be checked other than by hypothetical removal?
- Hypothetical removal means asking "if this capability were deleted, which Modules would need edits?" Can completeness instead be checked statically, for instance from declared dependencies alone? (From the Capability Completeness topic's retired Discussion.)

### What is the exact formal relationship between Module and Framework?
- Module was proposed during the discussion leading to this document as peer-level to System, Structure, Protocol, and Framework; this document now positions Module against Type, Structure, Protocol, Process, and Responsibility, but the relationship to Framework specifically remains open and deserves a dedicated consistency review.

## The category layout of this repository
How modules are placed and which categories exist is Classification (`modules/knowledge/modularity/placements.md`)'s, and the open questions about the layout moved to its handoff (`modules/knowledge/modularity/placements.handoff.md`) on 2026-10-17, when the owner's ruling made the categories themselves subject to critique rather than only the folders inside them. What was settled by that ruling and what stays open:
- **Settled 2026-10-17:** `runtime/` merged into `computer/runtime/`; `hardware/`, `identifier/`, the media types, `codec/`, `crypto/` and `memory/` moved under `computer/`; `time/` is not subdivided, because it holds few modules and will keep few; the `lib` category was dissolved into pluggable modules labelled `guest`; the content module and its document sit under `knowledge/` beside documentation. Each is recorded in Classification → Decisions (`modules/knowledge/modularity/placements.handoff.md#decisions`).
- **Still open, carried to the Classification handoff:** whether `crypto/` is rather `math`'s, the four declarations of the `UUID` name, which other modules are pluggable, and whether the base documents of `docs/` move to their modules.
- **Still open here:** where the concurrency primitives live. `computer/runtime/` holds `thread/` and `scheduler/`, while immutable infrastructure (`modules/computer/runtime/immutable_infrastructure/immutable_infrastructure.md`) and concurrency (`modules/computer/concurrency/concurrency.md`) both reach into the area; no document states which of runtime, process, or computer owns a primitive.
- **Settled 2026-10-08, kept as record:** `datatype/` was the wrong spelling and is `modules/computer/type/`; `datatypes/` is `modules/computer/types/`, and under the owner's ruling of 2026-10-10 that no `DataType` trace stays in the corpus nothing else of it remains open but the `Computer_` prefix on one of the three declarations of that module.
- **One naming convention for the layer** is a question about labels, and Label (`modules/knowledge/label/label.md`) is where the rules for names point; `sRPC` and `immutable_infrastructure` against kebab-case neighbours is decided there, not here.

## Anticipated Work
- A dedicated treatment may later define the relationship between Module, Optional Module, Protocol, EventTarget, and Rule in more formal graph terms. (From the document-level retired Future possibilities.)
- A future document may define how modular boundaries can be reviewed independently of implementation structure, including checks for responsibility coherence, uncontrolled knowledge, unnecessary coupling, and accidental deployment-driven boundaries. (From the same section.)
- Once this document is stable, documents that currently define modularity-related behavior locally — including `modeling.md`, `khayyam/modularity.md`, `framework.md`, and `protocol.md` — should be reduced where appropriate and reference this document instead. Each should retain only the consequences specific to its own concerns rather than redefining Module independently. (From the same section.)
