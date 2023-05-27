/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentParticipant indicate the domain record data fields.
type CommentParticipant interface {
	CommentID() CommentUUID         //
	UserID() UserUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentParticipant_StorageServices interface {
	Save(cp CommentParticipant) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (cp CommentParticipant, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(userID UserUUID, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
