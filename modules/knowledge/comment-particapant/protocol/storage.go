/* For license and copyright information please see the LEGAL file in the code repository */

package cpp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID cp.CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID cp.CommentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_UserIDs_BY_CommentID(commentID cp.CommentUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
