/* For license and copyright information please see the LEGAL file in the code repository */

package dup

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	UserID() up.UserUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

