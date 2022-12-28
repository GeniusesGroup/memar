/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ContentSubstitute interface {
	ContentID() [16]byte        // content domain
	Priority() uint64           // substitute priority
	SubstituteID() [16]byte     // content domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
