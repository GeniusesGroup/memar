/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// CommentObject indicate the domain record data fields.
// Object can be any such as image, video, voice, ...
type CommentObject interface {
	CommentID() CommentUUID         //
	ObjectID() ObjectUUID           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CommentObject_StorageServices interface {
	Save(dm CommentObject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID CommentUUID, vo protocol.VersionOffset) (dm CommentObject, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_CommentIDs_BY_ObjectID(objectID ObjectUUID, offset, limit uint64) (commentIDs []CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

