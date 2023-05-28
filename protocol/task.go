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
	UserID() UserUUID               //
	Type() Task_Type                //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}


type Task_StorageServices interface {
	Save(f Task) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID TaskUUID, vo protocol.VersionOffset) (f Task, nv protocol.NumberOfVersion, err protocol.Error)
}


type Task_Type uint8

const (
	Task_Type_Unset Task_Type = iota
	Task_Type_TimeBased
	Task_Type_Repetitive
)
