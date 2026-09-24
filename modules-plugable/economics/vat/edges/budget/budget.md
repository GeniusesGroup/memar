# Tax relation budget

## Model

- Candidate (unconfirmed): `(tax)-[:relation_budget]->(budget)` carrying the label `IncomeTax` (direction unconfirmed).

## Policies (rules)

- Only `IncomeTax` recorded — what the link does (budget receives tax revenue? tax debited from a budget line?), absent from the source (no bare edges).

## Placement

- **Correct here — the tax-budget link is instantiated from the tax capability** (placement by entry point; source `vat/edges/tax-relation-budget.go`, deleted at `334d6e2c` 2026-09-09; pluggable owns complete capability — edge + any settlement rules that read it live together).
- **Not the budget module's own edge:** budget is the planning map ("JUST a map for future planning" — [budget edge](../../../budget/edges/budget/budget.md)); the tax side initiates where revenue lands — one owner, the capability that gives the edge meaning (shortcut-edge ownership rule; prefer existing homes over inventing new modules).
- **Not core transaction:** a tax→budget binding is tax-domain vocabulary; core transaction moves money without knowing taxes (core never knows Rule; fees-as-rules precedent in [rule.handoff.md](../../../../../modules/computer/rule/rule.handoff.md) §9).
- **Not a new module:** one labeled relation is parameters, not independent processing (parameters vs semantics).

## Open questions

- Direction and meaning: tax revenue flows *into* a budget (`IncomeTax` as a budget income kind), or a budget *funds* a tax line?
- Does this duplicate general `(budget)-[:budget]->(---)` attachment ([budget edge](../../../budget/edges/budget/budget.md) — "It CAN relate to `production`, `department`, `group`") with tax as one more related subject? Converge to one attachment vocabulary.
- Who may set the link, and what does it trigger (revenue posting? forecasting entry?) — no-bare-edges test open.
- Direction/naming unconfirmed — nothing ratified.

