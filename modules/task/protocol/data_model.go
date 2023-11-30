/* For license and copyright information please see the LEGAL file in the code repository */

package tp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	up "org/modules/user/protocol"
)

// Task indicate the domain record data fields.
type Task interface {
	TaskID() TaskUUID
	UserID() up.UserUUID
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
