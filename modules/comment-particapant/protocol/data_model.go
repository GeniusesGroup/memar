/* For license and copyright information please see the LEGAL file in the code repository */

package cpp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID
	UserID() up.UserUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
