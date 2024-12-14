/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fap "org/modules/financial-account/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel or pos operator is to supply a particular service.
type DataModel interface {
	PosID() pp.PosUUID
	AccountID() fap.FinancialAccountUUID
	// TODO::: move below fields to financial domains
	MaxCash() protocol.MoneyAmount
	MaxCashTransfer() protocol.Duration // from reach the max limit

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
