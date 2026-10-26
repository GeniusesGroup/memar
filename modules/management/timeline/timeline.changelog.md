# Timeline Changelog

## Changelog

### Research on what the timeline domain is for, its kernel, and the owner's questions
- Time: 2026-10-18T19:30:00Z
- Type: added
- Cited:
  - [Modules → Placement](../../modules.md#placement) - Reference: the kernel and pluggable tests the research applies
  - [Event → What an Event Is](../../process/event/event.md#what-an-event-is) - Reference: an Event is a runtime occurrence, not a stored record
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-18)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted

#### What changed
- [timeline.research.001.md](timeline.research.001.md) is added: thirteen scenarios; a proposal that the domain's concept is the placement; a five-element kernel and eight pluggables; six rival models with a recommendation (unratified); a mapping of every edge folder; eleven missing pieces; twenty-four test scenarios; reconciliation with the sibling researches; fourteen contradictions reported, not resolved; and twenty-five owner questions with defaults.
- [timeline.handoff.md](timeline.handoff.md) gains the twenty-five questions with defaults and what each blocks, six Next Steps, and the research in Related Artifacts.
- Nothing in [timeline.md](timeline.md), in any edge document, or in any `.kh` file was changed; nothing was moved or deleted.

---

### Decisions that storing timelines and placements forces
- Time: 2026-10-23T17:30:00Z
- Type: Added
- Cited:
  - [Memory Record](../../../modules-plugable/computer/memory/store/record/record.md) - Reference: the store placements are written to
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme; the build tasks are queued after it
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-22/23), ruled the premises it rests on
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted
  - Three sub-agents (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed; their findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- [timeline.handoff.md](timeline.handoff.md) gains the Tentative decisions for questions 1 to 4, 15, 17 and 25 and the reply order: the one id of Task, timeline and group, the group and the conversation, the placement as a node, the order by `placed_at`, nothing ended or erased, and the current content of each name as a stored pointer in the `timeline` part.
- [timeline.md](timeline.md) is not edited.

---

### Timeline storage shape: a question for the owner
- Time: 2026-10-24T17:30:00Z
- Type: Changed
- Cited:
  - [Memory](../../computer/memory/memory.md#retention-is-reached-through-one-contract) - Reference: the memory contract's reference to an address, which is all a kernel module takes of retention
- Tasks:
  - main:.agents/tasks/20261024-T160312Z-25344/: Partial - repoints the kernel documents from the record contract to the memory contract's reference to an address; a fresh critique follows
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled on 2026-10-24 that the link is only the reference to an address
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — found the statements and wrote the change

#### What changed
- `timeline.handoff.md`: the sentence that the store has no access notion names the memory contract; the Open Question "Does the timeline domain keep its storage shape, the keys `timeline`, `placement` and `placement-end`, in the kernel module?" is added. `timeline.md` names nothing of `record` and is unchanged.

#### Considered and not done
- Moving the Tentative decisions of 2026-10-23 out of the handoff: they are not load-bearing in `timeline.md` and the owner's answer decides where they go.

---

### The citation of the memory contract names the module that owns the statement
- Time: 2026-10-26T14:10:00Z
- Type: Changed
- Cited:
  - [Memory Address](../../computer/memory/address/address.md) - Reference: the reference to an address
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the files moved with `git mv` and the links and addresses repaired; the second division and the build tasks are still owed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried out the move and repaired the links; no `approved` is recorded

#### What changed
- The links to `memory.md#retention-is-reached-through-one-contract` in the document and its handoff name [Memory Address](../../computer/memory/address/address.md), the module that owns the statement, since the section is now a pointer.
