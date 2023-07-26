/* For license and copyright information please see the LEGAL file in the code repository */

// user (delegate usage), ...
package rrup

import (
	"memar/protocol"

	rp "org/modules/role/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID
	UserID() up.UserUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
