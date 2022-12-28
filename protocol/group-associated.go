/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// GroupAssociated indicate the domain record data fields
type GroupAssociated interface {
	GroupID() GroupUUID         // group domain
	UserID() protocol.UserID    // user domain
	JoinBy() protocol.UserID    // user domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
