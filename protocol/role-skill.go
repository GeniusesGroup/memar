/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// RoleSkill indicate the domain record data fields.
type RoleSkill interface {
	RoleID() [16]byte // role domain

	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
