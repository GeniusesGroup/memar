# Currency

## Model

- `(---)-[:currency]->(count_unit)`
- Candidate (unconfirmed): currency as a count-unit label carrying a `DecimalNumber` convention (e.g. `8099 >> 80.99`) and a settlement-reference `Domain` field (mediatype precedent noted in the source).

## Policies (rules)

- Decimal scaling sketch: `8099 >> 80.99` — who reads/writes decimal placement: see Placement.
- Settlement reference: "Clearing and Settlement. MoneySettlementReference can be any org or society user." — a settlement edge already owns this (see Placement).
- No who-may-set/what-it-triggers recorded — without those semantics the label must not be ratified (no bare edges).

## Placement

- **The `currency` label attachment stays here** — it marks a count-unit *as* a money unit; the [count_unit](../../count_unit.md) edge owns its unit labels (prefer the existing home — the label rides the unit this module already stores).
- **Decimal placement belongs to the money module, not the count-unit edge** — [money](../../../../../../../modules-plugable/economics/money/money.md) already decides it: the `Amount` decimal convention is "per-currency code inside this module, not graph edges" (this answers the standing review question the thing backlog used to hold).
- **The settlement-reference field must not be re-created here** — settlement already owns [settlement_reference](../../../../../../../modules-plugable/economics/settlement/edges/settlement_reference/settlement_reference.md); a duplicate field on the currency label would fork a pluggable's complete capability.
- Not a new module: decimal convention is a per-currency parameter list (parameters vs semantics ⇒ one module + configuration).

## Open questions

- If decimal placement and the settlement reference both live elsewhere, what does the currency label itself still carry beyond "this count-unit is a money unit" — strip the fields (parameter recipe to strip)?
- Direction and naming unconfirmed — nothing ratified.

