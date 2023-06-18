/* For license and copyright information please see the LEGAL file in the code repository */

package rrup

import (
	"libgo/protocol"

	rp "org/modules/role/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID rp.RoleUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID rp.RoleUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// FindByOwner(ownerID up.UserUUID, offset, limit uint64) (roleIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RoleIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (roleIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_UserIDs_BY_RoleID(roleID rp.RoleUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
