package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// quiddity domain. use in Coordinate domain too, to get physical location of the Location.
type BuildingLocationUUID = protocol.UUID

// BuildingLocation can use to indicate any part of a building like warehouses, zones, halls, ...
type BuildingLocation interface {
	BuildingLocationID() BuildingLocationUUID //
	BuildingID() BuildingUUID                 //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}
