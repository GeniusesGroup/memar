/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

// StaffShift indicate the domain record data fields.
type StaffShift interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	ShiftID() ShiftUUID            
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffShift_StorageServices interface {
	Save(dm StaffShift) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm StaffShift, nv protocol.NumberOfVersion, err protocol.Error)


    LIST_StaffIDs_BY_Day(day utc.DayElapsed, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)

}
