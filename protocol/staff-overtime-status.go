/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

type StaffOvertimeStatus interface {
	StaffID() [16]byte            // staff domain
	Day() utc.DayElapsed          //
	Status() StaffOvertime_Status //
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type StaffOvertimeStatus_StorageServices interface {
	Save(ss StaffOvertimeStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID [16]byte, vo protocol.VersionOffset) (ss StaffOvertimeStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status StaffOvertime_Status, offset, limit uint64) (staffIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type StaffOvertime_Status Quiddity_Status

const (
	StaffOvertime_Status_NeedManagerApprove = StaffOvertime_Status(Quiddity_Status_FreeFlag << iota)
	StaffOvertime_Status_ManagerApprove
)
