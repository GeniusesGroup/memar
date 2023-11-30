/* For license and copyright information please see the LEGAL file in the code repository */

package fsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	up "org/modules/user/protocol"
)

// Individual and General score
type DataModel interface {
	UserID() up.UserUUID
	Score() int64

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
