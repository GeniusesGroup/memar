/* For license and copyright information please see the LEGAL file in the code repository */

package esp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ep "org/modules/estate/protocol"
)

type DataModel interface {
	EstateID() ep.EstateUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
