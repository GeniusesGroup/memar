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
	PresentedID() [16]byte          //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffTakeLeaveAlternate_StorageServices interface {
	Save(f StaffTakeLeaveAlternate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (f StaffTakeLeaveAlternate, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
