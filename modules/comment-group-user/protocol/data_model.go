/* For license and copyright information please see the LEGAL file in the code repository */

package cgp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// each comment is immutable record and so use version mechanism to chain comments in a group.
type DataModel interface {
	UserID() up.UserUUID
	GroupID() gp.GroupUUID
	CommentID() cp.CommentUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
