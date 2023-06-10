/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type DepartmentStatus interface {
	DepartmentID() DepartmentUUID   //
	Status() Department_Status      //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentStatus_StorageServices interface {
	Save(dm DepartmentStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID DepartmentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID DepartmentUUID, vo protocol.VersionOffset) (dm DepartmentStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_DepartmentIDs_BY_Status(status Department_Status, offset, limit uint64) (departmentIDs []DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	
	// protocol.EventTarget
}

type Department_Status Quiddity_Status

const (
// Department_Status_ Department_Status = (Quiddity_Status_FreeFlag << iota)
)
