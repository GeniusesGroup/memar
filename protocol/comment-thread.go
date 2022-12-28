/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// CommentThread indicate the domain record data fields.
// Comment thread name can be set by help of comment-text domain
type CommentThread interface {
	CommentID() CommentUUID          // comment domain
	ArchiveAfter() protocol.Duration //
	Time() protocol.Time             // save time
	RequestID() UserRequestUUID      // user-request domain
}

type CommentThread_StorageServices interface {
	Save(ct CommentThread) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID [16]byte) (ct CommentThread, err protocol.Error)
}
