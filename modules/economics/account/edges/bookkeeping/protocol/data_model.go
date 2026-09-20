/* For license and copyright information please see the LEGAL file in the code repository */

package bookkeeping_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	fa_p "org/modules/economics/account/protocol"
	ft_p "org/modules/economics/transaction/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	fa_p.Field_AccountID
	// TODO::: Add bookkeeping edge type
	ft_p.Field_FinancialTransactionUUID

	Field_TransactionIndex
	Field_Balance

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
