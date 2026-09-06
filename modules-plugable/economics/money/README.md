# Money

Money is pluggable: a count unit like any other. Currencies are declared through the general `(thing)-[:count_unit_is]->(count_unit)` edge (with the `currency` label under `identity/thing`), so the accounting kernel needs nothing from this module. What lives here is money-specific representation only: amount types, per-currency decimal scaling, formatting.

## Model

- `Money` = `Field_Amount` + `currency_p.Field_FinancialCurrencyID` — a typed pairing of quantity and currency for GUI/service convenience, not a new accounting primitive.
- `Amount` is an `int64` scaled by the currency's decimal convention (e.g. `8099` → `80.99$`); precision handling is per-currency code inside this module, not graph edges.

## Discussion

### Drawbacks

- "Money-ness" is split across two places: currencies under `identity/thing`, amount/precision code here.

### Rationale and alternatives

- Money-as-core was rejected: transactions are unit-general (shares, kg, points); a money-first core was the legacy framing this redesign removed (see [core-vs-pluggable.md](../../../modules/economics/core-vs-pluggable.md)).
- Exchange rates rejected as stored facts: a rate is discovered/derived from past trades — a hint, not a guarantee — so it is analytics territory, not module state.
- Per-currency precision as edges was rejected: it is a data-type property, hence internal packages. NOTE: precision is NOT display-only — decimal precision and rounding rules affect which operations are creditable/valid (an amount that rounds away is a real economic difference), so they are domain-affecting, not GUI concerns.

### Prior art

- ISO 4217 currency codes already live as a `uri` module; this module consumes, not redefines, them.

### Unresolved questions

- Does `money` need to exist at all, or should amount/precision move to consumers of `memar/math/decimal`?
- `int64` scaling vs `decimal_p.Quantity` used on bookkeeping fields — reconcile the two quantity representations.
- Define the rounding/precision contract per currency (banker's rounding vs half-up, when truncation is legal) — this must be settled before fee/interest rules are trusted with real balances.

### Future possibilities

- Crypto units (variable decimals, e.g. satoshi) as sibling packages under the same pattern.
