/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type RoleHolidayUTC interface {
	RoleID() RoleUUID               //
	Week() utc.WeekElapsed          //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this role active to provide services
	DayHours() earth.DayHours       // what hours in a day this role active to provide services
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleHolidayUTC_StorageServices interface {
	Save(dm RoleHolidayUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID, week utc.WeekElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, week utc.WeekElapsed, vo protocol.VersionOffset) (dm RoleHolidayUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
