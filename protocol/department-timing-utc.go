/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

type DepartmentTimingUTCWeekly interface {
	DepartmentID() DepartmentUUID   //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours       // what hours in day in utc time week this department active to provide services
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentTimingUTCWeekly_StorageServices interface {
	Save(dm DepartmentTimingUTCWeekly) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID DepartmentUUID, week utc.Weekdays) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID DepartmentUUID, week utc.Weekdays, vo protocol.VersionOffset) (dm DepartmentTimingUTCWeekly, nv protocol.NumberOfVersion, err protocol.Error)
}
