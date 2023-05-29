/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserVehicle
// Vehicle is a conveyance that transports people or objects
type UserVehicle interface {
	UserID() UserUUID               //
	ThingID() [16]byte              //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
