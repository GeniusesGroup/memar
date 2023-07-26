/* For license and copyright information please see the LEGAL file in the code repository */

package dhup

import (
	"memar/protocol"
	"memar/time/utc"

	dp "org/modules/department/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID dp.DepartmentUUID, week utc.WeekElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID dp.DepartmentUUID, week utc.WeekElapsed, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
