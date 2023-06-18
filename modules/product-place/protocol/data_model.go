/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel indicate service provides in specific place e.g. stations(bus, train, airport, ...), ...
type DataModel interface {
	ProductID() pp.ProductUUID                     //
	BuildingLocationID() eblp.BuildingLocationUUID // use also for Coordinate domain
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
}
