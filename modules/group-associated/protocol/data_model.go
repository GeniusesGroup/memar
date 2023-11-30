/* For license and copyright information please see the LEGAL file in the code repository */

package gap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields
type DataModel interface {
	GroupID() gp.GroupUUID
	UserID() up.UserUUID
	JoinBy() up.UserUUID
	JoinWay() JoinWay

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
