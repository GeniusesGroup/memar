/* For license and copyright information please see the LEGAL file in the code repository */

package cap

import (
	"libgo/protocol"

	cp "org/modules/contract/protocol"
	urp "org/modules/user-request/protocol"
)

type ContractAnalytic interface {
	ContractID() cp.ContractUUID //

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
