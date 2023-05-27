/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// CommentMentioned indicate the domain record data fields.
type CommentMentioned interface {
	UserID() UserUUID       //
	CommentID() CommentUUID //
	Time() protocol.Time    // save time
}

type CommentMentioned_StorageServices interface {
	Save(cm CommentMentioned) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, vo protocol.VersionOffset) (cm CommentMentioned, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
