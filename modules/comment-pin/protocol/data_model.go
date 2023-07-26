/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID
	GroupID() gp.GroupUUID
	CommentPinedID() cp.CommentUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// Unpin service : Hidden status to unpin a comment
