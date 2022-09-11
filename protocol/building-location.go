package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// BuildingLocation can use to indicate any part of a building like warehouses, zones, halls, ...
type BuildingLocation interface {
	BuildingLocationID() [16]byte // quiddity domain. use in Coordinate domain too, to get physical location of the Location.
	BuildingID() [16]byte         // building domain
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}
