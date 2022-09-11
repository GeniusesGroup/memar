/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// each metrics for a thing is immutable record and so use version mechanism to chain metrics for a device.
type Temperature interface {
	ThingID() [16]byte
	Amount() int64
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
