/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	csp "org/modules/comment-settings/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type (
	BS_Register_Request interface {
		GroupID() gp.GroupUUID
		ReplyTo() [16]byte
		UserID() up.UserUUID
		Type() Type
		Settings() csp.Comment_Settings
	}
	BS_Register_Response interface {
		CommentID() CommentUUID
		NumberOfVersion() protocol.NumberOfVersion
	}
)
