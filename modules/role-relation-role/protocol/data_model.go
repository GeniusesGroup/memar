/* For license and copyright information please see the LEGAL file in the code repository */

package rrrp

import (
	"memar/protocol"

	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID
	OtherID() rp.RoleUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
