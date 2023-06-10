/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type StaffTimingUTC interface {
	StaffID() StaffUUID  //
	Day() utc.DayElapsed //
	ShiftID() ShiftUUID
	DayHours() earth.DayHours       // what hours in a day this staff must active to provide services or do projects
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffTimingUTC_StorageServices interface {
	Save(dm StaffTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm StaffTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)

	// FIND_StaffIDs_BY_ShiftID(shiftID ShiftUUID, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
