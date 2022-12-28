/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// StaffTakeLeaveAlternate or staff replace
type StaffTakeLeaveAlternate interface {
	StaffID() [16]byte          // staff domain
	Day() utc.DayElapsed        //
	PresentedID() [16]byte      // staff domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
