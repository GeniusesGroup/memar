/* For license and copyright information please see the LEGAL file in the code repository */

package dtvp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel or LiveUntil indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	Start() protocol.Time           //
	End() protocol.Time             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

