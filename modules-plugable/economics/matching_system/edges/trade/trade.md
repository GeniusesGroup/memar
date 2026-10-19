# Transaction trade
Add watcher to specific transactions to check min or max to make a deal (sell/buy) order.

## Model

- `[transaction-[:trade_by]->(market{rule})`
- Trade-order record fields ([data_model.kh](protocol/data_model.kh)): `OrderID`, `Level uint8` ("usually 3 level trade order"), `HighPrice protocol.MoneyAmount // SaveProfit e.g. 45$, -102$`, `LowPrice protocol.MoneyAmount // StopLoss e.g. 43$, -95$`, `Type Type`.

## Policies (rules)

- Use to send the transaction to desire matching engine
- use to register an order to e.g. exchange(an instruction to buy or sell) currencies
- A matching engine uses the orders book to determine which orders can be fully or partially executed.
- An DataModel submitted without a specified price, and sequentially matched at the best available price in the market or in other words
- if user want to limit price, must fill order-price record otherwise market price will choose for the deals.
- "can be zero to prevent sell on profit(cover order) or stopping loss" — zero `HighPrice`/`LowPrice` means no cover/stop at that level.

## Order-type vocabulary ([dt-type.kh](protocol/dt-type.kh))

- `Type_Regular // price rules`, `Type_Trade // trade rules`, `Type_Duration`.
- `Type_AllOrNone` — "Whole order must be filled for matching deal or order must cancelled on timeout"; absent flag "allow matching engine to deal part of order" (https://en.wikipedia.org/wiki/All_or_none).
- IOC/Fill-or-kill recorded as commented derivations: `Type_ImmediateOrCancel = !Type_AllOrNone & Type_Duration` (https://en.wikipedia.org/wiki/Immediate_or_cancel), `Type_FillOrKill = Type_AllOrNone & Type_Duration` (https://en.wikipedia.org/wiki/Fill_or_kill).
- Separate const block: `Type_StopLoss // stop-loss orders guarantee execution`, `Type_StopLimit // stop-limit orders guarantee price` (https://en.wikipedia.org/wiki/Order_(exchange)).

## Placement

- **Correct here — `modules-plugable/economics/matching_system/edges/trade` (already its home).** The module statement owns `trade` and its order vocabulary: "`trade` describes an outcome of a matching system, not the system itself" ([matching_system.md](../../matching_system.md)) — edge + order-type/level fields travel together (pluggable owns complete capability).
- **Not core `transaction`:** core moves money without knowing order books (core never knows Rule); matching semantics are the pluggable's whole reason to exist.
- **Not a new module per order type:** StopLoss/StopLimit/AllOrNone are types *on the trade edge* the matching engine interprets — parameters of this capability, not separate modules (parameters vs semantics; prefer existing homes over inventing new modules). Loop/shortcut siblings ([all_or_none](../../edges-loop/all_or_none/all_or_none.md), [fill_or_kill](../../edges-shortcut/fill_or_kill/fill_or_kill.md), [instant_withdrawal](../../edges-loop/instant_withdrawal/instant_withdrawal.md), [exchange](../../edges-shortcut/exchange/exchange.md)) stay beside it.

## Fields

- `OrderID`, `Level`, `HighPrice` (SaveProfit), `LowPrice` (StopLoss), `Type` — see Model above; `arp.AuditLogging`, `protocol.Storage_Versioned`, `protocol.Storage_SaveTime`.

## Open questions

- Are order types rules over the trade edge or trade-edge types? (Receiving [matching_system.md](../../matching_system.md) review question — type flags asserted above; confirm against how the engine selects behavior.)
- Does Auction need a matching-engine protocol rather than a label? Auction/Vickrey/GTC appear only in the domain backlog prose (and market prose in [matching_system.md](../../matching_system.md) intro — "auction where matching is done at fixed intervals"), NOT in the cited `protocol/*.kh` sources — no code source of record; record provenance before ratifying (StopLoss/StopLimit/IOC ARE in `protocol/dt-type.kh`).
- `fill_or_kill`/`all_or_none` as types here vs their loop-edge siblings — type flag and loop edge: one meaning, two expressions? (Domain Unresolved also asks fill_or_kill vs all_or_none: genuine difference or duplicate labels?)
- `Type` const blocks: StopLoss/StopLimit restart `iota` in a second block (values overlap `Type_Unset`=0) — naming/values quirk to resolve at implementation pass.
- Is a party's currently stated offer to sell a currency — an ask in this order book — a priced thing that a [price-index component](../../../price-index/edges/component/component.md) or a [replacement-cost source](../../../replacement-cost/edges/source/source.md) may point at and follow, so a basket can hold the US dollar's price in rial? It must respect the [money](../../../money/money.md#unresolved-questions) model; open there and in [price index](../../../price-index/price-index.md#unresolved-questions).

## Source

> Source: `modules-plugable/economics/matching_system/edges/trade/protocol/dt-type.kh` and `protocol/data_model.kh` (in code).

