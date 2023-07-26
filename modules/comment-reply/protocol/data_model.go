/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID
	ReplyTo() cp.CommentUUID // Comment can be reply to other comment just in the same group.

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
