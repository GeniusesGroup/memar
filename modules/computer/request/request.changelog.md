# Request Changelog

## Changelog

### Request Research 001: what the domain is for, its kernel, the runtime chain, and the owner's questions
- Time: 2026-10-19T00:00:00Z
- Type: added
- Cited:
  - [Modules → Placement](../../modules.md#placement) - Reference: the kernel and pluggable tests the research applies
  - [Account Research 001](../../economics/account/account.research.001.md) - Reference: the sibling research whose shape this follows
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-14)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted

#### What changed
- [request.research.001.md](request.research.001.md) is added: ten scenarios; a proposal that the domain is the durable memory of one asking, cited by other domains' registration facts; a seven-element kernel and event target; six rival models with a recommendation (unratified); the who, pipe, software, node chain read through connection, software and instance_of; a mapping of every folder; missing edges and pluggables; eighteen tests; fifteen contradictions; reconciliation with the sibling researches and the synthesis task `20261018-T195830Z-17032`.
- [request.handoff.md](request.handoff.md) gains seventeen questions with defaults and what each blocks, a pointer to the contradictions (including Memar file names that do not exist), and six Next Steps.
- Nothing in [request.md](request.md), in any `.kh` file, or in the neighbour domains' documents was changed beyond a pointer section in the connection, software and instance_of handoffs; nothing was moved or deleted.

---

### Recording a change of state, and the decisions that storing Requests forces
- Time: 2026-10-23T17:30:00Z
- Type: Added
- Cited:
  - [Memory Record](../../../modules-plugable/computer/memory/store/record/record.md) - Reference: the store the Request is written to
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme; the build tasks are queued after it
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-22/23), ruled the premises it rests on
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted
  - Three sub-agents (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed; their findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- [request.md](request.md) gains the section Recording a change of state: what a change of state is, which changes are recorded and which are not, the write of the new value and the Request in one batch with its expectations in order, the retry rule, the Request node (`request`, `request-data`, the labels), the stored `request-head` and `follows` of each change, and the history walk. It marks `Owed: memory.stored-shape` and `Owed: request.signing-key`, and its blank lines under headings are corrected.
- [request.handoff.md](request.handoff.md) gains the Tentative decisions for questions 1 to 9, 12, 14, 16 and 17, the questions that block nothing, and the facts verified on 2026-10-23.

#### Considered and not done
- A head pointer was first refused as derived data, then adopted because tokens repeat and ids order by minting instant, so the last Request cannot be derived.
- The view in the port document, an adapter-built view, a default adapter for an unset class, a port that refuses invalid text, and `sub-request` as the chain edge's name were each considered and not taken; the reasons are in the port handoff and the request handoff.
- No Status history is recovered for the migration, since the old logs hold no Status values.

---

### Request chain: identifier repointed to the memory contract, storage shape asked of the owner
- Time: 2026-10-24T17:30:00Z
- Type: Changed
- Cited:
  - [Memory](../memory/memory.md#retention-is-reached-through-one-contract) - Reference: the memory contract's reference to an address, which is all a kernel module takes of retention
- Tasks:
  - main:.agents/tasks/20261024-T160312Z-25344/: Partial - repoints the kernel documents from the record contract to the memory contract's reference to an address; a fresh critique follows
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled on 2026-10-24 that the link is only the reference to an address
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — found the statements and wrote the change

#### What changed
- `request.md`: a stored Request is named by the address through which it is retained, with a link to the memory contract's reference to an address, in place of the id of its node. `request.handoff.md` gained the Open Question "Does the Request domain need more of `record` than the reference to an address?".

#### Considered and not done
- Editing "Recording a change of state" and "The Request node": parts, `request-head`, labels, `scan` and the binding of classes are only `record`'s and load-bearing, so the section and its links to `record.md` stay and the question is the owner's.

---

### The conversion of stored shapes against signed Requests asked of the owner
- Time: 2026-10-24T16:50:00Z
- Type: Changed
- Tasks:
  - main:.agents/tasks/20261024-T162240Z-16944/: Complete - applies the independent critique of task 20261024-T161344Z-16944 to the Python-first delivery path
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) — wrote the question

#### What changed
- `request.handoff.md` gained the open question "How does an update convert stored shapes when past Requests are signed and never edited?", anchored at [The Request node](./request.md#the-request-node) and its mark `Owed: memory.stored-shape`; `request.md` is unchanged.

#### Deliberation
- The critique (task 20261024-T161344Z-16944, finding (d)1) found that converting the payloads of past Requests on update breaks their digests and signatures, while not converting them breaks the rule that the system reads only the new shape (Claude — checked against "The write" and "The Request node").
- No document named `memory.stored-shape` exists yet, so the question is written here, where the mark is (Claude — checked).

---

### The owner's working answer on stored shapes under signed Requests recorded as a Tentative decision
- Time: 2026-10-25T14:30:00Z
- Type: Changed
- Propagates to:
  - [request.md](./request.md): Pending - its mark `Owed: memory.stored-shape` stays until task 20261025-T140526Z-16944 settles the rule.
  - [Immutable Infrastructure → A change carried to a site with no network](../runtime/immutable_infrastructure/immutable_infrastructure.md#a-change-carried-to-a-site-with-no-network): Pending - still says the treatment of past Requests' payloads is open, and its rule would read "writes only the new shape and reads old shapes only in history"; for the deeper task.
- Tasks:
  - dev-knowledge:.agents/tasks/20261025-T140621Z-16944/: Closed - records the owner's acceptance of 2026-10-25
  - dev-knowledge:.agents/tasks/20261024-T074257Z-16944/: Reference - the design task whose report asked the entry
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5 via Claude Code) - recorded

#### What changed
- On 2026-10-25 the owner accepted the recommended option of the open entry "How does an update convert stored shapes when past Requests are signed and never edited?" in [the handoff](./request.handoff.md) as a working answer, to be studied in depth in task 20261025-T140526Z-16944. The entry left Open Questions and is now the Tentative decision "Past Requests are never converted; old shapes are read only in history", carrying its reasons and the options not taken; it is an exception to a stated rule and stays visibly a working answer.

---

### The citation of the memory contract names the module that owns the statement
- Time: 2026-10-26T14:10:00Z
- Type: Changed
- Cited:
  - [Memory Address](../memory/address/address.md) - Reference: the reference to an address
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the files moved with `git mv` and the links and addresses repaired; the second division and the build tasks are still owed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried out the move and repaired the links; no `approved` is recorded

#### What changed
- The links to `memory.md#retention-is-reached-through-one-contract` in the document and its handoff name [Memory Address](../memory/address/address.md), the module that owns the statement, since the section is now a pointer.
