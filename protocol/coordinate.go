/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Coordinate store location details of user or things
// location of the provider. live location of the user.
type Coordinate interface {
	CoordinateID() [16]byte     // quiddity||user||invoice||area||building||building-location||staff||... domain
	ThingID() [16]byte          // device who send the coordinate
	Lat() uint64                // latitude
	Lon() uint64                // longitude
	Alt() uint64                // altitude
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
