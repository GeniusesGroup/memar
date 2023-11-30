/* For license and copyright information please see the LEGAL file in the code repository */

package eblup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	eblp "org/modules/estate-building-location/protocol"
	ebp "org/modules/estate-building/protocol"
)

type DataModel interface {
	BuildingLocationID() eblp.BuildingLocationUUID // use in Coordinate domain too, to get physical location of the Location.
	BuildingID() ebp.BuildingUUID
	Usage() string

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
