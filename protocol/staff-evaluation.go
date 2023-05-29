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
