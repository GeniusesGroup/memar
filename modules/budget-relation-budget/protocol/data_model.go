/* For license and copyright information please see the LEGAL file in the code repository */

package brbp

import (
	"memar/protocol"

	bp "org/modules/budget/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	OtherBudgetID() bp.BudgetUUID
	Type() Type
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
