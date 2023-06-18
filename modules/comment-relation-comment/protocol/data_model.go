/* For license and copyright information please see the LEGAL file in the code repository */

package crcp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID     //
	SideCommentID() cp.CommentUUID //
	// Type()
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

