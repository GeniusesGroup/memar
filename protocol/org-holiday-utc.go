/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type OrgHolidayUTCWeekly interface {
	OrgID() OrgUUID
	Week() utc.WeekElapsed          //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this org active to provide services
	DayHours() earth.DayHours       // what hours in a day this org active to provide services
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type OrgHolidayUTC_StorageServices interface {
	Save(dm OrgHolidayUTCWeekly) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orgID OrgUUID, week utc.WeekElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orgID OrgUUID, week utc.WeekElapsed, vo protocol.VersionOffset) (dm OrgHolidayUTCWeekly, err protocol.Error)
}
