/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(commentID cp.CommentUUID) (dm DataModel, err protocol.Error)

	FIND_CommentIDs_BY_GroupID(groupID gp.GroupUUID, offset, limit uint64) (commentIDs []cp.CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_CommentPinIDs_BY_GroupID(groupID gp.GroupUUID, offset, limit uint64) (commentPinedIDs []cp.CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
