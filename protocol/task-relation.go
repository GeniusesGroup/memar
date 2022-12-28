/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// TaskRelation indicate the domain record data fields.
type TaskRelation interface {
	TaskID() TaskUUID           //
	OtherID() TaskUUID          //
	Priority() uint64           //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
