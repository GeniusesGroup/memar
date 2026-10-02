# Buy limit

## Model

- Candidate (unconfirmed): a purchase-eligibility constraint — "limit user not buy before year a product": a user may not buy the product before some year/date boundary (pre-order or scheduled-release window).
- The edge carried its own `protocol/` (data model + storage intent) — evidence it was shaping up as edge-with-processing, not a bare label.

## Policies (rules)

- Time-bound purchase embargo: before the boundary the product is not buyable by the limited user (or by anyone, if org-wide — direction unconfirmed).
- Source note `"memar/protocol"` shows the protocol import was still commented out; the data model was empty scaffolding.

## Placement

- **Not core-by-necessity** — products and invoices work without purchase windows; ubiquitous ≠ core (payroll/VAT/POS precedent).
- **Proposed: pluggable.** Carrying its own protocol = processing semantics = module candidate (edge becomes a module when it carries independent semantics; pluggable owns edge + processing together). Two candidate homes, decide before migrating:
  1. **Rule attachment** — express as generic `(product)-[:condition_is]->(rule)` / `(user)-[:condition_is]->(rule)` with a time-window rule; then *no* dedicated module, consistent with Core never knows Rule ([rule.handoff.md](../../../../computer/rule/rule.handoff.md)). Cheapest and most consistent with [customable](../customable/customable.md) / [sell-limit](../sell-limit/sell-limit.md).
  2. **Own pluggable module** (e.g. `modules-plugable/economics/buy-limit` or an eligibility capability) — chosen only if the embargo needs storage/processing beyond what a rule already provides (partial windows, per-user grants, waiting lists).
- Not [restriction](../../../../../modules-plugable/economics/restriction/restriction.md): that module is quantity constraints, not time windows.
- Evidence of original pluggable intent: package name `pbl_p` in the source (vs `ppp` used by the core price protocol).

## Open questions

- Per-user limit vs org-wide embargo? "limit user not buy before year" — whose year, whose limit?
- Boundary semantics: calendar year, product release year, or arbitrary timestamp?
- Does the same mechanism cover `Type_PreSale` (flag marked `??` in [product.kh](../product.kh))? If yes, flag + edge must converge — one capability, not two.
- Decide rule-attachment vs own module *before* any Khayyam migration (empty abstraction must not convert).

