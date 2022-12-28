/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type TaskUUID = protocol.UUID

// Task indicate the domain record data fields.
type Task interface {
	TaskID() TaskUUID           //
	ProjectID() ProjectUUID     // project domain
	Priority() uint64           //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
