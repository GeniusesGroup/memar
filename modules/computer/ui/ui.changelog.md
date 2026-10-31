# UI Changelog

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
- `ui.handoff.md`, decision "The first realization of the GUI, for a system delivered in Python": it stays Tentative; the rule that the GUI does not speak the network is said to hold for widget code by construction, and the browser-script bullet states that a hand-written script speaking HTTP departs from a premise of [Position on GUI Architecture](../../../modules-plugable/computer/ui/gui/gui.md#position-on-gui-architecture).
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
- `ui.handoff.md`, Tentative decision "The first realization of the GUI, for a system delivered in Python": the browser-script bullet now states that the script's network part is the generated realization of the page-event service, written by the SDK generator from that service's declaration, and that its hand-written part only applies returned document parts and knows no network, so the premise of [Position on GUI Architecture](../../../modules-plugable/computer/ui/gui/gui.md#position-on-gui-architecture) holds unchanged; the bullet carries its reasons and its cost, the SDK generator's browser-side network realization added to the GUI block of the delivery design.
- The open entry "Does the GUI's browser script speak HTTP by hand, or is it generated from the SDK?" was removed, its answer being that bullet.

#### Considered and not done
- A hand-written script that speaks HTTP, as the one stated exception: it puts an exception into the premise and drops the shared validation shown as the person types.
- No script, a full page per event by a plain HTML form: no validity shown as the person types.

---

### UI document says what it is; the GUI position moves to the GUI realization; Widget stated in full
- Time: 2026-10-31T07:00:00Z
- Type: Changed
- Tasks:
  - memar:.agents/tasks/20261030-T151453Z-10624/: Open - the owner reviewed the proposal in chat and approved it before it was applied
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) - recorded

#### What changed
- `ui.md` was titled and written as the GUI document while its module and file are `ui`, which led agents to read Widget as UI-only. It is now "UI - User Interface": it states that UI is how any agent meets services, that the GUI, VUI, command and CLI are its realizations, and that Widget and Page are its core parts. Its Widget section states the owner's ruling of 2026-10-30: a widget is the aggregator of services and of other domains' widgets, aggregation is done only in widgets, and a service does one definite thing and never aggregates.
- The GUI position (three separations, the stances, Page ID and URN, resources, related projects) moved unchanged in substance to `modules-plugable/computer/ui/gui/gui.md`, the GUI realization's own document, with the Widget stance now naming the widget as the aggregator. The title of this changelog is now "UI Changelog"; the entries below record the GUI position's history before the move.
- `widget/widget.md` states the concept in full: what a widget is (named, stateful, not bound to a screen, hosted by software), aggregation, composition, and operation as methods; it links the rules [A Widget Aggregates, a Service Does One Thing](./rules/widget-aggregates/widget-aggregates.md) and [A Concept Has One Owner Module](../../knowledge/modularity/rules/one-owner/one-owner.md).
- Links to the GUI position in `sdk.md`, its changelog excepted, and in this module's handoff now point at `gui.md`.

#### Considered and not done
- Renaming the module and document to `gui`: the owner's rulings of 2026-10-20 to 2026-10-22 make ui the concept and the GUI one realization, and `modules-plugable/computer/ui/gui` already exists.
- Keeping the GUI position in `ui.md` under a retitled document: it would leave the realization's position as the concept's own text.

---

### Widget state kept apart from the SDK cache; widget-related documents corrected
- Time: 2026-10-31T07:00:00Z
- Type: Changed
- Tasks:
  - memar:.agents/tasks/20261030-T151453Z-10624/: Open - the owner reviewed the applied result and asked for the precision
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) - recorded

#### What changed
- `widget/widget.md`: Stateful now means the state of the widget's own operation; a new section "State and the SDK cache" states that the SDK of a service is the only place its answers are cached and a widget never caches, with a test. `rules/widget-aggregates` carries the same bullet.
- `widget/edges/types/types.md` and `software/edges/widget/widget.md` no longer say a widget is removable with the GUI layer or that no widget module exists; `ui.handoff.md` links the store contract where it linked a missing memory anchor.

---

### The cache boundary is a rule of the service domain; the explanations link it
- Time: 2026-10-31T08:00:00Z
- Type: Changed
- Tasks:
  - memar:.agents/tasks/20261030-T151453Z-10624/: Closed - the owner asked that rules live in their owner's rules folder
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) - recorded

#### What changed
- `widget/widget.md` states the widget's state and links the rule [A Service's SDK Is the Only Place Its Answers Are Cached](../../process/service/rules/sdk-caches-answers/sdk-caches-answers.md); `rules/widget-aggregates` and the Aggregation and Composition sections link their rules instead of restating them.
