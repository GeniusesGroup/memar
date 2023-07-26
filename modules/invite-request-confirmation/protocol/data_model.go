/* For license and copyright information please see the LEGAL file in the code repository */

package ircp

import (
	"memar/protocol"

	ip "org/modules/invite/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID
	AccepterID() up.UserUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
