/* For license and copyright information please see the LEGAL file in the code repository */

package brdp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	bp "org/modules/budget/protocol"
	dp "org/modules/department/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	DepartmentID() dp.DepartmentUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
