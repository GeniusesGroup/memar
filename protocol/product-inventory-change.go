/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type InventoryChangeUUID = protocol.UUID

// ProductInventoryChange indicate the domain record data fields.
type ProductInventoryChange interface {
	InventoryChangeID() InventoryChangeUUID //
	ProductID() ProductUUID                 //
	From() BuildingLocationUUID             //
	To() BuildingLocationUUID               // Can be zero for voiding products.
	Amount() int64                          // this transaction
	Priority() uint64                       //
	// TODO::: Reference to invoice??
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductInventoryChange_StorageServices interface {
	Save(pi ProductInventoryChange) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(inventoryChangeID InventoryChangeUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(inventoryChangeID InventoryChangeUUID, vo protocol.VersionOffset) (pi ProductInventoryChange, nv protocol.NumberOfVersion, err protocol.Error)

	FindByProduct(productID ProductUUID, offset, limit uint64) (inventoryChangeIDs []InventoryChangeUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
