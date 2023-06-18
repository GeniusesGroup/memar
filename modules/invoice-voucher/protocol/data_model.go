/* For license and copyright information please see the LEGAL file in the code repository */

package ivp

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// This domain will let users redeem their vouchers and track vouchers rules.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID        //
	VoucherID() vp.VoucherUUID        //
	Discounted() protocol.MoneyAmount //
	SaveTime() protocol.Time          //
	RequestID() urp.UserRequestUUID   //
}


