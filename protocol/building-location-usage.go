package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type BuildingLocationUsage interface {
	BuildingLocationID() [16]byte // quiddity domain. use in Coordinate domain too, to get physical location of the Location.
	BuildingID() [16]byte         // building domain
	Usage() string                //
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}
