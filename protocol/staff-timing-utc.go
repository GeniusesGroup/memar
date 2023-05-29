/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type StaffTimingUTC interface {
	StaffID() StaffUUID             //
	ShiftID() [16]byte              // org-shift domain
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       // what hours in a day this staff must active to provide services or do projects
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffTimingUTC_StorageServices interface {
	Save(st StaffTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (st StaffTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
