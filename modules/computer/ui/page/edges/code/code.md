# Code

## Model

- `(page)-[:object]->(code)`
- `(rule)-[:object]->(code)`
- Candidate (unconfirmed): `GUICategories` on a page-code record — `Content()` (HTML), `Style()` (CSS), `Logic()` (JS).

## Policies (rules)

- "GUICategories indicate the domain record data fields." — the triple partitions a page record's fields into markup, style, and behavior.

## Placement

- **Correct here — the page-code attachment stays with the page capability** (source in this module's `edges/code/` folder; placement by entry point — the categories are instantiated on a page's code record; pluggable keeps edge and its fields together).
- **Not a new module:** HTML/CSS/JS are the web dialect of page projection; a naming quibble ("GUI categories under page/code") is not a module boundary (prefer existing homes over inventing new modules).
- **Not core `computer`:** page itself is removable (stated in [page.md](../../page.md)) — the categories travel with it.

## Open questions

- Naming: "GUI categories" hosted under page/code — a page-specific name, or a shared GUI vocabulary that `widget` and the `gui/page-*` instances reuse (cf. [widget types](../../../widget/edges/types/types.md) across modules)?
- Is the Content/Style/Logic triple a projection-layer concern rather than domain data — and if so, should it sit in protocol instead of the edge?

## Source

> Source: `modules/computer/ui/page/edges/code/protocol/data_model.kh` (in code).
