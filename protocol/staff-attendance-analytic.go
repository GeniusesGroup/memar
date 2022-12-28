/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// StaffAttendanceAnalytic indicate the domain record data fields.
type StaffAttendanceAnalytic interface {
	StaffID() [16]byte          // staff domain
	Day() utc.DayElapsed        //
	Hours() uint64              //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
