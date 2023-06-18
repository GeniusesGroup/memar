/* For license and copyright information please see the LEGAL file in the code repository */

package rrgp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	rp "org/modules/role/protocol"
)

type StorageServices interface {
	Save(f DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID rp.RoleUUID, status Status) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID rp.RoleUUID, status Status, vo protocol.VersionOffset) (f DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_RoleIDs_BY_GroupID(groupID gp.GroupUUID, offset, limit uint64) (roleIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_GroupIDs_BY_RoleID(roleID rp.RoleUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
