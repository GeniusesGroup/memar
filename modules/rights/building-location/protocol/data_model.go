/* For license and copyright information please see the LEGAL file in the code repository */

package eblp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ebp "org/modules/estate-building/protocol"
)

// DataModel can use to indicate any part of a building like warehouses, zones, halls, ...
type DataModel interface {
	BuildingLocationID() BuildingLocationUUID
	BuildingID() ebp.BuildingUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
