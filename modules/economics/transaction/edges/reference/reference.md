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
- Budget labels recorded with these reference types (likely budget vocabulary, not reference types): Materials, Labor, Investments (Equipment), Markup (the % added to the cost to determine the wholesale price), WholesaleProfit, Margin (the % of product price to determine the retail price), RetailProfit, Cost.

## Code correspondence
The edge record's declarations are in [data_model.kh](protocol/data_model.kh). The label vocabulary in "Reference types" above is not in code, so the candidate list currently has no owner.
