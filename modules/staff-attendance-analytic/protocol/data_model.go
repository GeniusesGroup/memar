/* For license and copyright information please see the LEGAL file in the code repository */

package saap

import (
	"libgo/protocol"
	"libgo/time/utc"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	StaffID() sp.StaffUUID          //
	Day() utc.DayElapsed            //
	Hours() uint64                  //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
