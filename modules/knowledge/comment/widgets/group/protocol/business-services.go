/* For license and copyright information please see the LEGAL file in the code repository */

package cgp

import (
	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
)

type (
	BS_Register_Request interface {
		GroupID() gp.GroupUUID
		CommentID() cp.CommentUUID
	}
)
