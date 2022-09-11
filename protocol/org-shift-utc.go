/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/earth"
	"github.com/GeniusesGroup/libgo/time/utc"
)

type OrgShiftUTC interface {
	ShiftID() [16]byte          // quiddity domain
	Weekdays() utc.Weekdays     // what days in weekday in utc time week this org active to provide services
	DayHours() earth.DayHours   // what hours in day in utc time week this org active to provide services
	Type() OrgShift_Type        //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
