/* For license and copyright information please see the LEGAL file in the code repository */

package drop

import (
	"memar/protocol"

	dp "org/modules/department/protocol"
	org "org/modules/org/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	count(ownerID org.OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(ownerID org.OrgUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	Delete(ownerID org.OrgUUID, departmentID dp.DepartmentUUID) (err protocol.Error)

	FIND_DepartmentID_BY_OrganizationID(departmentID dp.DepartmentUUID, offset, limit uint64) (ownerID org.OrgUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
