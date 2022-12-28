/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ContentComplement interface {
	ContentID() [16]byte        // content domain
	Priority() uint64            // complement priority
	ComplementID() [16]byte     // content domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
