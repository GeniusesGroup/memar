/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InviteConsumer indicate the domain record data fields.
type InviteConsumer interface {
	InviteID() InviteUUID           //
	PermitUsageID() UserUUID        //
	ConsumerID() UserUUID           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
