/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type DepartmentOffice interface {
	DepartmentID() DepartmentUUID //
	BuildingLocationID() [16]byte // building-location domain
	// TODO::: Label or type: IT-Office, ...
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentOffice_StorageServices interface {
	Save(do DepartmentOffice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID [16]byte, vo protocol.VersionOffset) (do DepartmentOffice, nv protocol.NumberOfVersion, err protocol.Error)
}
