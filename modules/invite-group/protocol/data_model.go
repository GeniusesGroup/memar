/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InviteGroup indicate the domain record data fields.
type InviteGroup interface {
	InviteID() InviteUUID           //
	GroupID() GroupUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
