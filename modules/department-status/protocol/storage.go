/* For license and copyright information please see the LEGAL file in the code repository */

package ds_p

import (
	"memar/protocol"

	dp "org/modules/org-department/protocol"
	storage_p "org/modules/storage/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err protocol.Error)

	Count(departmentID dp.DepartmentUUID) (nv storage_p.NumberOfVersion, err protocol.Error)
	Get(departmentID dp.DepartmentUUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err protocol.Error)

	FILTER_DepartmentIDs_BY_Status(status Status, offset, limit uint64) (departmentIDs []dp.DepartmentUUID, nv storage_p.NumberOfVersion, err protocol.Error)
}
