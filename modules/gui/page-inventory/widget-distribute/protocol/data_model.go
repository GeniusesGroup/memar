/* For license and copyright information please see the LEGAL file in the code repository */

package icp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/inventory/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryChangeID() InventoryChangeUUID
	From() ip.InventoryUUID
	To() ip.InventoryUUID // Can be zero for voiding products.
	Amount() int64        // this transaction
	Priority() uint64

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
