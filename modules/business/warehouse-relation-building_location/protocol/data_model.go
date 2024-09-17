/* For license and copyright information please see the LEGAL file in the code repository */

package wrbl

import (
	blp "org/modules/estate-building-location/protocol"
)

type DataModel interface {
	BuildingLocationUUID() blp.BuildingLocationUUID
	Status() Status
}
