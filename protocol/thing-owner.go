/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// ThingOwner
// e.g. Vehicle is a conveyance that transports people or objects
type ThingOwner interface {
	ThingID() ThingUUID             //
	OwnerID() up.UserUUID           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
