/* For license and copyright information please see the LEGAL file in the code repository */

package dvp

import (
	"memar/math/per"
	"memar/protocol"

	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	Quantity() per.Myriad        // max discount percentage for each invoices, products, ... price
	Price() protocol.MoneyAmount // max discount price can use for each invoices, product, ... price

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
