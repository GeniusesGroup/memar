/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductPlace indicate the domain record data fields.
// ProductPlace indicate service provides in specific place e.g. stations(bus, train, airport, ...), ...
type ProductPlace interface {
	ProductID() [16]byte          // product domain.
	BuildingLocationID() [16]byte // building-location domain. use also for Coordinate domain
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type ProductPlace_StorageServices interface {
	Save(pp ProductPlace) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pp ProductPlace, nv protocol.NumberOfVersion, err protocol.Error)

	FindByBuildingLocation(buildingLocationID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
