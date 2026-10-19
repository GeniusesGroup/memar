# Widget types

## Model

- Candidate (unconfirmed): a widget-kind flag-space — `Type_Service`, `Type_Landing`, `Type_Content` — one iota list in the source; the next slot is a commented-out `// Type_`, so the set is explicitly open-ended in code.

## Policies (rules)

- No rules recorded: what a kind changes (host page? lifecycle?) is absent from the source (no bare edges).

## Placement

- **Correct here — the widget module owns its own kind vocabulary** (source in this module's `edges/` folder; a flag-space is parameters, not processing — parameters vs semantics ⇒ one widget capability plus per-organization kind configuration; no new module).
- **Not core `computer` kernel:** widget is a GUI fragment hosted by software, removable with the GUI layer (stated in [widget.md](../../widget.md)); its flags travel with it.
- Not the `gui/page-*` instance pages: these kinds classify widgets, not pages.

## Open questions

- Closed kernel set or organizational-open (low-code extensibility)? The commented-out `// Type_` slot reads as an invitation to extend.
- Do `Type_Service` / `Type_Landing` / `Type_Content` mirror the page-kind set ([page types](../../../page/edges/types/types.md)) on purpose — one GUI vocabulary with two attachment points — or two flag-spaces that will drift apart?

