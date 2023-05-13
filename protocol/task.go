/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	
	urp "org/modules/user-request/protocol"
)

type TaskUUID = protocol.UUID

// Task indicate the domain record data fields.
type Task interface {
	TaskID() TaskUUID               //
	UserID() protocol.UserID        //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}
