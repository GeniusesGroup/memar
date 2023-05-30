/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductPlace indicate the domain record data fields.
// ProductPlace indicate service provides in specific place e.g. stations(bus, train, airport, ...), ...
type ProductPlace interface {
	ProductID() ProductUUID                   //
	BuildingLocationID() BuildingLocationUUID // use also for Coordinate domain
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type ProductPlace_StorageServices interface {
	Save(pp ProductPlace) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pp ProductPlace, nv protocol.NumberOfVersion, err protocol.Error)

	FindByBuildingLocation(buildingLocationID BuildingLocationUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
