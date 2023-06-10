/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

type DepartmentHolidayUTCWeekLy interface {
	DepartmentID() DepartmentUUID   //
	Week() utc.WeekElapsed          //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours       // what hours in a day this department active to provide services
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DepartmentHolidayUTCWeekLy_StorageServices interface {
	Save(dm DepartmentHolidayUTCWeekLy) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(departmentID DepartmentUUID, week utc.WeekElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(departmentID DepartmentUUID, week utc.WeekElapsed, vo protocol.VersionOffset) (dm DepartmentHolidayUTCWeekLy, nv protocol.NumberOfVersion, err protocol.Error)
}
