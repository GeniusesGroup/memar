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
