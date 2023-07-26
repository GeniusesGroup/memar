/* For license and copyright information please see the LEGAL file in the code repository */

package igp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	ip "org/modules/invite/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID
	GroupID() gp.GroupUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
