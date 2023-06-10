/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: why not relate to ProductInventoryChange domain??

// ProductInventory indicate the domain record data fields.
// ProductInventory or good stock
type ProductInventory interface {
	ProductID() ProductUUID                   //
	OrgID() OrgUUID                           // OwnerID
	BuildingLocationID() BuildingLocationUUID //
	ReferenceID() [16]byte                    // Depend on ReferenceType()
	ReferenceType() ProductInventory_RT       //
	Amount() int64                            // this transaction
	Stock() int64                             // overall in each location
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type ProductInventory_StorageService interface {
	// Save(p ProductInventory) (nv protocol.NumberOfVersion, err protocol.Error)

	Lock(productID ProductUUID, buildingLocationID BuildingLocationUUID) (p ProductInventory, err protocol.Error)
	Unlock(p ProductInventory) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, buildingLocationID BuildingLocationUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, buildingLocationID BuildingLocationUUID, vo protocol.VersionOffset) (f ProductInventory, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_BuildingLocationID(buildingLocationID BuildingLocationUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_BuildingLocationIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (buildingLocationIDs []BuildingLocationUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductInventory_RT uint8

const (
	ProductInventory_RT_Unset        ProductInventory_RT = iota
	ProductInventory_RT_Production                       // ProductionID
	ProductInventory_RT_Invoice                          // InvoiceID
	ProductInventory_RT_Order                            // ProductOrderID
	ProductInventory_RT_Transfer                         // ProductInventoryChangeID
	ProductInventory_RT_ChangeOwner                      // UserID
	ProductInventory_RT_SplitProduct                     // Split to small size product || Split from upper size product
	ProductInventory_RT_Void                             //
	// ProductInventory_RT_
)
