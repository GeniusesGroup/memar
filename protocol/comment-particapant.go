/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// CommentParticipant indicate the domain record data fields.
type CommentParticipant interface {
	CommentID() CommentUUID     // comment domain
	UserID() protocol.UserID    // ForwardedCommentID
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CommentParticipant_StorageServices interface {
	Save(cp CommentParticipant) (nv protocol.NumberOfVersion, err protocol.Error)
	
	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (cp CommentParticipant, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(userID [16]byte, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
