/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentPin indicate the domain record data fields.
type CommentPin interface {
	CommentID() CommentUUID         //
	GroupID() GroupUUID             //
	CommentPinedID() CommentUUID    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentPin_StorageServices interface {
	Save(dm CommentPin) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID CommentUUID) (dm CommentPin, err protocol.Error)

	FIND_CommentIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_CommentPinIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (commentPinedIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// Unpin service : Hidden status to unpin a comment
