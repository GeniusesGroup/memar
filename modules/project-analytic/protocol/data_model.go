/* For license and copyright information please see the LEGAL file in the code repository */

package pap

import (
	"libgo/protocol"
	"libgo/time/utc"

	pp "org/modules/project/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID //
	Day() utc.DayElapsed       //

	TotalTasks() uint64      //
	CompletedTasks() uint64  //
	RejectedTasks() uint64   //
	Progress() uint64        //
	TaskOverDueTime() uint64 // due time

	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}
