# Transaction trade
Add watcher to specific transactions to check min or max to make a deal (sell/buy) order.

## Model
- `[transaction-[:trade_by]->(market{rule})`
- The trade-order record is declared in [data_model.kh](protocol/data_model.kh).

## Policies (rules)
- Use to send the transaction to desire matching engine
- use to register an order to e.g. exchange(an instruction to buy or sell) currencies
- A matching engine uses the orders book to determine which orders can be fully or partially executed.
- An DataModel submitted without a specified price, and sequentially matched at the best available price in the market or in other words
- if user want to limit price, must fill order-price record otherwise market price will choose for the deals.
- "can be zero to prevent sell on profit(cover order) or stopping loss" — zero `HighPrice`/`LowPrice` means no cover/stop at that level.

## Order-type vocabulary
The order types are declared in [dt-type.kh](protocol/dt-type.kh).

## Placement
- **Correct here — `modules-plugable/economics/matching_system/edges/trade` (already its home).** The module statement owns `trade` and its order vocabulary: "`trade` describes an outcome of a matching system, not the system itself" ([matching_system.md](../../matching_system.md)) — edge + order-type/level fields travel together (pluggable owns complete capability).
- **Not core `transaction`:** core moves money without knowing order books (core never knows Rule); matching semantics are the pluggable's whole reason to exist.
- **Not a new module per order type:** StopLoss/StopLimit/AllOrNone are types *on the trade edge* the matching engine interprets — parameters of this capability, not separate modules (parameters vs semantics; prefer existing homes over inventing new modules). Loop/shortcut siblings ([all_or_none](../../edges-loop/all_or_none/all_or_none.md), [fill_or_kill](../../edges-shortcut/fill_or_kill/fill_or_kill.md), [instant_withdrawal](../../edges-loop/instant_withdrawal/instant_withdrawal.md), [exchange](../../edges-shortcut/exchange/exchange.md)) stay beside it.

## Source
> Source: `modules-plugable/economics/matching_system/edges/trade/protocol/dt-type.kh` and `protocol/data_model.kh` (in code).

