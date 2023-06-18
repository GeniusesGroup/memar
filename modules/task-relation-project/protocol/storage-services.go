/* For license and copyright information please see the LEGAL file in the code repository */

package trpp

import (
	"libgo/protocol"
	pp "org/modules/project/protocol"
	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID pp.ProjectUUID, taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID pp.ProjectUUID, taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	List_ProjectIDs_BY_TaskID(taskID tp.TaskUUID, offset, limit uint64) (projectIDs []pp.ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_TaskIDs_BY_ProjectID(projectID pp.ProjectUUID, offset, limit uint64) (taskIDs []tp.TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
