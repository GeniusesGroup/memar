/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/earth"
	"github.com/GeniusesGroup/libgo/time/utc"
)

type DepartmentHolidayUTC interface {
	DepartmentID() [16]byte     // department domain
	Week() utc.WeekElapsed      //
	Weekdays() utc.Weekdays     // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours   // what hours in a day this department active to provide services
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
