/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskRelationTask indicate the domain record data fields.
type TaskRelationTask interface {
	TaskID() TaskUUID               //
	OtherID() TaskUUID              //
	Priority() uint64               //
	Type() TaskRelationTask_Type    //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type TaskRelationTask_Type uint8

// TaskBlocking
