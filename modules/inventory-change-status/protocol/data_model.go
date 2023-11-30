/* For license and copyright information please see the LEGAL file in the code repository */

package icsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	icp "org/modules/inventory-change/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryChangeID() icp.InventoryChangeUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
