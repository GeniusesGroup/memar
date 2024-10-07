/* For license and copyright information please see the LEGAL file in the code repository */

package discount

import (
	bp "org/modules/rights/building-location/protocol"
)

type Location interface {
	BuildingLocationID() bp.UUID
}
