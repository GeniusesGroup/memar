/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentReply indicate the domain record data fields.
type CommentReply interface {
	CommentID() CommentUUID         //
	ReplyTo() CommentUUID           // Comment can be reply to other comment in the same group.
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentReply_StorageServices interface {
	Save(sf CommentReply) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (sf CommentReply, nv protocol.NumberOfVersion, err protocol.Error)

	FindByReplyTo(replyTo CommentUUID, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
