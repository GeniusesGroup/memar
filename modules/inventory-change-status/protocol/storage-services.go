/* For license and copyright information please see the LEGAL file in the code repository */

package picsp

import (
	"libgo/protocol"

	picp "org/modules/product-inventory-change/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(inventoryChangeID picp.InventoryChangeUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(inventoryChangeID picp.InventoryChangeUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_InventoryChangeIDs_BY_Status(status Status, offset, limit uint64) (inventoryChangeIDs []picp.InventoryChangeUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
