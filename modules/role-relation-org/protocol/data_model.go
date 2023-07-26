/* For license and copyright information please see the LEGAL file in the code repository */

package rrop

import (
	"memar/protocol"

	org "org/modules/org/protocol"
	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrganizationID() org.OrgUUID
	RoleID() rp.RoleUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
