/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	fap "org/modules/economics/account/protocol"
	fmp "org/modules/economics/money/protocol"
)

// DataModel indicate the domain record data fields.
// each FinancialTransaction is an immutable record and so use version mechanism to chain FinancialTransactions in AccountID way.
//
//memar:ganjine --ShardConsistency=strict
type DataModel interface {
	fap.Field_AccountID
	AccountSideID() fap.UUID
	TransactionNumber() uint64
	Amount() fmp.Amount

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
