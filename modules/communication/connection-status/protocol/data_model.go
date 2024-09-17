/* For license and copyright information please see the LEGAL file in the code repository */

package acsp

import (
	"memar/protocol"

	acp "org/modules/app-connection/protocol"
	arp "org/modules/app-request/protocol"
)

// ConnectionMetrics
type DataModel interface {
	ConnectionID() acp.ConnectionUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
