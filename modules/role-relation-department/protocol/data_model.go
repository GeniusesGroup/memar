/* For license and copyright information please see the LEGAL file in the code repository */

package rrdp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/department/protocol"
	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID
	Status() Status
	DepartmentID() dp.DepartmentUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
