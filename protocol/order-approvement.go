/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// OrderApprovement indicate the domain record data fields.
type OrderApprovement interface {
	OrderID() OrderUUID              //
	UserID() UserUUID                //
	Status() OrderApprovement_Status //
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}

type OrderApprovement_Status uint8
