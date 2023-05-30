/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type RoleTimingUTC interface {
	RoleID() RoleUUID               //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this role active to provide services
	DayHours() earth.DayHours       // what hours in day in utc time week this role active to provide services
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleTimingUTC_StorageServices interface {
	Save(rt RoleTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (rt RoleTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
