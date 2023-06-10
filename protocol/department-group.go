/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type DepartmentGroup interface {
	DepartmentID() DepartmentUUID // quiddity domain. use to get and show locale title.
	GroupID() GroupUUID
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentGroup_StorageServices interface {
	Save(dm DepartmentGroup) (nv protocol.NumberOfVersion, err protocol.Error)
	Delete(departmentID DepartmentUUID, groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)

	LIST_GroupIDs_BY_DepartmentID(departmentID DepartmentUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
