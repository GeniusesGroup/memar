/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

// StaffShift indicate the domain record data fields.
type StaffShift interface {
	StaffID() [16]byte          // staff domain
	Day() utc.DayElapsed        //
	ShiftID() [16]byte          // org-shift domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
