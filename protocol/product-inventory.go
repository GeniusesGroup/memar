/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductInventory indicate the domain record data fields.
// ProductInventory or good stock
type ProductInventory interface {
	ProductID() [16]byte                // product domain
	OrgID() protocol.UserID             // OwnerID
	BuildingLocationID() [16]byte       // building-location domain
	ReferenceID() [16]byte              // Depend on ReferenceType()
	ReferenceType() ProductInventory_RT //
	Amount() int64                      // this transaction
	Stock() int64                       // overall in each location
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}

type ProductInventory_StorageService interface {
	Save(p ProductInventory) (nv protocol.NumberOfVersion, err protocol.Error)

	Lock(productID, buildingLocationID [16]byte) (p ProductInventory, err protocol.Error)
	Unlock(p ProductInventory) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID, buildingLocationID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID, buildingLocationID [16]byte, vo protocol.VersionOffset) (p ProductInventory, nv protocol.NumberOfVersion, err protocol.Error)

	ListProductIDs(buildingLocationID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListBuildingLocationIDs(productID [16]byte, offset, limit uint64) (buildingLocationIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
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
