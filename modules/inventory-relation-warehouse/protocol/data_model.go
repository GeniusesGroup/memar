/* For license and copyright information please see the LEGAL file in the code repository */

package idp

import (
	"memar/protocol"

	ip "org/modules/inventory/protocol"
	wp "org/modules/warehouse/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryUUID() ip.InventoryUUID
	WarehouseID() wp.WarehouseUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
