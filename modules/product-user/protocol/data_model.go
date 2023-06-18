/* For license and copyright information please see the LEGAL file in the code repository */

package pup

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SubscriptionID() pp.ProductUUID //
	UserID() up.UserUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
