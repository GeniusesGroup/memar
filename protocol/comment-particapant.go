/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// CommentParticipant indicate the domain record data fields.
type CommentParticipant interface {
	CommentID() CommentUUID         //
	UserID() up.UserUUID            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentParticipant_StorageServices interface {
	Save(dm CommentParticipant) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (dm CommentParticipant, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_UserIDs_BY_CommentID(commentID CommentUUID, offset, limit uint64) (userIDs []up.UserUUID , nv protocol.NumberOfVersion, err protocol.Error)
}
