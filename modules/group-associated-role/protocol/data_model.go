/* For license and copyright information please see the LEGAL file in the code repository */

package garp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gp "org/modules/group/protocol"
	rp "org/modules/role/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID
	UserID() up.UserUUID
	RoleID() rp.RoleUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
