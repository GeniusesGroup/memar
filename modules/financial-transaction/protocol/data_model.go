/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
// each FinancialTransaction is an immutable record and so use version mechanism to chain FinancialTransactions in AccountID way.
//
//libgo:ganjine --ShardConsistency=strict
type DataModel interface {
	AccountID() fap.FinancialAccountUUID
	AccountSideID() fap.FinancialAccountUUID // or AccountPartyID
	Amount() protocol.MoneyAmount            // This transaction
	Balance() protocol.MoneyAmount           // Account balance with this transaction

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
