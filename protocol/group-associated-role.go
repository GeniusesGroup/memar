/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// GroupAssociatedRole indicate the domain record data fields.
type GroupAssociatedRole interface {
	GroupID() [16]byte          // group domain
	UserID() protocol.UserID    // user domain
	RoleID() [16]byte           // role domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
