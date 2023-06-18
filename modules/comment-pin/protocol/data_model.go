/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID      //
	GroupID() gp.GroupUUID          //
	CommentPinedID() cp.CommentUUID //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// Unpin service : Hidden status to unpin a comment
