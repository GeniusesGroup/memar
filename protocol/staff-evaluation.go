/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// it can be done by staff itself, manager, other staff, ...
type StaffEvaluation interface {
	StaffID() [16]byte     // staff domain
	EvaluatorID() [16]byte // user domain

	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
