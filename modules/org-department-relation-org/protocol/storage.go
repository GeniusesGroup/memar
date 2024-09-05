/* For license and copyright information please see the LEGAL file in the code repository */

package dro_p

import (
	"memar/protocol"

	dp "org/modules/org-department/protocol"
	org "org/modules/org/protocol"
	storage_p "org/modules/storage/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err protocol.Error)

	count(ownerID org.OrgUUID) (nv storage_p.NumberOfVersion, err protocol.Error)
	Get(ownerID org.OrgUUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err protocol.Error)

	Delete(ownerID org.OrgUUID, departmentID dp.DepartmentUUID) (err protocol.Error)

	FIND_DepartmentID_BY_OrganizationID(departmentID dp.DepartmentUUID, offset, limit uint64) (ownerID org.OrgUUID, nv storage_p.NumberOfVersion, err protocol.Error)
}
