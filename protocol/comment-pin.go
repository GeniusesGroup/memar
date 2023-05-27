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
	Save(cp CommentPin) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID [16]byte) (cp CommentPin, err protocol.Error)

	FindByGroupID(groupID [16]byte, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// Unpin service : Hidden status to unpin a comment
