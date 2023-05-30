/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleSkill indicate the domain record data fields.
type RoleSkill interface {
	RoleID() RoleUUID //

	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
