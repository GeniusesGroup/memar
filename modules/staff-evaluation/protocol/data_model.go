/* For license and copyright information please see the LEGAL file in the code repository */

package sep

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	sp "org/modules/staff/protocol"
)

// it can be done by staff itself, manager, other staff, ...
type DataModel interface {
	StaffID() sp.StaffUUID     //
	EvaluatorID() sp.StaffUUID //

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


