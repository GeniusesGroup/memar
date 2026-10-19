# Money Handoff

Load-bearing state for the money module: the amount representation decision, what the conversion left out, and the questions that are still open. Paired with [money.md](money.md), which owns the model and the placement argument.

## Status

Active — the amount representation is settled and the protocol is converted; the per-currency rounding contract and the module's own necessity are still open.

## Khayyam conversion (2026-10-03)

Converted:

- `protocol/dt-money-amount.kh` — `tp Amount ab { Decimal_Quantity }`, `tp Field_Amount ab`, `tp MoneyAmount mt (self Field_Amount) () (a Amount)`.
- `protocol/money.kh` — `tp Money ab { Field_Amount Field_FinancialCurrencyID }`, with `Field_Amount` included from the file above and `Field_FinancialCurrencyID` included from `identity/thing/edges/count_unit/labels/currency/protocol/dt-uuid.kh`.

Both return `accept` from the Khayyam frontend.

## Decisions

### The amount is the kernel's quantity, not a scaled `int64`

`money.md` carried this as an unresolved question — *"`int64` scaling vs `decimal_p.Quantity` used on bookkeeping fields — reconcile the two quantity representations"* — and it is now settled: **`Amount` is `Decimal_Quantity`**. The repository has one quantity representation.

What the evidence said, in order of weight:

1. **The document already de-fanged the `int64`.** The `Money` bullet says the pairing of quantity and currency is "a typed pairing of quantity and currency for GUI/service convenience, **not a new accounting primitive**." If money's amount were a separate accounting primitive, that sentence would be false. The `int64` line in the same section describes the *legacy representation*, not the concept.
2. **Core had already converged on `Decimal_Quantity` before money was converted.** `account/edges/bookkeeping/protocol/dt-balance.kh` values `Field_Balance` as `Decimal_Quantity`; `transaction/edges/account-from/protocol/data_model.kh` composes `Observer_Quantity`, which memar values as `Decimal_Quantity`. The kernel side of the "reconcile" was already done — the reconciliation is money's half, or money's half is deletion.
3. **A `Decimal_Quantity` cannot express a currency's scale, and neither can an `int64`.** `Math_Decimal` in memar is a signed integer plus a `W64` fraction — a fixed-scale decimal, the .NET shape, not a per-currency one. The legacy `int64` was no better: `Amount(8099)` is meaningless without the currency's decimal exponent, and `money.md` itself says the exponent is "per-currency code inside this module". So in both readings the scale lives beside the amount, not in it. Only the *representation* of the scaled value was ever in dispute.
4. **Keeping the `int64` would have made core import a pluggable.** Twenty-six files name `money_p.Amount`, including two core ones — `economics/product/edges/price/protocol/*` and `economics/invoice/edges/item/protocol/*`. `money.md`'s placement argument is that money is deliberately outside core and that "the accounting kernel needs nothing from this module". An `Amount` that is a second, `int64`-based quantity type can only be named by importing money, so core would depend on a capability any organization may not install. Choosing `Decimal_Quantity` is what lets the kernel say "quantity" without saying "money".

Cost of this choice, stated plainly:

- The module's remaining content shrinks. What is left here after this decision is the pairing and the per-currency scale code — and `money.md`'s own first unresolved question asks whether *that* justifies a module at all ("Does `money` need to exist at all, or should amount/precision move to consumers of `memar/math/decimal`?"). This decision makes that question sharper, not answered.
- Per-currency precision stops being a type property. `money.md` insists precision is "domain-affecting, not GUI concerns", and it still is — but it is now the scale *code* beside the pairing, so nothing in the type system stops a consumer from pairing an amount with a currency whose exponent it ignored. That guard has to be built into the pairing's realization, and it is not built yet (see below).
- Migrating the legacy arithmetic (`internal/amount.kh`, integer division on a scaled value) to decimal semantics changes results at the rounding edge. Nothing in the tree depends on those results today — the only caller is a test — so the cost is currently zero and the risk is deferred to whoever implements it.

### `MoneyAmount` kept the Go's name

`Field_Amount`'s accessor is `MoneyAmount`, not `Amount`. The suffix convention (`Field_X` + `X`) would ask for `Amount`, and that name is the value type in the same file: two declarations, one word. `MoneyAmount` is the author's own spelling in the Go, it carries the module qualifier that resolves the collision (the same shape as `Field_ThingUUID` → `ThingID` beside the `ThingUUID` type, and `Field_FinancialCurrencyID` → `FinancialCurrencyID` beside `ThingUUID`), and it is not otherwise claimed in the corpus. Recorded here because it is a judgment call the repository-wide suffix sweep will otherwise have to rediscover.

### The arithmetic stayed in `internal/`

`internal/amount.kh` implements `PerCent`, `PerMille`, `PerMyriad` and `Root` on the internal amount. None was moved onto `Amount` in the protocol, because `money.md` records the rounding contract as unsettled — *"Define the rounding/precision contract per currency (banker's rounding vs half-up, when truncation is legal) — this must be settled before fee/interest rules are trusted with real balances"*. Declaring those four on the protocol would put a requirement on every realization and ratify a policy the document has explicitly not settled. They stay implementation-layer behaviour (Phase 3).

## Unconverted, and what blocks it

- **`internal/amount.kh`, `internal/price.kh`** — implementation layer. `amount.kh` is four arithmetic operations plus a formatter, and `price.kh` is a two-field capsule that the protocol's `Money` abstraction already covers (`Field_Amount` + `Field_FinancialCurrencyID`). Both are re-modeled work, not conversion work. Nothing else in the tree needs them today.
- **`internal/amount_test.kh`** — a test, and the disposition for tests is re-derivation from behaviour. Its single case (`209000` at per-myriad 9 → `17257`) is worth keeping as the regression test for `Root` once the rounding contract is settled, because it pins the truncation direction of the legacy integer division.
- **`errors/locale.eng.kh`, `errors/locale.per.kh`** — locale registration for three errors that do not exist. `money.md` lists them under "Idea backlog" with the note "Nothing below is ratified", and its review question — *who raises each error, this module's amount/precision code or the consuming services* — is still open; the same bullet already answers part of it by observing that a *terminal* is a POS concept, not money representation. Declaring `Money_Error_BadCurrency` and friends as capsules (the shape `knowledge/text/errors/errors.kh` already uses) would ratify an unratified idea. Left as the document has it.

## Open from this pass

- **`Amount` is currently structurally identical to `Decimal_Quantity`.** `Decimal_Quantity` in memar is `tp Decimal_Quantity ab` with no requirements, so it is vacuously satisfied; `Amount ab { Decimal_Quantity }` inherits that, and under implicit structural satisfaction any quantity would pass where an amount is expected — 3.5 kg of steel is a `Decimal_Quantity` and therefore an `Amount`. This is the accidental-satisfaction risk named in `docs/khayyam/abstraction.md`, and it is the direct cost of the decision above. Two ways out, both outside this module: `Decimal_Quantity` gains real requirements (memor's file, memar's call), or money drops `Amount` and the twenty-six consumers name `Decimal_Quantity` directly. Until one happens, `Amount` is a name that reads as money and is checked as a number.
- **The pairing carries no scale guard.** `Money` requires both a currency and an amount but nothing connects them, so nothing stops a realization from pairing a KWD amount (three decimals) with a JPY currency. `money.md` says precision is domain-affecting; the type that must express that is `Money`, and it currently does not. What it needs is a requirement stating that the amount is on the named currency's scale, and a realization that fails when it is not.
- **The file name typo is fixed.** `protocol/dt-money-amout.kh` is renamed `dt-money-amount.kh`, and the imports in `money.kh`, `discount` and `voucher` name the new file.
- **The twenty-six stale import paths.** Every one of them says `modules/economics/money/protocol` (or, for `product/edges/price/protocol/data_model.kh`, `modules/fields/money/protocol` — a path this repository has never had). The module is at `modules-plugable/economics/money/`, and `money.md` places it outside core deliberately. Repointing them is a one-line change per file, outside this domain. Note that `product.handoff.md` and `invoice.handoff.md` both record this as their blocker; the blocker is now the path, not the missing type. `Field_Amount` and `Amount` are declared, so a core file that needs them may now import either from `memar/modules/math/decimal/protocol/dt-quantity.kh` (for the quantity) or, if the money spelling is wanted, from this module — and the second is a core-to-pluggable dependency that the core-vs-pluggable rubric does not sanction. The choice of which is a repository decision, not this module's.

## Related Artifacts

- [money.md](money.md) — model, placement argument, idea backlog.
- [`../pos/pos.md`](../pos/pos.md) — the terminal concept one planned error belongs to.
- [`../../../modules/economics/account/edges/bookkeeping/bookkeeping.md`](../../../modules/economics/account/edges/bookkeeping/bookkeeping.md) — the kernel side of the quantity representation this module now shares.
