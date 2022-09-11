/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// InviteUsable indicate the domain record data fields.
type InviteUsable interface {
	InviteID() InviteUUID       //
	UserID() protocol.UserID    // user domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
