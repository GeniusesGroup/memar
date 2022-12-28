/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// StaffScore or staff grade
type StaffScore interface {
	StaffID() [16]byte          // staff domain
	Score() uint64              //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
