# Agency Handoff
Open work for `agency.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### What is the exact semantic direction of `agent_for`?
The relationship must be formalized so that its graph direction cannot be misunderstood — including whether the direction should read Principal → Agent or Agent → Principal, since natural-language phrasing ("A is agent for B") does not settle this by itself and different direction conventions have been used informally in early drafts of this model.

### Should the execution-responsibility relationship get a canonical edge name?
Whether Memar should eventually give the execution-responsibility relationship a canonical edge name, or keep it expressed through the existing Responsibility concept until the graph model demonstrates a need for a specific relation.

### How does accountability propagate through delegated Agency?
Delegation does not necessarily transfer accountability. The model should establish explicit rules for responsibility and accountability propagation — including whether accountability can be split (partially transferred) rather than only wholly retained or wholly transferred, which the current model does not address.

### Does this document's own existence count as an instance of the Hybrid Agency it describes?
This is a genuine reflexive question rather than a rhetorical one: the process that produced this document involved a human Principal setting direction, one AI system drafting and revising collaboratively, and a second AI system (performing an earlier edit) reorganizing and extending it against a separate specification — which maps fairly directly onto the [Hybrid Agency](./agency.md#hybrid-agency) and [Multi-Agent Systems](./agency.md#multi-agent-systems) topics in the body. Whether that mapping holds up, and whether it is useful, has not been tested.

### Do the Working Principles hold up as later documents are written against them?
- State: moved here 2026-09-10 from the removed `Results` section (three-section skeleton migration): whether the working principles in [Working Principles](./agency.md#working-principles) hold up is watched as later documents (Role, Permission, Contract) are written against this document.
- Next: evaluate each new document written against this one for whether the principles required exception or restatement; record findings in this handoff and route any resulting change through a changelog entry.

## Anticipated Work
- Define `role.md`, `permission.md`, and `contract.md` if they prove dense enough to warrant their own documents — concepts mentioned during the discussion that produced this document as ones that may eventually reference Agency rather than redefine it; consistent with the Delegation decision in [Delegation](./agency.md#delegation), the same "can it be defined without first defining Agency?" test should be applied to each before splitting it out. (From the document-level Future possibilities.)
- Produce a worked example connecting this document to `type.md` — the placement of System, Agent, and Principal relative to Capsule, Method, Abstraction, and Scope is settled as cross-cutting in [Agency and Type Categories](./agency.md#agency-and-type-categories), but which category, if any, realizes a given agentive System is not, and a worked example would settle it in practice rather than by assertion. (From the document-level Future possibilities.)
- State a positive composition rule for how Delegation, Responsibility, Authority, Capability, Context, Knowledge, and Trust combine into a coherent delegation, replacing the current pairwise non-equivalence statements (recorded as a drawback in the [Agency Changelog](./agency.changelog.md)) with something closer to a checklist or a formal condition. (From the document-level Future possibilities.)
