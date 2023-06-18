/* For license and copyright information please see the LEGAL file in the code repository */

package dvp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	Quantity() protocol.PerMyriad   // max discount percentage for each invoices, products, ... price
	Price() protocol.MoneyAmount    // max discount price can use for each invoices, product, ... price
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

