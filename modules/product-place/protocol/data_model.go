/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"memar/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel indicate service provides in specific place e.g. stations(bus, train, airport, ...), ...
type DataModel interface {
	ProductID() pp.ProductUUID
	BuildingLocationID() eblp.BuildingLocationUUID // use also for Coordinate domain

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
