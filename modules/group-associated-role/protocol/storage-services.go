/* For license and copyright information please see the LEGAL file in the code repository */

package garp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_RoleIDs_BY_GroupID(groupID gp.GroupUUID, userID up.UserUUID, offset, limit uint64) (roleIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
