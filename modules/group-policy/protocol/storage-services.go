/* For license and copyright information please see the LEGAL file in the code repository */

package gpp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// need to be discussed
	// FindByUserID(ownerUserID up.UserUUID, offset, limit uint64) (ids [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
