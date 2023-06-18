/* For license and copyright information please see the LEGAL file in the code repository */

package ursp

import (
	"libgo/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, sideID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, sideID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByStatus(userID up.UserUUID, status Status, offset, limit uint64) (sideIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
