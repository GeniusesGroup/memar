/* For license and copyright information please see the LEGAL file in the code repository */

package trtp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	tp "org/modules/text/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TextID() tp.TextUUID
	RelatedID() tp.TextUUID
	Type()

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
