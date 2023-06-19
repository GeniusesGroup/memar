/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type (
	BS_Register_Request interface {
		GroupID() gp.GroupUUID
		ReplyTo() cp.CommentUUID
		UserID() up.UserUUID
		Type() cp.Type
		Settings() Settings
	}
	BS_Register_Response interface {
		CommentID() cp.CommentUUID
		NumberOfVersion() protocol.NumberOfVersion
	}
)
