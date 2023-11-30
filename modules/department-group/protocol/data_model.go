/* For license and copyright information please see the LEGAL file in the code repository */

package dgp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/department/protocol"
	gp "org/modules/group/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID
	GroupID() gp.GroupUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
