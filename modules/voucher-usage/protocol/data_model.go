/* For license and copyright information please see the LEGAL file in the code repository */

package vup

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	MaximumInvoice() uint64         //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
