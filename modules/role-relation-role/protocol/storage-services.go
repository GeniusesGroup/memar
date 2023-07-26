/* For license and copyright information please see the LEGAL file in the code repository */

package rrrp

import (
	"memar/protocol"

	rp "org/modules/role/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID rp.RoleUUID, otherID rp.RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID rp.RoleUUID, otherID rp.RoleUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_OtherIDs_BY_RoleID(roleID rp.RoleUUID, offset, limit uint64) (otherIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RoleIDs_BY_OtherID(otherID rp.RoleUUID, offset, limit uint64) (roleIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
