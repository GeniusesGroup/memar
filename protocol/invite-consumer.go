/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// InviteConsumer indicate the domain record data fields.
type InviteConsumer interface {
	InviteID() InviteUUID           //
	PermitUsageID() up.UserUUID     //
	ConsumerID() up.UserUUID        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
