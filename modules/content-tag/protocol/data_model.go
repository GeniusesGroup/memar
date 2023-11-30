/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"

	// arp "org/modules/app-request/protocol"
	cp "org/modules/content/protocol"
)

type DataModel interface {
	Tag() string
	ContentID() cp.ContentUUID

	// arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
