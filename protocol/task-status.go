/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// TaskStatus indicate the domain record data fields.
type TaskStatus interface {
	TaskID() TaskUUID           //
	Status() Task_Status        //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}

type Task_Status Quiddity_Status
