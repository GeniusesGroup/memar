/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Task indicate the comment record data fields.
type TaskParticipant interface {
	TaskID() TaskUUID           // quiddity domain. use to get and show locale title.
	UserID() protocol.UserID    // user-status domain
	Type() TaskParticipant_Type //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}

type TaskParticipant_Type uint8

const (
	TaskParticipant_Type_Unset TaskParticipant_Type = iota
	TaskParticipant_Type_Assigner
	TaskParticipant_Type_Assigned
	TaskParticipant_Type_Reviewer
)
