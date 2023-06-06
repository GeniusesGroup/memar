/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: user-number??
type StaffID interface {
	StaffID() StaffUUID             //
	ID() uint32                     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffID_StorageServices interface {
	Save(dm StaffID) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (dm StaffID, nv protocol.NumberOfVersion, err protocol.Error)
}
