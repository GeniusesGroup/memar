/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProjectTask indicate the domain record data fields.
type ProjectTask interface {
	TaskID() [16]byte           //
	ProjectID() [16]byte        // project domain
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
