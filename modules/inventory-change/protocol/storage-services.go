/* For license and copyright information please see the LEGAL file in the code repository */

package icp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(inventoryChangeID InventoryChangeUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(inventoryChangeID InventoryChangeUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InventoryChangeIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (inventoryChangeIDs []InventoryChangeUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
