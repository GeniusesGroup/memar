/* For license and copyright information please see the LEGAL file in the code repository */

package cgp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// each comment is immutable record and so use version mechanism to chain comments in a group.
type DataModel interface {
	GroupID() gp.GroupUUID
	CommentID() cp.CommentUUID
	UserID() up.UserUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
