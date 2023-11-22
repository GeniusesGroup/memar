/* For license and copyright information please see the LEGAL file in the code repository */

package asrmp

import (
	"memar/protocol"

	amp "org/modules/app-module/protocol"
	arp "org/modules/app-request/protocol"
	asp "org/modules/app-service/protocol"
)

// DataModel indicates the domain record data fields.
type DataModel interface {
	ServiceID() asp.ServiceUUID
	ModuleID() amp.ModuleUUID
	// Type()

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
