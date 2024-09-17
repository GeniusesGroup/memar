/* For license and copyright information please see the LEGAL file in the code repository */

package dtu_p

import (
	"memar/protocol"
	"memar/time/utc"

	dp "org/modules/org-department/protocol"
	storage_p "org/modules/storage/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err protocol.Error)

	Count(departmentID dp.DepartmentUUID, week utc.Weekdays) (nv storage_p.NumberOfVersion, err protocol.Error)
	Get(departmentID dp.DepartmentUUID, week utc.Weekdays, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err protocol.Error)
}
