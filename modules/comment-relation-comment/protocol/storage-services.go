/* For license and copyright information please see the LEGAL file in the code repository */

package crcp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID cp.CommentUUID) (dm DataModel, err protocol.Error)

	FIND_CommentIDs_BY_SideCommentID(sideCommentID cp.CommentUUID, offset, limit uint64) (commentIDs []cp.CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
