/* For license and copyright information please see the LEGAL file in the code repository */

package dpp

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
	pp "org/modules/product/protocol"
)

// DataModel or product sale indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	ProductID() pp.ProductUUID
	MinAmount() uint64              // Minimum number to buy to use discount
	MaxAmount() uint64              // Maximum number to buy to use discount
	MinPrice() protocol.MoneyAmount // Minimum price to buy to use discount
	MinStock() uint64               // 0 for unlimited until related product exist to sell
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
