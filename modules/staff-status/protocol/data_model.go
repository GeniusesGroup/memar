/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type StaffStatus interface {
	StaffID() StaffUUID             //
	Status() Staff_Status           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffStatus_StorageServices interface {
	Save(dm StaffStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (dm StaffStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_StaffIDs_BY_Status(status Staff_Status, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Staff_Status Quiddity_Status

const (
	Staff_Status_Hire = Staff_Status(Quiddity_Status_FreeFlag << iota)
	Staff_Status_Fire
	Staff_Status_End // death, end of contract, ...
	// Staff_Status_Active   // Shift
	// Staff_Status_Inactive // Shift
)
