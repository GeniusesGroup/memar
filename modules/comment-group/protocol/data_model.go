/* For license and copyright information please see the LEGAL file in the code repository */

package cgp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// each comment is immutable record and so use version mechanism to chain comments in a group.
type DataModel interface {
	GroupID() gp.GroupUUID          //
	CommentID() cp.CommentUUID      //
	UserID() up.UserUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
