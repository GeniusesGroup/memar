/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	eblp "org/modules/estate-building-location/protocol"
	tp "org/modules/thing/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ThingUUID() tp.ThingUUID
	BuildingLocationID() eblp.BuildingLocationUUID
	X() uint64 // Three-Dimensional Coordinate Systems
	Y() uint64 // Three-Dimensional Coordinate Systems
	Z() uint64 // Three-Dimensional Coordinate Systems

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
