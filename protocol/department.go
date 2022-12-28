/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Department indicate the domain record data fields.
// It can use to show organizational chart. Also staffs can join to the related group.
type Department interface {
	DepartmentID() [16]byte     // quiddity domain
	ParentID() [16]byte         // DepartmentID, Exist if it isn't top of the organization.
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Department_StorageServices interface {
	Save(d Department) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID [16]byte, vo protocol.VersionOffset) (d Department, nv protocol.NumberOfVersion, err protocol.Error)
}
