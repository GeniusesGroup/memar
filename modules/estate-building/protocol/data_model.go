/* For license and copyright information please see the LEGAL file in the code repository */

package ebp

import (
	"memar/protocol"

	ep "org/modules/estate/protocol"
)

type DataModel interface {
	BuildingID() BuildingUUID
	AreaID() ep.EstateUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
