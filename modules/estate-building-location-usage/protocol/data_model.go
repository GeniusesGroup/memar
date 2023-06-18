/* For license and copyright information please see the LEGAL file in the code repository */

package eblup

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	ebp "org/modules/estate-building/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	BuildingLocationID() eblp.BuildingLocationUUID // quiddity domain. use in Coordinate domain too, to get physical location of the Location.
	BuildingID() ebp.BuildingUUID                  //
	Usage() string                                 //
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
}
