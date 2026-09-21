# Exchange fill_or_kill
[Fill or kill](https://en.wikipedia.org/wiki/Fill_or_kill) is an order that must be executed immediately"—a few seconds, customarily—in its entirety; otherwise, the entire order is cancelled; no partial fulfillments are allowed.

## Model

- `(transaction)-[:fill_or_kill]->(___)`
- `(time)<-[:duration]-(transaction)-[:all_or_none]->(___)`

## Policies (rules)

- Type_FillOrKill = Type_AllOrNone & Type_Duration
- Fill-or-Kill Budget (FOK-B)

## Fields
