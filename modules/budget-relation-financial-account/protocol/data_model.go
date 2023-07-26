/* For license and copyright information please see the LEGAL file in the code repository */

package bsrp

import (
	"memar/protocol"

	bp "org/modules/budget/protocol"
	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	AccountID() fap.FinancialAccountUUID
	Type() Type
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
