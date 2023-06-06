/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

// StaffTakeLeaveAlternate or staff replace
type StaffTakeLeaveAlternate interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	PresentedID() StaffUUID         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffTakeLeaveAlternate_StorageServices interface {
	Save(dm StaffTakeLeaveAlternate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm StaffTakeLeaveAlternate, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
