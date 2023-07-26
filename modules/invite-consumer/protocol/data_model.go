/* For license and copyright information please see the LEGAL file in the code repository */

package icp

import (
	"memar/protocol"

	ip "org/modules/invite/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID
	PermitUsageID() up.UserUUID
	ConsumerID() up.UserUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
