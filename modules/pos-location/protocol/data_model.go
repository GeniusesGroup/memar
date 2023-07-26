/* For license and copyright information please see the LEGAL file in the code repository */

package plp

import (
	"memar/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PosID() pp.PosUUID
	BuildingLocationID() eblp.BuildingLocationUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
