/* For license and copyright information please see the LEGAL file in the code repository */

package irlp

import (
	"memar/protocol"

	ip "org/modules/inventory/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// ProductInventory or good stock
type DataModel interface {
	InventoryID() ip.InventoryUUID
	ProductID() pp.ProductUUID
	// OwnerID() op.OrgUUID		here or product-relation-product

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
