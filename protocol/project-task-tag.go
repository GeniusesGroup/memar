/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProjectTaskTag indicate the domain record data fields.
type ProjectTaskTag interface {
	TaskID() [16]byte    // task domain
	Tag() [16]byte       // project-tags domain
	Time() protocol.Time // Save time
}
