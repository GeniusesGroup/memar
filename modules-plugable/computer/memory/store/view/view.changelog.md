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

---

### The view built: the builder, the key `view` and `memar view refresh`
- Time: 2026-10-26T21:00:00Z
- Type: Added
- Cited:
  - [Memory Record](../record/record.md) - Reference: the operations the builder reads through
  - [Kernel Neutrality](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule) - Reference: why the key's name is this module's and only its form the preferences module's
  - [Test Practice → The Cycle](../../../../../modules/process/test/test.practice.md#the-cycle) - Reference: the document, then the tests, then the code
- Tasks:
  - main:.agents/tasks/20261026-T192807Z-36152/: Done - step 4 of task `20261023-T074642Z-5420`, part A
- Propagates to:
  - `modules/process/project/services/preferences.py`: Done - its docstring says a module that consumes a class declares its key too
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — wrote the document's changes, the tests, the builder, the verb and the decisions; no `approved` is recorded

#### What changed
- `view.md` names the builder and the verb, says how the key `view` is read, what the builder is handed and what it answers, and replaces its list of cases, and the `Owed: memory.view` line, by a pointer to `tests/view.py`.
- `view.py` holds the key, `Node`, the registry of presentations, the list the builder keeps, the refusals and `build`; `tests/view.py` runs every case over `volatile` and over `git-store`.
- `memar view refresh` is `bundles/memar/services/view/services/refresh.py`, tested by `bundles/memar/services/view/tests/refresh.py` with a test presentation.
- `view.handoff.md` holds the Tentative decisions the build took.

#### Considered and not done
- A line in the entry point of `bundles/memar` naming the verb's module, as `open` is named: its test refuses a verb word in the router's strings, and the router finds a verb by `describe`.
- Registering the Task's presentation: the task module's, task `20261023-T074643Z-5420`.
- A `view` line in Memar's own manifest and its ignore-list entry: the migration's (P4).
