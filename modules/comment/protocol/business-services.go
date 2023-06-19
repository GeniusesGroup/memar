/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	// cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type (
	BS_Register_Request interface {
		GroupID() gp.GroupUUID
		// ReplyTo() cp.CommentUUID
		UserID() up.UserUUID
		Type() Type
	}
	BS_Register_Response interface {
		CommentID() CommentUUID
		NumberOfVersion() protocol.NumberOfVersion
	}
)
