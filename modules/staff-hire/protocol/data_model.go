/* For license and copyright information please see the LEGAL file in the code repository */

package shp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	rp "org/modules/role/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	RoleID() rp.RoleUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
