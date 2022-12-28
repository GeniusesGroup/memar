/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// PosProvider indicate the domain record data fields.
// Provider or operator is to limit pos to specific staffs.
type PosProvider interface {
	PosID() [16]byte            // pos domain
	RoleID() [16]byte           // role domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
