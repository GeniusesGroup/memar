/* For license and copyright information please see the LEGAL file in the code repository */

package tup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	GroupID() gp.GroupUUID // generate for group & comment domain
	Priority() uint64
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
