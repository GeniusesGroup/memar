/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentStatus indicate the domain record data fields.
type CommentStatus interface {
	CommentID() CommentUUID         //
	Status() Comment_Status         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentStatus_StorageServices interface {
	Save(dm CommentStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (dm CommentStatus, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Comment_Status Quiddity_Status

const (
// Comment_Status_ = Comment_Status(Quiddity_Status_FreeFlag << iota)
)

type (
	CommentStatus_Service_Register_Request interface {
		CommentID() CommentUUID
		Status() Comment_Status
	}
	CommentStatus_Service_Register_Response interface {
		// OldStatus() Comment_Status
		// NewStatus() Comment_Status
		NumberOfVersion() protocol.NumberOfVersion
	}
)
