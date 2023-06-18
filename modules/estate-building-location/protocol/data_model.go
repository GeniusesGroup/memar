/* For license and copyright information please see the LEGAL file in the code repository */

package eblp

import (
	"libgo/protocol"

	ebp "org/modules/estate-building/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel can use to indicate any part of a building like warehouses, zones, halls, ...
type DataModel interface {
	BuildingLocationID() BuildingLocationUUID //
	BuildingID() ebp.BuildingUUID             //
	SaveTime() protocol.Time                  //
	RequestID() urp.UserRequestUUID           //
}
