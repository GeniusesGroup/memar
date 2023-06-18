/* For license and copyright information please see the LEGAL file in the code repository */

package dgp

import (
	"libgo/protocol"

	dp "org/modules/department/protocol"
	gp "org/modules/group/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)
	Delete(departmentID dp.DepartmentUUID, groupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)

	LIST_GroupIDs_BY_DepartmentID(departmentID dp.DepartmentUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
