/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductInventoryChangeStatus indicate the domain record data fields.
type ProductInventoryChangeStatus interface {
	InventoryChangeID() InventoryChangeUUID //
	Status() ProductInventoryChange_Status  // overall
	Time() protocol.Time                    // save time
	RequestID() urp.UserRequestUUID         //
}

type ProductInventoryChangeStatus_StorageServices interface {
	Save(dm ProductInventoryChangeStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(inventoryChangeID InventoryChangeUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(inventoryChangeID InventoryChangeUUID, vo protocol.VersionOffset) (dm ProductInventoryChangeStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_InventoryChangeIDs_BY_Status(status ProductInventoryChange_Status, offset, limit uint64) (inventoryChangeIDs []InventoryChangeUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type ProductInventoryChange_Status Quiddity_Status

// DC abbreviation for distribution-center or Warehouse
const (
	ProductInventoryChange_Status_OutcomeDCRequested = ProductInventoryChange_Status(Quiddity_Status_FreeFlag << iota)
	ProductInventoryChange_Status_IncomeDCRequested
	ProductInventoryChange_Status_OutcomeDCApproved
	ProductInventoryChange_Status_IncomeDCApproved
	ProductInventoryChange_Status_Void
)
