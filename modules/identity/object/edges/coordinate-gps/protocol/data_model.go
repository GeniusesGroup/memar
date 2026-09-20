/* For license and copyright information please see the LEGAL file in the code repository */

package coordinate_gps_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

// DataModel store location details of user or things
// location of the provider. live location of the user.
type DataModel interface {
	thing_p.Field_ThingUUID
	Lat() uint64 // latitude
	Lon() uint64 // longitude
	Alt() uint64 // altitude

	// X() uint64 // Three-Dimensional Coordinate Systems
	// Y() uint64 // Three-Dimensional Coordinate Systems
	// Z() uint64 // Three-Dimensional Coordinate Systems
}
