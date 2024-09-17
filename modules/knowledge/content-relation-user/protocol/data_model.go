/* For license and copyright information please see the LEGAL file in the code repository */

package crup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/content/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ContentID() cp.ContentUUID
	UserID() up.UserUUID
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
