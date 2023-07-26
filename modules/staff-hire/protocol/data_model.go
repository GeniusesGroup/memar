/* For license and copyright information please see the LEGAL file in the code repository */

package shp

import (
	"memar/protocol"

	rp "org/modules/role/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	RoleID() rp.RoleUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
