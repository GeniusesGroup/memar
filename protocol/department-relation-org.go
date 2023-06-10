/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DepartmentOrgRelation indicate the domain record data fields.
type DepartmentOwner interface {
	OwnerID() OrgUUID               //
	DepartmentID() DepartmentUUID   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentOrgRelation_StorageServices interface {
	Save(dm DepartmentOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	count(ownerID OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(ownerID OrgUUID, vo protocol.VersionOffset) (dm DepartmentOwner, nv protocol.NumberOfVersion, err protocol.Error)

	Delete(ownerID OrgUUID, departmentID DepartmentUUID) (err protocol.Error)

	FIND_DepartmentID_BY_OrganizationID(departmentID DepartmentUUID, offset, limit uint64) (ownerID OrgUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
