/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

type StaffOvertimeStatus interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	Status() StaffOvertime_Status   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffOvertimeStatus_StorageServices interface {
	Save(dm StaffOvertimeStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID,  day utc.DayElapsed ) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm StaffOvertimeStatus, nv protocol.NumberOfVersion, err protocol.Error)


	// FilterByStatus(status StaffOvertime_Status, offset, limit uint64) (staffIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type StaffOvertime_Status Quiddity_Status

const (
	StaffOvertime_Status_NeedManagerApprove = StaffOvertime_Status(Quiddity_Status_FreeFlag << iota)
	StaffOvertime_Status_ManagerApprove
)
