/* For license and copyright information please see the LEGAL file in the code repository */

package brpp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	bp "org/modules/budget/protocol"
	pp "org/modules/project/protocol"
	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	ProjectID() pp.ProjectUUID
	TaskID() tp.TaskUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
