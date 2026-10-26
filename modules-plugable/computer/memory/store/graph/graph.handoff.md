# Graph Handoff
Open work for `modules-plugable/computer/memory/store/graph/graph.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../../knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Decisions

### What the graph module is to the memory contract (2026-10-24, Tentative)
Reviewed by task `20261024-T160311Z-25344`; the module is held as it stands and nothing is moved or removed. Its Go-era services (`Save`, `Get` with versions, listing by complement and by priority) add no address kind, no operation and no guarantee to the contract, and the versions of a value are the Request chain, which `data_model.kh` already carries as `Field_RequestID`. What a graph store would own, if it owns anything, is a layout over [Key-Value](../key_value/key_value.md): an edge written under a key of the vertex, the label and the other vertex, with the key of the reverse side written in the same batch, and the derived edges rebuilt from `changes`. Whether that layout is a responsibility that can change independently of the key-value store, as a store specialised for graph-shaped data may be, is the open question below.

## Open Questions

### Does storing graph-shaped data need a module of its own, or is it a layout over `key_value` and `record`?
- State: the abstract graph is declared at `modules/computer/adt/graph/`, relations are the `edges` folders of the domain modules, and a derived edge is a cache owned by the module that gives it meaning ([Modules → Edge folder](../../../../../modules/modules.md)). On that reading this module has nothing of its own. The owner is not sure of it (2026-10-25): databases that claim specialisation for a shape of data, graphs or time series among them, may hold techniques for storing it efficiently that a general store does not, and an abstraction is justified by a responsibility that can evolve alone ([Modeling → Abstract](../../../../../docs/modeling.md#abstract)).
- Importers that a move would touch: `modules/computer/request/widget/protocol/data_model.kh` and `modules/knowledge/label/edges/list/protocol/data_model.kh` import its protocol; `modules/identity/organization/organization.md` and `modules/identity/person/edges/social_connections/social_connections.md` link its README.
- Next: examine, when `key_value` is built, which operations a graph consumer needs that the contract and a key layout do not give (adjacency by vertex and label in both directions, bounded neighbours of a vertex with millions of edges, incremental distance upkeep); a responsibility found there is a capsule of its own on `key_value`, and none found folds the module into its owners. No file is removed before then.
- Asked: 2026-10-24, Claude (task `20261024-T160311Z-25344`), for Omid Hekayati.
