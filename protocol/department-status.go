/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type DepartmentStatus interface {
	DepartmentID() [16]byte     // department domain
	Status() Department_Status  //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DepartmentStatus_StorageServices interface {
	Save(ds DepartmentStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID [16]byte, vo protocol.VersionOffset) (ds DepartmentStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Department_Status, offset, limit uint64) (departmentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	// protocol.EventTarget
}

type Department_Status Quiddity_Status

const (
// Department_Status_ Department_Status = (Quiddity_Status_FreeFlag << iota)
)
