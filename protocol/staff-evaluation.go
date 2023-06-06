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
	Save(dm StaffEvaluation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, vo protocol.VersionOffset) (dm StaffEvaluation, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_StaffIDs_BY_EvaluatorIDs(evaluatorID StaffUUID, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_EvaluatorIDs_BY_StaffID(staffID StaffUUID, offset, limit uint64) (evaluatorIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
