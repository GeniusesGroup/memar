/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// CommentStatus indicate the domain record data fields.
type CommentStatus interface {
	CommentID() CommentUUID     // comment domain
	Status() Comment_Status     //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CommentStatus_StorageServices interface {
	Save(cs CommentStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (cs CommentStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Comment_Status, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

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
