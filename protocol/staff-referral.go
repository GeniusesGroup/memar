/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type StaffReferral interface {
	StaffID() StaffUUID             //
	ReferralID() UserUUID           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}


type StaffReferral_StorageServices interface {
	Save(f StaffReferral) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (f StaffReferral, nv protocol.NumberOfVersion, err protocol.Error)
}
