/* For license and copyright information please see the LEGAL file in the code repository */

package trtp

import (
	"memar/protocol"

	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(otherID tp.TaskUUID, taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(otherID tp.TaskUUID, taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_OtherIDs_BY_TaskID(taskID tp.TaskUUID, offset, limit uint64) (otherIDs []tp.TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_TaskIDs_BY_OtherID(otherID tp.TaskUUID, offset, limit uint64) (taskIDs []tp.TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
