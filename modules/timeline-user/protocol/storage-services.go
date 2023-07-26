/* For license and copyright information please see the LEGAL file in the code repository */

package tup

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, priority uint64, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListUser(groupID gp.GroupUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGroup(userID up.UserUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(userID up.UserUUID, groupID gp.GroupUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO:::
	// FilterByStatus(userID up.UserUUID, status Status, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
