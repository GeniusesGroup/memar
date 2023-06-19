/* For license and copyright information please see the LEGAL file in the code repository */

package wrbl

import (
	blp "org/modules/estate-building-location/protocol"
	qsp "org/modules/quiddity-status/protocol"
)

type DataModel interface {
	BuildingLocationUUID() blp.BuildingLocationUUID
	Status() Status
}

type Status qsp.Quiddity_Status

const (
	Status_Reserved = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Occupied
	Status_Vacant
)
