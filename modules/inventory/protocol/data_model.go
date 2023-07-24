/* For license and copyright information please see the LEGAL file in the code repository */

package pip

import (
	"libgo/protocol"

	pbp "org/modules/inventory-lot/protocol"
	picp "org/modules/inventory-change/protocol"
	urp "org/modules/user-request/protocol"
	wp "org/modules/warehouse/protocol"
)

// DataModel indicate the domain record data fields.
// ProductInventory or good stock
type DataModel interface {
	LotID() pbp.ProductBatchUUID        //
	WarehouseID() wp.WarehouseUUID               //
	InventoryChangeID() picp.InventoryChangeUUID //
	Amount() int64                               // this transaction
	Stock() int64                                // overall in each location
	SaveTime() protocol.Time                     //
	RequestID() urp.UserRequestUUID              //
}
