/* For license and copyright information please see the LEGAL file in the code repository */

/*
- product can limit to sell one some physical branch or online store.
*/
package org

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ProductID() pp.ProductUUID
	BranchID()
	ProviderWarehouse() // TODO::: each product or branch??
	MinStock()
	MaxStock()
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
