/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
)

type (
	BS_Register_Request interface {
		CommentID() cp.CommentUUID
		Status() Status
	}
	BS_Register_Response interface {
		// OldStatus() Status
		// NewStatus() Comment_Status
		NumberOfVersion() protocol.NumberOfVersion
	}
)
