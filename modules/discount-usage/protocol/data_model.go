/* For license and copyright information please see the LEGAL file in the code repository */

package dup

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	MaximumInvoice() uint64         //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

