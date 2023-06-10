/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleDepartmentRelation indicate the domain record data fields.
type RoleDepartmentRelation interface {
	RoleID() RoleUUID //
	Status() Role_Department_Status
	DepartmentID() DepartmentUUID   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleDepartmentRelation_StorageServices interface {
	Save(dm RoleDepartmentRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID, status Role_Department_Status) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, status Role_Department_Status, vo protocol.VersionOffset) (dm RoleDepartmentRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_RoleIDs_BY_DepartmentID(departmentID DepartmentUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_DepartmentIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (departmentIDs []DepartmentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Role_Department_Status Quiddity_Status
