/* For license and copyright information please see the LEGAL file in the code repository */

package tp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm Task) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID TaskUUID, vo protocol.VersionOffset) (dm Task, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_TaskIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (taskIDs []TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
