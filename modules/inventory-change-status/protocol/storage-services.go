/* For license and copyright information please see the LEGAL file in the code repository */

package icsp

import (
	"memar/protocol"

	icp "org/modules/inventory-change/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(inventoryChangeID icp.InventoryChangeUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(inventoryChangeID icp.InventoryChangeUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_InventoryChangeIDs_BY_Status(status Status, offset, limit uint64) (inventoryChangeIDs []icp.InventoryChangeUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
