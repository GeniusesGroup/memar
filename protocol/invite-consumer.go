/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InviteConsumer indicate the domain record data fields.
type InviteConsumer interface {
	InviteID() InviteUUID           //
	PermitUsageID() protocol.UserID //
	ConsumerID() protocol.UserID    // user domain
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}
