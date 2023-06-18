/* For license and copyright information please see the LEGAL file in the code repository */

package gsp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_GroupIDs_BY_Status(status Status, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
