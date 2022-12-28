/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
)

type StaffOvertime interface {
	StaffID() [16]byte          // staff domain
	Day() utc.DayElapsed        //
	DayHours() earth.DayHours   //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
