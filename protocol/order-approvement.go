/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// OrderApprovement indicate the domain record data fields.
type OrderApprovement interface {
	OrderID() OrderUUID                     //
	UserID() protocol.UserID               // user domain
	Status() OrderApprovement_Status
	Time() protocol.Time                   // save time
	RequestID() UserRequestUUID            // user-request domain
}

type OrderApprovement_Status uint8
