/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// CommentForward indicate the domain record data fields.
type CommentForward interface {
	CommentID() CommentUUID     // comment domain
	ForwardedID() CommentUUID   // ForwardedCommentID
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type CommentForward_StorageServices interface {
	Save(cf CommentForward) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID [16]byte) (cf CommentForward, err protocol.Error)

	FindByForwardedID(forwardedID [16]byte, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
