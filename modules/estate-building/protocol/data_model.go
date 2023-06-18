/* For license and copyright information please see the LEGAL file in the code repository */

package ebp

import (
	"libgo/protocol"

	ep "org/modules/estate/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	BuildingID() BuildingUUID   //
	AreaID() ep.EstateUUID          // area domain
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
