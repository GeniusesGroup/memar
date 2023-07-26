/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
)

// CommentText indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID
	Text() string // Text With Style. HTML & CSS (No JS) is more expressive than markdown, suggest use them in article text to style text.

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
