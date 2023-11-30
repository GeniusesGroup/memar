/* For license and copyright information please see the LEGAL file in the code repository */

package cap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/content/protocol"
)

type DataModel interface {
	ContentID() cp.ContentUUID
	Access() Access

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
