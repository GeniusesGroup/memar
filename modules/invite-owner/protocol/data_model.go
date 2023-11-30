/* For license and copyright information please see the LEGAL file in the code repository */

package iop

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/invite/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID
	IssuerID() up.UserUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
