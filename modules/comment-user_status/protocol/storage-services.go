/* For license and copyright information please see the LEGAL file in the code repository */

package cus

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID cp.CommentUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID cp.CommentUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO::: get view number
}
