# Graph Changelog

## Changelog

---

### Reviewed against the memory contract: held as it stands
- Time: 2026-10-24T18:40:00Z
- Type: Changed
- Cited:
  - [Memory](../../../../../modules/computer/memory/memory.md#retention-is-reached-through-one-contract) - Reference: the contract the module was reviewed against
- Tasks:
  - main:.agents/tasks/20261024-T160311Z-25344/: Partial - the design task
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled that the module is held while it is unsure that graph-shaped storage needs none of its own
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed and wrote

#### What changed
- [graph.md](graph.md) gains a section on what the module is to the memory contract; [graph.handoff.md](graph.handoff.md) is added with the review and the open question.
#### Considered and not done
- Dropping the module and folding its subject into the abstract graph, the edge folders and the derived-edge rule was not done: the owner is unsure that specialised storage needs nothing of its own.

---

### The graph capsule stands under the store modules
- Time: 2026-10-26T14:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) - Reference: the division that gives the new path
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the files moved with `git mv` and the links and addresses repaired; the second division and the build tasks are still owed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried out the move and repaired the links; no `approved` is recorded

#### What changed
- The folder moved unedited from `modules/storage/graph/` to `modules-plugable/computer/memory/store/graph/`.
- The citation of the memory contract now names [Memory Store](../../../../../modules/computer/memory/store/store.md#the-contract).
