/* For license and copyright information please see the LEGAL file in the code repository */

package rap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID
	AccessControl() protocol.AccessControl

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
