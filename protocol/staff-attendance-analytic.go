/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

// StaffAttendanceAnalytic indicate the domain record data fields.
type StaffAttendanceAnalytic interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	Hours() uint64                  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
