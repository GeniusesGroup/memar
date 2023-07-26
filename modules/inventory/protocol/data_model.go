/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	"memar/protocol"

	icp "org/modules/inventory-change/protocol"
	pbp "org/modules/inventory-lot/protocol"
	wp "org/modules/warehouse/protocol"
)

// DataModel indicate the domain record data fields.
// ProductInventory or good stock
type DataModel interface {
	LotID() pbp.ProductBatchUUID
	WarehouseID() wp.WarehouseUUID
	InventoryChangeID() icp.InventoryChangeUUID
	Amount() int64 // this transaction
	Stock() int64  // overall in each location

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
