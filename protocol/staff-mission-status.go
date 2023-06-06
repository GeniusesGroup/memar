/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type StaffMissionStatus interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	Status() StaffMission_Status    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffMissionStatus_StorageServices interface {
	Save(dm StaffMissionStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm StaffMissionStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status StaffMission_Status, offset, limit uint64) (staffIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type StaffMission_Status Quiddity_Status

const (
	StaffMission_Status_NeedManagerApprove = StaffMission_Status(Quiddity_Status_FreeFlag << iota)
	StaffMission_Status_ManagerApproved
)
