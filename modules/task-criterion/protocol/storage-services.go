/* For license and copyright information please see the LEGAL file in the code repository */

package tcp

import (
	"memar/protocol"

	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_TaskIDs_BY_Type(t Type, offset, limit uint64) (taskIDs []tp.TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
