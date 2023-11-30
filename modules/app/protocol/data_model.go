/* For license and copyright information please see the LEGAL file in the code repository */

package ap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

type DataModel interface {
	AppID() AppUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
