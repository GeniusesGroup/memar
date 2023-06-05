/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskTiming indicate the domain record data fields.
type TaskTiming interface {
	TaskID() TaskUUID               //
	ExpectedTime() protocol.Time    //
	Deadline() protocol.Time        //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type TaskTiming_StorageServices interface {
	Save(dm TaskTiming) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID TaskUUID, vo protocol.VersionOffset) (dm TaskTiming, nv protocol.NumberOfVersion, err protocol.Error)
}
