/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// UserVehicle
// Vehicle is a conveyance that transports people or objects
type UserVehicle interface {
	UserID() protocol.UserID    // user domain
	ThingID() [16]byte          //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
