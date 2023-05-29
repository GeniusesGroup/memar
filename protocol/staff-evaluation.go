/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// it can be done by staff itself, manager, other staff, ...
type StaffEvaluation interface {
	StaffID() StaffUUID     //
	EvaluatorID() StaffUUID //

	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffEvaluation_StorageServices interface {
	Save(f StaffEvaluation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (f StaffEvaluation, nv protocol.NumberOfVersion, err protocol.Error)

}
