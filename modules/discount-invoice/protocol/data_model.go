/* For license and copyright information please see the LEGAL file in the code repository */

package dip

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	MinPrice() protocol.MoneyAmount // Minimum invoice price
	MinAmount() uint64              // Minimum invoice product numbers
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

