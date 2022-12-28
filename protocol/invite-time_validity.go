/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InviteTimeValidity indicate the domain record data fields.
type InviteTimeValidity interface {
	InviteID() InviteUUID       //
	Start() protocol.Time       //
	End() protocol.Time         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
