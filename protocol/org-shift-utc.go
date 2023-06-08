/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type OrgShiftUTCWeekly interface {
	ShiftID() ShiftUUID             //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week this org active to provide services
	DayHours() earth.DayHours       // what hours in day in utc time week this org active to provide services
	Type() OrgShift_Type            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type OrgShiftUTC_StorageServices interface {
	Save(dm OrgShiftUTCWeekly) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(shiftID ShiftUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(shiftID ShiftUUID, vo protocol.VersionOffset) (dm OrgShiftUTCWeekly, err protocol.Error)

	// do we need indexing ??
	FIND_ShiftIDs_BY_Type(t OrgShift_Type, offset, limit uint64) (shiftIDs []ShiftUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
