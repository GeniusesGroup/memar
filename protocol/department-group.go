/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type DepartmentGroup interface {
	DepartmentID() DepartmentUUID   // quiddity domain. use to get and show locale title.
	GroupID() GroupUUID             // group id
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentGroup_StorageServices interface {
	Save(dg DepartmentGroup) (nv protocol.NumberOfVersion, err protocol.Error)
	Delete(departmentID [16]byte, groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)

	ListGroupIDs(departmentID [16]byte, offset, limit uint64) (groupIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
