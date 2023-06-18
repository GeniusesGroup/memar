/* For license and copyright information please see the LEGAL file in the code repository */

package cugsp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, groupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, groupID gp.GroupUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
