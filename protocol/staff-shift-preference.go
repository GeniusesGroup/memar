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
	ShiftID() [16]byte              // org-shift domain
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffShift_StorageServices interface {
	Save(f StaffShift) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (f StaffShift, nv protocol.NumberOfVersion, err protocol.Error)
    
	// list shifts per staffID ?
}
