/* For license and copyright information please see the LEGAL file in the code repository */

package cdp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/content/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ContentID() cp.ContentUUID
	Duration() protocol.Duration // AI suggested duration

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
