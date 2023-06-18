/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID      //
	ReplyTo() cp.CommentUUID        // Comment can be reply to other comment in the same group.
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


