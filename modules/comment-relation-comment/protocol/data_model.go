/* For license and copyright information please see the LEGAL file in the code repository */

package crcp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/comment/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID
	SideCommentID() cp.CommentUUID
	// Type()

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
