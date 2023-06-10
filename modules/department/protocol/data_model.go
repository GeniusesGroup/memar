/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// quiddity domain
type DepartmentUUID = protocol.UUID

// Department indicate the domain record data fields.
// It can use to show organizational chart. Also staffs can join to the related group.
type Department interface {
	DepartmentID() DepartmentUUID   //
	ParentID() DepartmentUUID       // DepartmentID, Exist if it isn't top of the organization.
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Department_StorageServices interface {
	Save(dm Department) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID DepartmentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID DepartmentUUID, vo protocol.VersionOffset) (dm Department, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DepartmentIDs_BY_ParentID(parentID DepartmentUUID, offset, limit uint64) (departmentIDs []DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
