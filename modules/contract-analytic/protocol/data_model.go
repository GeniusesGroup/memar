/* For license and copyright information please see the LEGAL file in the code repository */

package cap

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContractAnalytic interface {
	CoordinateID() CoordinateUUID //

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
