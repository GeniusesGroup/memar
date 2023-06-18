/* For license and copyright information please see the LEGAL file in the code repository */

package cmp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID       //
	CommentID() cp.CommentUUID //
	SaveTime() protocol.Time   //
}


