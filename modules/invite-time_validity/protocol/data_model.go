/* For license and copyright information please see the LEGAL file in the code repository */

package itvp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/invite/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID
	Start() protocol.Time
	End() protocol.Time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
