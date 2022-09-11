/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// QuiddityIcon indicate the domain record data fields.
// Icon or emoji use in many domains e.g. category, departments, ...
type QuiddityIcon interface {
	QuiddityID() [16]byte       // quiddity domain
	Icon() [16]byte             // object domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
