/* For license and copyright information please see the LEGAL file in the code repository */

package idp

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	ip "org/modules/invoice/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID        //
	DiscountID() dp.DiscountUUID      //
	Discounted() protocol.MoneyAmount //
	SaveTime() protocol.Time          //
	RequestID() urp.UserRequestUUID   //
}
