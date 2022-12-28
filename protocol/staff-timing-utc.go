/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
)

type StaffTimingUTC interface {
	StaffID() [16]byte          // staff domain
	ShiftID() [16]byte          // org-shift domain
	Day() utc.DayElapsed        //
	DayHours() earth.DayHours   // what hours in a day this staff must active to provide services or do projects
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type StaffTimingUTC_StorageServices interface {
	Save(st StaffTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID [16]byte, vo protocol.VersionOffset) (st StaffTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
