/* For license and copyright information please see the LEGAL file in the code repository */

package department_p

import (
	"memar/protocol"

	storage_p "org/modules/storage/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err protocol.Error)

	Count(departmentID DepartmentUUID) (nv storage_p.NumberOfVersion, err protocol.Error)
	Get(departmentID DepartmentUUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err protocol.Error)

	FIND_DepartmentIDs_BY_ParentID(parentID DepartmentUUID, offset, limit uint64) (departmentIDs []DepartmentUUID, nv storage_p.NumberOfVersion, err protocol.Error)
}
