/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type StaffStatus interface {
	StaffID() [16]byte          // user domain
	Status() Staff_Status       //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type StaffStatus_StorageServices interface {
	Save(ss StaffStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID [16]byte, vo protocol.VersionOffset) (ss StaffStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Staff_Status, offset, limit uint64) (staffIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

type Staff_Status Quiddity_Status

const (
	Staff_Status_Hire = Staff_Status(Quiddity_Status_FreeFlag << iota)
	Staff_Status_Fire
	Staff_Status_End // death, end of contract, ...
	// Staff_Status_Active   // Shift
	// Staff_Status_Inactive // Shift
)
