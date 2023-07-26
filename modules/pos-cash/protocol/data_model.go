/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel or pos operator is to supply a particular service.
type DataModel interface {
	PosID() pp.PosUUID
	AccountID() fap.FinancialAccountUUID
	MaxCash() protocol.MoneyAmount
	MaxCashTransfer() protocol.Duration // from reach the max limit

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
