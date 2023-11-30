/* For license and copyright information please see the LEGAL file in the code repository */

package trpp

import (
	"memar/math/per"
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/project/protocol"
	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID
	ProjectID() pp.ProjectUUID
	Priority() uint64
	PerMyriad() per.Myriad // 0 means unset e.g. equal to other tasks in the project
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
