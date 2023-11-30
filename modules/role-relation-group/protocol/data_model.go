/* For license and copyright information please see the LEGAL file in the code repository */

package rrgp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gp "org/modules/group/protocol"
	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID
	GroupID() gp.GroupUUID
	// Type()
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
