/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

type StaffTakeLeaveStatus interface {
	StaffID() [16]byte             // staff domain
	Day() utc.DayElapsed           //
	Status() StaffTakeLeave_Status //
	Time() protocol.Time           // save time
	RequestID() UserRequestUUID    // user-request domain
}

type StaffTakeLeaveStatus_StorageServices interface {
	Save(ss StaffTakeLeaveStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID [16]byte, vo protocol.VersionOffset) (ss StaffTakeLeaveStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status StaffTakeLeave_Status, offset, limit uint64) (staffIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type StaffTakeLeave_Status Quiddity_Status

const (
	StaffTakeLeave_Status_NeedAlternate = StaffTakeLeave_Status(Quiddity_Status_FreeFlag << iota)
	StaffTakeLeave_Status_NeedAlternateApprove
	StaffTakeLeave_Status_AlternateApprove
	StaffTakeLeave_Status_NeedManagerApprove
	StaffTakeLeave_Status_ManagerApprove
)
