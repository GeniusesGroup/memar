/* For license and copyright information please see the LEGAL file in the code repository */

package fat_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	fa_p "org/modules/financial/account/protocol"
	money_p "org/modules/financial/money/protocol"
	ft_p "org/modules/financial/transaction/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	fa_p.Field_FinancialAccountID
	Field_TransactionIndex
	ft_p.Field_FinancialTransactionID

	money_p.Field_Amount

	// Balance or ActualBalance or EffectiveBalance or CurrentBalance
	// is the total of all the transactions on the account including any pending transactions.
	Balance() money_p.Amount

	// TODO::: below field seems to be a cache field not truth of source field!??
	// AvailableBalance is actual balance minus any pending transactions
	// e.g. block by justice, block for pending transaction, ...
	AvailableBalance() money_p.Amount

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
