/* For license and copyright information please see the LEGAL file in the code repository */

package pip

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	org "org/modules/org/protocol"
	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// TODO::: why not relate to ProductInventoryChange domain??

// DataModel indicate the domain record data fields.
// DataModel or good stock
type DataModel interface {
	ProductID() pp.ProductUUID                     //
	OrgID() org.OrgUUID                            // OwnerID
	BuildingLocationID() eblp.BuildingLocationUUID //
	ReferenceID() [16]byte                         // Depend on ReferenceType()
	ReferenceType() ProductInventory_RT            //
	Amount() int64                                 // this transaction
	Stock() int64                                  // overall in each location
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
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
