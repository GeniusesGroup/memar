/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// can be same as quiddity||user||invoice||area||building||building-location||staff||... domain
type CoordinateUUID = protocol.UUID

// Coordinate store location details of user or things
// location of the provider. live location of the user.
type Coordinate interface {
	CoordinateID() CoordinateUUID   //
	ThingID() [16]byte              // device who send the coordinate
	Lat() uint64                    // latitude
	Lon() uint64                    // longitude
	Alt() uint64                    // altitude
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
