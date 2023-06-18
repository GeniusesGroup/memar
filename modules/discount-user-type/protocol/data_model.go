/* For license and copyright information please see the LEGAL file in the code repository */

package dutp

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	UserType() protocol.UserType    //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
