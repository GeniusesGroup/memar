/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductUser indicate the domain record data fields.
type ProductUser interface {
	SubscriptionID() ProductUUID    //
	UserID() UserUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
