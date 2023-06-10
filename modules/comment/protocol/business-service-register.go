/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	csp "org/modules/comment-settings/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type (
	Comment_Service_Register_Request interface {
		GroupID() gp.GroupUUID
		ReplyTo() [16]byte
		UserID() up.UserUUID
		Type() Comment_Type
		Settings() csp.Comment_Settings
	}
	Comment_Service_Register_Response interface {
		CommentID() CommentUUID
		NumberOfVersion() protocol.NumberOfVersion
	}
)
