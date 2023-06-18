/* For license and copyright information please see the LEGAL file in the code repository */

package ohup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	OrgID() org.OrgUUID
	Week() utc.WeekElapsed          //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this org active to provide services
	DayHours() earth.DayHours       // what hours in a day this org active to provide services
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

