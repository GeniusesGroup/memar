/* For license and copyright information please see the LEGAL file in the code repository */

package osup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	sp "org/modules/org-shift/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ShiftID() sp.ShiftUUID          //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this org active to provide services
	DayHours() earth.DayHours       // what hours in day in utc time week this org active to provide services
	Type() sp.OrgShift_Type         //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
