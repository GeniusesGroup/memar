/* For license and copyright information please see the LEGAL file in the code repository */

package gap

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_UsersJoinWayIDs_BY_JoinWay(groupID gp.GroupUUID, joinWay JoinWay, offset, limit uint64) (joinedBys []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_GroupIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
