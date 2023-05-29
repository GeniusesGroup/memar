/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type StaffInterview interface {
	StaffID() StaffUUID //

	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffInterview_StorageServices interface {
	Save(f StaffInterview) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (f StaffInterview, nv protocol.NumberOfVersion, err protocol.Error)

}