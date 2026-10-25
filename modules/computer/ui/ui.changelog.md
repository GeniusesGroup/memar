# GUI Changelog

## Changelog

### Architecture position added: three separations, widget model, page state, network silence, shared validation
- Time: 2026-09-06T00:00:00Z
- Type: Expanded
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- The GUI protocol gained its architectural position: three-way separation, widget-based model, protocol-level page state and history, single routing authority, SDK-mediated service access, and once-generated shared validation.
- The positions were recorded as the document's Position on GUI Architecture, above the existing Page specification (Super Z — recorded).
- The silent-on-architecture fault was linked to the modeling document's decomposition treatment (Super Z — recorded).
- The JSX/React separation-of-technologies claim was kept stated as the ecosystem's own reasoning (Super Z — recorded).
- The existing Page/ID/URN spec was preserved untouched below the new position (Super Z — recorded).

#### Deliberation
- The positions were brought from public GUI-architecture discussions — the front-end gafteman sessions and their written continuation (Omid Hekayati — claimed).
- The content/presentation/logic three-way separation was claimed as the web standards' one proven idea (Omid Hekayati).
- The widget/component distinction was claimed: widget — a single named instance acquiring its own data; component — a per-use template instance with passed-in state (Omid Hekayati).
- The History API was critiqued as built on SSR assumptions, with structureless state blobs (Omid Hekayati).
- One routing authority per application was claimed (Omid Hekayati).
- The GUI-does-not-speak-network rule was claimed, with the generated SDK as the only network-aware part (Omid Hekayati).
- Shared server/GUI validation via accessor/setter generation was claimed (Omid Hekayati).

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:50Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed

#### What changed
- Reviewed; no change needed. The added handoff entry about `Event_Methods`: `modules/gui/protocol/event.kh` lines 14, 40, 63 and `modules/gui/event.kh` lines 18 and 56 match the cited text, and no file under `modules/process/event/` declares it. Ownership reasoning holds; the question is left to the owner.

---

### The first realization of the GUI, for a system delivered in Python
- Time: 2026-10-24T16:06:00Z
- Type: Added
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) — argued, drafted, applied

#### What changed
- `ui.handoff.md` gained the Tentative decision [The first realization of the GUI, for a system delivered in Python](./ui.handoff.md#the-first-realization-of-the-gui-for-a-system-delivered-in-python-tentative-2026-10-24-task-20261024-t074257z-16944): widgets run in the serving process and reach services through local SDK invocation; the browser holds one small fixed runtime that is the only part speaking HTTP; a console is the domains' pages composed by the adopting organization's bundle, editing through the verb and its Request and deleting nothing; right-to-left as a document property; and recommended answers to the open questions on page state and on the GUI's half of validation.
- `ui.md` is unchanged.

#### Deliberation
- The owner's ruling of 2026-10-24 (Python, no Django, the console on Memar's own GUI) is the input (Claude — recorded).
- Running widgets in the serving process keeps one language to convert, one validation and no browser build toolchain on an air-gapped site; the cost is a round trip per interaction on the site's own network (Claude — argued).

---

### Guarantee of removal repointed to the memory contract
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
- `ui.handoff.md`: that nothing is deleted is stated of the memory contract, until an erasure rule is made, in place of the port of `record`.

#### Considered and not done
- Any other change to the console's paragraph.

---

### The browser script's departure from the network premise asked of the owner
- Time: 2026-10-24T16:50:00Z
- Type: Changed
- Tasks:
  - main:.agents/tasks/20261024-T162240Z-16944/: Complete - applies the independent critique of task 20261024-T161344Z-16944 to the Python-first delivery path
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) — applied the critique's findings

#### What changed
- `ui.handoff.md`, decision "The first realization of the GUI, for a system delivered in Python": it stays Tentative; the rule that the GUI does not speak the network is said to hold for widget code by construction, and the browser-script bullet states that a hand-written script speaking HTTP departs from a premise of [Position on GUI Architecture](./ui.md#position-on-gui-architecture).
- `ui.handoff.md` gained the open question "Does the GUI's browser script speak HTTP by hand, or is it generated from the SDK?", with the generated script as the recommended option.

#### Deliberation
- The critique (task 20261024-T161344Z-16944, findings (a)2 and (f)4) found the decision changes a premise the model rests on, which makes it the owner's before it binds (Claude — checked against `ui.md`).

---

### The browser script's network part is generated from the SDK, recorded Tentative
- Time: 2026-10-24T17:00:00Z
- Type: Changed
- Tasks:
  - dev-knowledge:.agents/tasks/20261024-T164111Z-16944/: Closed - records the answer the questions-answer agent of task 20261024-T074257Z-16944 gave from the owning documents
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) - recorded

#### What changed
- `ui.handoff.md`, Tentative decision "The first realization of the GUI, for a system delivered in Python": the browser-script bullet now states that the script's network part is the generated realization of the page-event service, written by the SDK generator from that service's declaration, and that its hand-written part only applies returned document parts and knows no network, so the premise of [Position on GUI Architecture](./ui.md#position-on-gui-architecture) holds unchanged; the bullet carries its reasons and its cost, the SDK generator's browser-side network realization added to the GUI block of the delivery design.
- The open entry "Does the GUI's browser script speak HTTP by hand, or is it generated from the SDK?" was removed, its answer being that bullet.

#### Considered and not done
- A hand-written script that speaks HTTP, as the one stated exception: it puts an exception into the premise and drops the shared validation shown as the person types.
- No script, a full page per event by a plain HTML form: no validity shown as the person types.
