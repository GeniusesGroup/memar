/* For license and copyright information please see the LEGAL file in the code repository */

package rlp

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	rp "org/modules/role/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID rp.RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID rp.RoleUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_RoleIDs_BY_BuildingLocationID(buildingLocationIDs eblp.BuildingLocationUUID, offset, limit uint64) (roleIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
