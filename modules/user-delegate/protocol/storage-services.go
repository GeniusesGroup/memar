/* For license and copyright information please see the LEGAL file in the code repository */

package udp

import (
	"memar/protocol"

	rp "org/modules/role/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(ud DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(givenUserID, gottenUserID up.UserUUID, roleID rp.RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(givenUserID, gottenUserID up.UserUUID, roleID rp.RoleUUID, vo protocol.VersionOffset) (ud DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListRoles(givenUserID, gottenUserID up.UserUUID, offset, limit uint64) (roles []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGottenUsers(roleID rp.RoleUUID, offset, limit uint64) (gottenUserIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGivenUsers(roleID rp.RoleUUID, offset, limit uint64) (givenUserIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGottenDelegateUsers(gottenUserID up.UserUUID, offset, limit uint64) (givenUserIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListGivenDelegateUsers(givenUserID up.UserUUID, offset, limit uint64) (gottenUserID []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
