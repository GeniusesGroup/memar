/* For license and copyright information please see the LEGAL file in the code repository */

package stlap

import (
	"libgo/protocol"
	"libgo/time/utc"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel or staff replace
type DataModel interface {
	StaffID() sp.StaffUUID          //
	Day() utc.DayElapsed            //
	PresentedID() sp.StaffUUID      //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
