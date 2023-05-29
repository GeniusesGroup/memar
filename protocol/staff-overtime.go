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


type StaffOvertime_StorageServices interface {
	Save(f StaffOvertime) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (f StaffOvertime, nv protocol.NumberOfVersion, err protocol.Error)
}