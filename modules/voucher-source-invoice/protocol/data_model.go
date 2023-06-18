/* For license and copyright information please see the LEGAL file in the code repository */

package vsip

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	InvoiceID() ip.InvoiceUUID      //
	InvoiceType() Type              //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_PastCompleted
	Type_HurryToBuying
	Type_BackToBuy
)
