/* For license and copyright information please see the LEGAL file in the code repository */

/*
- product can limit to sell one some physical branch or online store.
*/
package org

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
)

type DataModel interface {
	ProductID() pp.ProductUUID
	BranchID()
	ProviderWarehouse() // TODO::: each product or branch??
	MinStock()
	MaxStock()

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
