/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type DepartmentOffice interface {
	DepartmentID() [16]byte       // department domain
	BuildingLocationID() [16]byte // building-location domain
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type DepartmentOffice_StorageServices interface {
	Save(do DepartmentOffice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID [16]byte, vo protocol.VersionOffset) (do DepartmentOffice, nv protocol.NumberOfVersion, err protocol.Error)
}
