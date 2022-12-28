/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InviteGroup indicate the domain record data fields.
type InviteGroup interface {
	InviteID() InviteUUID       //
	GroupID() GroupUUID         // group domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
