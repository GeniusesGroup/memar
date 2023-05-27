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
	Save(co CommentObject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID [16]byte, vo protocol.VersionOffset) (co CommentObject, nv protocol.NumberOfVersion, err protocol.Error)

	FindByObjectID(objectID [16]byte, offset, limit uint64) (commentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
