/* For license and copyright information please see the LEGAL file in the code repository */

package ebp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ep "org/modules/estate/protocol"
)

type DataModel interface {
	BuildingID() BuildingUUID
	AreaID() ep.EstateUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
