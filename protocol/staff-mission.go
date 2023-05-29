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
	Save(f StaffMission) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (f StaffMission, nv protocol.NumberOfVersion, err protocol.Error)

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
