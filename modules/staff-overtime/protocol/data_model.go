/* For license and copyright information please see the LEGAL file in the code repository */

package sop

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID          //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
