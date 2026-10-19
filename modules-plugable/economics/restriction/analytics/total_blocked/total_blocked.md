# total_blocked

## Dictionary

## Model

- `(user)-[:total_blocked]->(---)`

## Policies (rules)

## Fields

<!--
TODO::: below field seems to be a cache field not truth of source field!??
AvailableBalance is actual balance minus any pending transactions
e.g. block by justice, block for pending transaction, ...
-->
	AvailableBalance() decimal_p.Quantity
