/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel store location details of user or things
// location of the provider. live location of the user.
type DataModel interface {
	CoordinateID() CoordinateUUID   //
	ThingID() [16]byte              // device who send the coordinate
	Lat() uint64                    // latitude
	Lon() uint64                    // longitude
	Alt() uint64                    // altitude
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
