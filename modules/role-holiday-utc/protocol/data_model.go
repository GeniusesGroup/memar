/* For license and copyright information please see the LEGAL file in the code repository */

package rhup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	RoleID() rp.RoleUUID            //
	Week() utc.WeekElapsed          //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this role active to provide services
	DayHours() earth.DayHours       // what hours in a day this role active to provide services
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

