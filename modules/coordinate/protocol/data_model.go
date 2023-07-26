/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"

	tp "org/modules/thing/protocol"
)

// DataModel store location details of user or things
// location of the provider. live location of the user.
type DataModel interface {
	CoordinateID() CoordinateUUID
	ThingID() tp.ThingUUID // device who send the coordinate
	Lat() uint64           // latitude
	Lon() uint64           // longitude
	Alt() uint64           // altitude

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
