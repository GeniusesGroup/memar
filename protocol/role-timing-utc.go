/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
)

type RoleTimingUTC interface {
	RoleID() [16]byte           // role domain
	Weekdays() utc.Weekdays     // what days in weekday in utc time week this role active to provide services
	DayHours() earth.DayHours   // what hours in day in utc time week this role active to provide services
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type RoleTimingUTC_StorageServices interface {
	Save(rt RoleTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID [16]byte, vo protocol.VersionOffset) (rt RoleTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
