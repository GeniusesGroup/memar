/* For license and copyright information please see the LEGAL file in the code repository */

package otp

import (
	"memar/protocol"

	op "org/modules/order/protocol"
)

// DataModel indicate the invoice order-trade record data fields.
// can be zero to prevent sell on profit(cover order) or stopping loss
type DataModel interface {
	OrderID() op.OrderUUID
	Level() uint8                    // usually 3 level trade order
	HighPrice() protocol.MoneyAmount // SaveProfit	e.g. 45$ , -102$
	LowPrice() protocol.MoneyAmount  // StopLoss	e.g. 43$ , -95$
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
