/* For license and copyright information please see the LEGAL file in the code repository */

package top

import (
	"libgo/protocol"

	tp "org/modules/thing/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// ThingOwner
// e.g. Vehicle is a conveyance that transports people or objects
type ThingOwner interface {
	ThingID() tp.ThingUUID             //
	OwnerID() up.UserUUID           //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
