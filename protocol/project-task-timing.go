/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProjectTaskTiming indicate the domain record data fields.
type ProjectTaskTiming interface {
	TaskID() [16]byte            // project-task domain
	ExpectedTime() protocol.Time //
	Deadline() protocol.Time     //
	Time() protocol.Time         // Save time
	RequestID() UserRequestUUID  // user-request domain
}
