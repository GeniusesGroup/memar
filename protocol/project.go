/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// Project indicate the domain record data fields.
type Project interface {
	ProjectID() [16]byte // group domain. use to get and show locale title.

	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
