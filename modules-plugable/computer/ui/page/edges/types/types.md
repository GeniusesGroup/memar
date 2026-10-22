# Page types

## Model

- Candidate (unconfirmed): a page-kind flag-space — `Service`, `Landing`, `Content`, `Email`, `Print` — one iota list in the source, so one flag set rather than five edges.

## Policies (rules)

- No rules recorded: what a kind changes (template? renderer? lifecycle?) is absent from the source (no bare edges).

## Placement

- **Correct here — the page module owns its own kind vocabulary** (source cited under this module's `edges/`; a flag-space is a parameter list, not processing semantics — parameters vs semantics ⇒ one page capability plus per-organization kind configuration; no new module).
- **Not core `computer` kernel:** page is a removable projection capability (stated in [page.md](../../page.md)); its flags travel with it.
- **Not the `gui/page-*` instance pages:** instance pages are deployments of these kinds, not owners of the vocabulary (`modules-plugable/gui/page-*` renders org domains).

## Open questions

- Closed set or organizational-open (low-code extensibility)?
- Is `Print` a page kind or a rendering target?

