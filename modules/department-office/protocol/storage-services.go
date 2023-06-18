/* For license and copyright information please see the LEGAL file in the code repository */

package dop

import (
	"libgo/protocol"

	dp "org/modules/department/protocol"
	blp "org/modules/estate-building-location/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID dp.DepartmentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID dp.DepartmentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DepartmentIDs_BY_BuildingLocationID(buildingLocationID blp.BuildingLocationUUID, offset, limit uint64) (departmentIDs []dp.DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
