# POS 
The [point of sale (POS)](https://en.wikipedia.org/wiki/Point_of_sale) or point of purchase (POP) is the time and place at which a retail transaction is completed. At the point of sale, the merchant calculates the amount owed by the customer, indicates that amount, may prepare an invoice for the customer (which may be a cash register printout), and indicates the options for the customer to make payment.

## point of service

The point of sale is often referred to as the point of service because it is not just a point of sale but also a point of return or customer order. POS terminal software may also include features for additional functionality, such as inventory management, CRM, financial, or warehousing.

## Idea backlog from edge code comments

Raw proposals from comment notes in `edges/*.go` (comments remain in code as source). Nothing below is ratified.

- **POS-to-account relations with guards** (`pos-relation-financial-account.go`): CashAccount requires the target account to carry the `cash_account` label; one cash account cannot back two POSes; also DepositAccount, RefundAccount. The exclusivity rule is an invariant candidate.
- **POS placement** (`pos-relation-estate.go`): ExactLocation vs LimitTo (area-based service: taxi, stations).
- **POS staff/group limits** (`pos-relation-staff.go`, `pos-relation-group.go`): provider/operator limiting POS to specific staff or roles.
- **Status** (`pos-status.go`): CashLimitInactivated.