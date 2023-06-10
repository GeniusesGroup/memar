/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type DepartmentOffice interface {
	DepartmentID() DepartmentUUID //
	BuildingLocationID() BuildingLocationUUID
	// TODO::: Label or type: IT-Office, ...
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentOffice_StorageServices interface {
	Save(dm DepartmentOffice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID DepartmentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID DepartmentUUID, vo protocol.VersionOffset) (dm DepartmentOffice, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DepartmentIDs_BY_BuildingLocationID(buildingLocationID BuildingLocationUUID, offset, limit uint64) (departmentIDs []DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
