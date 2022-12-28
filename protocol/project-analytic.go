/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// ProjectAnalytic indicate the domain record data fields.
type ProjectAnalytic interface {
	ProjectID() ProjectUUID // project domain
	Day() utc.DayElapsed    //

	TotalTasks() uint64      //
	CompletedTasks() uint64  //
	RejectedTasks() uint64   //
	Progress() uint64        //
	TaskOverDueTime() uint64 // due time

	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
