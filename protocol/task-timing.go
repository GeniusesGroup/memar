/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// TaskTiming indicate the domain record data fields.
type TaskTiming interface {
	TaskID() TaskUUID            //s
	ExpectedTime() protocol.Time //
	Deadline() protocol.Time     //
	Time() protocol.Time         // Save time
	RequestID() UserRequestUUID  // user-request domain
}
