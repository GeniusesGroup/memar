/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// TODO::: user-number??
type StaffID interface {
	StaffUUID() [16]byte        // user domain
	ID() uint32                 //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
