# Budget

## Model

- `(account)-[:budget_for]->(thing)`
- `(account)-[:invoice]->(budget)`
- `(account)-[:transaction]->(budget)`
- `(account)-[:budget_for]->(user)`
- `(account)-[:contract]->(budget)`
- `(account)-[:task]->(budget)`

## Policies (rules)

- Budget Usage:
  - Shareholders can see org profit and decide to sell or buy more stocks.
  - Country Governments: need to steal organizations profits by the name of law as Tax, ...! so force them to implement these services.
  - Stock Markets: need to show related data to traders to know the quality of organizations in making profit.
- Limit the account to accept certain transaction types — Materials, Labor, Investments ([LinkedIn: 5 budgeting methods](https://www.linkedin.com/pulse/5-budgeting-methods-everyone-should-know-about-advantages-ehab-sobhy/)); Budget kinds: Budget, Budget_Zero_based, Budget_Incremental, Budget_Activity_Based, Budget_Value_Proposition, Budget_Flexible.
- Budget labels: Blocking, Continuous, Withdrawal, Deposit.

## Open questions

- Are the Materials/Labor/Investments budget labels the budget module's data, or reference-type labels on the transaction side? The same list rides the transaction shortcut comments — converge with [reference](../../../modules/economics/transaction/edges/reference/reference.md) (Reference types → Open questions), one home.
- Budget statuses Executed/Inspected (from the transaction status-labels backlog): this module's vocabulary or general status domain ([status](../../../modules/knowledge/status/status.md))?
