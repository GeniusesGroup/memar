/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProjectList indicate the domain record data fields.
type ProjectTag interface {
	ProjectID() [16]byte        // Project domain
	Tag() [16]byte              // project-tags domain
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
