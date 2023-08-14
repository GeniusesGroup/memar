/* For license and copyright information please see the LEGAL file in the code repository */

package icp

import (
	"memar/protocol"

	ilp "org/modules/inventory-lot/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryChangeID() InventoryChangeUUID
	ProductID() pp.ProductUUID
	From() ilp.LotUUID
	To() ilp.LotUUID // Can be zero for voiding products.
	Amount() int64   // this transaction
	Priority() uint64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
