/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// each FinancialTransaction is an immutable record and so use version mechanism to chain FinancialTransactions in AccountID way.
//
//libgo:ganjine --ShardConsistency=strict
type DataModel interface {
	AccountID() fap.FinancialAccountUUID     //
	AccountSideID() fap.FinancialAccountUUID // or AccountPartyID
	Amount() protocol.MoneyAmount            // This transaction
	Balance() protocol.MoneyAmount           // Account balance with this transaction
	SaveTime() protocol.Time                 //
	RequestID() urp.UserRequestUUID          //
}
