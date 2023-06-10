/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type StaffMission interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       //
	Type() StaffMission_Type        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffMission_StorageServices interface {
	Save(dm StaffMission) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm StaffMission, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_StaffIDs_BY_Day(day utc.DayElapsed, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// we may need indexing based on mission type ??
	// FindByType(t StaffMission_Type, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)

}

type StaffMission_Type uint8

const (
	StaffMission_Type_Unset StaffMission_Type = iota
	StaffMission_Type_Meeting
	StaffMission_Type_Negotiation
	StaffMission_Type_Deal
	StaffMission_Type_Study
	// StaffMission_Type_
)
