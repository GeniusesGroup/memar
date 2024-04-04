/* For license and copyright information please see the LEGAL file in the code repository */

package urup

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, sideID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, sideID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListSides(userID up.UserUUID, offset, limit uint64) (sideIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListUsers(sideID up.UserUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
