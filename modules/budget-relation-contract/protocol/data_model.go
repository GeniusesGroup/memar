/* For license and copyright information please see the LEGAL file in the code repository */

package brcp

import (
	"memar/protocol"

	bp "org/modules/budget/protocol"
	cp "org/modules/contract/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	ContractID() cp.ContractUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
