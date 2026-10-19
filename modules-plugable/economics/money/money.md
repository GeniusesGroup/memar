# Money

Money is pluggable: a count unit like any other. Currencies are declared through the general `(thing)-[:count_unit_is]->(count_unit)` edge (with the `currency` label under `identity/thing`), so the accounting kernel needs nothing from this module. What lives here is money-specific representation only: amount types, per-currency decimal scaling, formatting.

## Model

- `Money` = `Field_Amount` + `currency_p.Field_FinancialCurrencyID` — a typed pairing of quantity and currency for GUI/service convenience, not a new accounting primitive.
- `Amount` is the kernel's quantity (`decimal_p.Quantity`), not a second quantity type; the currency's decimal convention (e.g. `8099` → `80.99$`) is per-currency code inside this module, not a graph edge and not part of the amount's type. Settled 2026-10-03 — the legacy representation was an `int64` scaled by a power of ten, and the reconciliation with the quantity representation bookkeeping already uses is recorded in [money.handoff.md](money.handoff.md) together with its costs.

## Discussion

### Drawbacks

- "Money-ness" is split across two places: currencies under `identity/thing`, amount/precision code here.

### Rationale and alternatives

- Money-as-core was rejected: transactions are unit-general (shares, kg, points); a money-first core was the legacy framing this redesign removed. Core-by-necessity (not prevalence) decides what stays in `modules/` — money fails that test.
- Exchange rates rejected as stored facts: a rate is discovered/derived from past trades — a hint, not a guarantee — so it is analytics territory, not module state.
  - Note (owner's reading, 2026-10-10): this rejection concerns the design of the project's own currency — not repeating the mistake of a gold standard pegged through the US dollar; money, if debt-based, must be modeled precisely ([credit](../credit/credit.md)). It is not a statement about evaluating prices against currencies or baskets, which [price index](../price-index/price-index.md) and [replacement cost](../replacement-cost/replacement-cost.md) do.
- Per-currency precision as edges was rejected: it is a data-type property, hence internal packages. NOTE: precision is NOT display-only — decimal precision and rounding rules affect which operations are creditable/valid (an amount that rounds away is a real economic difference), so they are domain-affecting, not GUI concerns.

### Prior art

- ISO 4217 currency codes already live as a `uri` module; this module consumes, not redefines, them.

### Unresolved questions

- Does `money` need to exist at all, or should amount/precision move to consumers of `memar/math/decimal`?
- Define the rounding/precision contract per currency (banker's rounding vs half-up, when truncation is legal) — this must be settled before fee/interest rules are trusted with real balances.
- Nothing states how `Money` holds the amount to its currency's scale: the pairing requires both halves and nothing connects them.
- How is a currency's price — the US dollar in rial — represented as a priced thing that a [price-index component](../price-index/edges/component/component.md) or a [replacement-cost source](../replacement-cost/edges/source/source.md) may point at: a dealer's or an exchange's currently stated offer to sell (an ask on [trade](../matching_system/edges/trade/trade.md)), a product whose price is stated in the graph, or something this module must define? It must respect this module's model of the project's own currency (see the note under Rationale and alternatives); the same question is open in [price index](../price-index/price-index.md#unresolved-questions) and [replacement cost](../replacement-cost/replacement-cost.md#unresolved-questions).

### Future possibilities

- Crypto units (variable decimals, e.g. satoshi) as sibling packages under the same pattern.

## Idea backlog

Nothing below is ratified.

### Planned package errors
- **Idea**: planned package errors `ErrBadCurrency`, `ErrInvalidTerminalID`, `ErrNotEnoughBalance`, each initialized with a URI — `domain/memar.scm.geniuses.group; package=money; type=error; name=bad-currency` / ` ... name=invalid-terminal-id` / ` ... name=not-enough-balance` (the whole file was commented-out scaffolding; the locale files remain in [locale.eng.kh](errors/locale.eng.kh)).
- **Review questions**: who raises each error — this module's amount/precision code, or consuming services (a *terminal* is a POS concept, not money representation; see [pos](../pos/pos.md))? Is the error set closed at these three or open for extension?
