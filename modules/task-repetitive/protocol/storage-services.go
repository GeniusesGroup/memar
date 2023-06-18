/* For license and copyright information please see the LEGAL file in the code repository */

package trp

import (
	"libgo/protocol"

	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
