/* For license and copyright information please see the LEGAL file in the code repository */

package dp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID DepartmentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID DepartmentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DepartmentIDs_BY_ParentID(parentID DepartmentUUID, offset, limit uint64) (departmentIDs []DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
