/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"

	// arp "org/modules/app-request/protocol"
	cp "org/modules/comment/protocol"
)

// DataModel indicate the domain record data fields.
// It must just use to index hashtag words from comment-text domain
type DataModel interface {
	Tag() string
	CommentID() cp.CommentUUID

	// arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
