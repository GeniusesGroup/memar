/* For license and copyright information please see the LEGAL file in the code repository */

package plp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PosID() pp.PosUUID
	BuildingLocationID() eblp.BuildingLocationUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
