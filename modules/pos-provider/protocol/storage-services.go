/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"libgo/protocol"

	pp "org/modules/pos/protocol"
	rp "org/modules/role/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID pp.PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID pp.PosUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_PosIDs_BY_RoleID(roleID rp.RoleUUID, offset, limit uint64) (posIDs []pp.PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
