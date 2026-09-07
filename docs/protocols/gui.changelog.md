# GUI Changelog

## Changelog

### Architecture position added: three separations, widget model, page state, network silence, shared validation
- Time: 2026-09-06T00:00:00Z
- Type: Expanded
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
The GUI protocol gained its architectural position: three-way separation, widget-based model, protocol-level page state and history, single routing authority, SDK-mediated service access, and once-generated shared validation.

The positions were brought from public GUI-architecture discussions (the front-end gafteman sessions and their written continuation): the content/presentation/logic three-way separation as the web standards' one proven idea; the widget/component distinction (widget: single named instance acquiring its own data; component: per-use template instance with passed-in state); the History API critique (built on SSR assumptions, structureless state blobs); one routing authority per application; the GUI-does-not-speak-network rule with generated SDK as the only network-aware part; shared server/GUI validation via accessor/setter generation (Omid Hekayati).

Recording decisions (Super Z): the positions were recorded as the document's Position on GUI Architecture above the existing Page specification; the silent-on-architecture fault was linked to the modeling document's decomposition treatment; the JSX/React separation-of-technologies claim was kept stated as the ecosystem's own reasoning; the existing Page/ID/URN spec was preserved untouched below the new position.
