/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type DepartmentGroup interface {
	DepartmentID() [16]byte     // quiddity domain. use to get and show locale title.
	GroupID() [16]byte          // group id
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DepartmentGroup_StorageServices interface {
	Save(dg DepartmentGroup) (nv protocol.NumberOfVersion, err protocol.Error)
	Delete(departmentID [16]byte, groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)

	ListGroupIDs(departmentID [16]byte, offset, limit uint64) (groupIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
