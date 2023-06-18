/* For license and copyright information please see the LEGAL file in the code repository */

package dhup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
	
	dp "org/modules/department/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID //
	Week() utc.WeekElapsed           //
	Weekdays() utc.Weekdays          // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours        // what hours in a day this department active to provide services
	SaveTime() protocol.Time         //
	RequestID() urp.UserRequestUUID  //
}
