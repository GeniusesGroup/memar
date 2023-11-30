/* For license and copyright information please see the LEGAL file in the code repository */

package irlp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/inventory/protocol"
)

// DataModel indicate the domain record data fields.
// ProductInventory or good stock
type DataModel interface {
	InventoryID() ip.InventoryUUID
	SerialID_Start() string
	SerialID_End() string

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
