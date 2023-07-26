/* For license and copyright information please see the LEGAL file in the code repository */

package rrdp

import (
	"memar/protocol"

	dp "org/modules/department/protocol"
	rp "org/modules/role/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID rp.RoleUUID, status Status) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID rp.RoleUUID, status Status, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_RoleIDs_BY_DepartmentID(departmentID dp.DepartmentUUID, offset, limit uint64) (roleIDs []rp.RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_DepartmentIDs_BY_RoleID(roleID rp.RoleUUID, offset, limit uint64) (departmentIDs []dp.DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
