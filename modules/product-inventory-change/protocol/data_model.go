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
	ProductID() pp.ProductUUID                   //
	From() eblp.BuildingLocationUUID             //
	To() eblp.BuildingLocationUUID               // Can be zero for voiding products.
	Amount() int64                               // this transaction
	Priority() uint64                            //
	// TODO::: Reference to invoice??
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
