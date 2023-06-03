/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentCommentRelation indicate the domain record data fields.
type CommentCommentRelation interface {
	CommentID() CommentUUID     //
	SideCommentID() CommentUUID //
	// Type()
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentCommentRelation_StorageServices interface {
	Save(dm CommentCommentRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID CommentUUID) (dm CommentCommentRelation, err protocol.Error)

	FIND_CommentIDs_BY_SideCommentID(sideCommentID CommentUUID, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

