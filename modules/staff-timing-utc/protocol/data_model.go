/* For license and copyright information please see the LEGAL file in the code repository */

package stup

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	osp "org/modules/org-shift/protocol"
	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID //
	Day() utc.DayElapsed   //
	ShiftID() osp.ShiftUUID
	DayHours() earth.DayHours       // what hours in a day this staff must active to provide services or do projects
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
