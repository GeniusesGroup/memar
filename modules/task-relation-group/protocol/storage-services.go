/* For license and copyright information please see the LEGAL file in the code repository */

package trgp

import (
	"libgo/protocol"
	gp "org/modules/group/protocol"
	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID gp.GroupUUID, taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID gp.GroupUUID, taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_TaskIDs_BY_GroupID(groupID gp.GroupUUID, offset, limit uint64) (taskIDs []tp.TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_GroupIDs_BY_TaskID(taskID tp.TaskUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
