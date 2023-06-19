/* For license and copyright information please see the LEGAL file in the code repository */

package picp

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryChangeID() InventoryChangeUUID //
	ProductID() pp.ProductUUID              //
	From() eblp.BuildingLocationUUID        //
	To() eblp.BuildingLocationUUID          // Can be zero for voiding products.
	ReferenceID() protocol.UUID             // Depend on ReferenceType()
	ReferenceType() ProductInventory_RT     //
	Amount() int64                          // this transaction
	Priority() uint64                       //
	SaveTime() protocol.Time                //
	RequestID() urp.UserRequestUUID         //
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
