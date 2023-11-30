/* For license and copyright information please see the LEGAL file in the code repository */

package isp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/inventory/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryID() ip.InventoryUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
