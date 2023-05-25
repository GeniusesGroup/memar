/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentThread indicate the domain record data fields.
// Comment thread name can be set by help of comment-text domain
//
// TODO::: I think we don't need this domain. If Thread flag is on means all reply to a comment must show in a thread window.
// TODO::: It means when new comment appear in a group, instead of show comment text, just show first thread comment with some badge as new message arrived.
type CommentThread interface {
	CommentID() CommentUUID          // comment domain
	ArchiveAfter() protocol.Duration //
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  // user-request domain
}

type CommentThread_StorageServices interface {
	Save(ct CommentThread) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID [16]byte) (ct CommentThread, err protocol.Error)
}
