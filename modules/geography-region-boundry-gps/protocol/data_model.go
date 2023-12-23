/* For license and copyright information please see the LEGAL file in the code repository */

package ggcrp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

// TODO:::
type DataModel interface {
	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
