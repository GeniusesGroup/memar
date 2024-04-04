/* For license and copyright information please see the LEGAL file in the code repository */

package dsp

import (
	"memar/protocol"

	dp "org/modules/department/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID dp.DepartmentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID dp.DepartmentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_DepartmentIDs_BY_Status(status Status, offset, limit uint64) (departmentIDs []dp.DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
