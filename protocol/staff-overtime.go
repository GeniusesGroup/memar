/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

type StaffOvertime interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
