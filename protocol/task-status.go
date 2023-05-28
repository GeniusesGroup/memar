/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskStatus indicate the domain record data fields.
type TaskStatus interface {
	TaskID() TaskUUID               //
	Status() Task_Status            //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type TaskStatus_StorageServices interface {
	Save(f TaskStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID TaskUUID, vo protocol.VersionOffset) (f TaskStatus, nv protocol.NumberOfVersion, err protocol.Error)
}

type Task_Status Quiddity_Status

const (
	Task_Status_ReadyForDevelopment = Task_Status(Quiddity_Status_FreeFlag << iota)
	Task_Status_InProgress
	Task_Status_Close
	Task_Status_Success
)
