# Transaction reference
Transaction reference or `is_financial_settlement_for` use in relation to any domain to track for any purpose like invoice payment, ...

## Model

- `(transaction)-[:transaction_reference_is]->(thing)`
- `(thing)-[:financial_transaction_is]->(transaction)`

## Policies (rules)

- domains like `Budget`, `Contract`, `Order`, ...
- `batch` for `Invoice` for `product_inventory` purpose
- CAN relate multiple transactions for the same reference.
- It can't be changed after registered for any reason. The transaction MUST get `ReadOnly` label.
- Referencing MUST be automatic process.

## Fields

## Reference types

Candidate label set on `transaction_reference_is` (unconfirmed placement: labels on this edge vs originating domains):

- Accepted list: TransactionFee, Prize, Donate, Charity, Tip, Commission, Reward, Profit, Credit, Loan, BadDebt (debt default), Installment, Compensation, RentalFee, Bill, Asset, Stock, Invoice (both buy and refund via ReturnInvoice).
- Explicitly rejected in source comments: RevolvingFund, SameBankTransfer, ForeignBankTransfer, POSTransfer, WebTransfer — "Due to digital era banking, prefer to not support cash transactions" / "Not the goal and just the way of transaction that can check by RequestID".
- Budget labels recorded with these reference types (likely budget vocabulary, not reference types): Materials, Labor, Investments (Equipment), Markup (the % added to the cost to determine the wholesale price), WholesaleProfit, Margin (the % of product price to determine the retail price), RetailProfit, Cost.

## Open questions

- Do reference types belong to the reference edge (`transaction_reference_is`) as labels, or to the originating domains?
- Are the budget labels the budget module's data instead (converge with [budget](../../../../../modules-plugable/economics/budget/budget.md) Open questions — one home for the shared Materials/Labor list)?
- The Item-ingredient and item-seat business-service comments (listing query services) are data-model pass material.

