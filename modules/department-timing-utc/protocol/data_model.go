/* For license and copyright information please see the LEGAL file in the code repository */

package dtup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
	dp "org/modules/department/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID   //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours       // what hours in day in utc time week this department active to provide services
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


