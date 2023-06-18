/* For license and copyright information please see the LEGAL file in the code repository */

package cpp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID      //
	UserID() up.UserUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

