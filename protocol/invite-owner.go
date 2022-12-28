/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InviteOwner indicate the domain record data fields.
type InviteOwner interface {
	InviteID() InviteUUID       //
	IssuerID() protocol.UserID  // user domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
