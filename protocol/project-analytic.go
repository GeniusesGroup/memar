/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

// ProjectAnalytic indicate the domain record data fields.
type ProjectAnalytic interface {
	ProjectID() ProjectUUID //
	Day() utc.DayElapsed    //

	TotalTasks() uint64      //
	CompletedTasks() uint64  //
	RejectedTasks() uint64   //
	Progress() uint64        //
	TaskOverDueTime() uint64 // due time

	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type ProjectAnalytic_StorageServices interface {
	Save(dm ProjectAnalytic) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, vo protocol.VersionOffset) (dm ProjectAnalytic, nv protocol.NumberOfVersion, err protocol.Error)
}
