/* For license and copyright information please see the LEGAL file in the code repository */

package icp

import (
	"memar/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryChangeID() InventoryChangeUUID
	ProductID() pp.ProductUUID
	From() eblp.BuildingLocationUUID
	To() eblp.BuildingLocationUUID // Can be zero for voiding products.
	ReferenceID() protocol.UUID    // Depend on ReferenceType()
	ReferenceType() ReferenceType
	Amount() int64 // this transaction
	Priority() uint64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
