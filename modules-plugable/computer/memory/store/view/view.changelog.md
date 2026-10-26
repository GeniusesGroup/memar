# Memory View Changelog

## Changelog

---

### The memory view as a pluggable consumer of the port
- Time: 2026-10-23T17:30:00Z
- Type: Added
- Cited:
  - [Memory Record](../record/record.md) - Reference: the port the view reads through
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme; the build tasks are queued after it
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-22/23), ruled the premises it rests on
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted
  - Three sub-agents (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed; their findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- [view.md](view.md) is added: a read-only folder built from the committed state of one class, a function of that state and the preferences, never committed and never edited, built on demand, named by the content names and the task module's presentation, with its cases.
- The view section of the port document is replaced by a pointer to it.

---

### The view stands beside the capsules it reads
- Time: 2026-10-24T16:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#the-model-of-the-memory-layer-2026-10-24-decided-by-the-owner-in-task-20261024-t052936z-22844) - Reference: the model that places it
- Tasks:
  - main:.agents/tasks/20261024-T052936Z-22844/: Partial - the modelling task
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled the adapters and their consumers independent of `record`
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- The Placement paragraph names the home, `modules-plugable/computer/memory/view/`, and says the module moves there with the others.

---

### The view stands under the store modules
- Time: 2026-10-26T14:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) - Reference: the division that gives the new path
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the files moved with `git mv` and the links and addresses repaired; the second division and the build tasks are still owed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried out the move and repaired the links; no `approved` is recorded

#### What changed
- The folder moved unedited from `modules-plugable/computer/memory/record/view/` to `modules-plugable/computer/memory/store/view/`; the Placement paragraph names the new path.
