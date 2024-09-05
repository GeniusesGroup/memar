/* For license and copyright information please see the LEGAL file in the code repository */

package dg_p

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	dp "org/modules/org-department/protocol"
	storage_p "org/modules/storage/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err protocol.Error)
	Delete(departmentID dp.DepartmentUUID, groupID gp.GroupUUID) (nv storage_p.NumberOfVersion, err protocol.Error)

	LIST_GroupIDs_BY_DepartmentID(departmentID dp.DepartmentUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv storage_p.NumberOfVersion, err protocol.Error)
}
