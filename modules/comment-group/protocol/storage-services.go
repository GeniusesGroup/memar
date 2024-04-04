/* For license and copyright information please see the LEGAL file in the code repository */

package cgp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
	gp "org/modules/group/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_GroupIDs_BY_CommentID(commentID cp.CommentUUID) (groupIDs []gp.GroupUUID, err protocol.Error)
	LIST_CommentIDs_By_GroupID(groupID gp.GroupUUID, offset, limit uint64) (commentIDs []cp.CommentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
