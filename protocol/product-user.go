/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductUser indicate the domain record data fields.
type ProductUser interface {
	SubscriptionID() ProductUUID //
	UserID() protocol.UserID     //
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}
