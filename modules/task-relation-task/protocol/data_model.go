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
	RequestID() urp.UserRequestUUID //
}

type TaskRelationTask_StorageServices interface {
	Save(dm TaskRelationTask) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(otherID TaskUUID, taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(otherID TaskUUID, taskID TaskUUID, vo protocol.VersionOffset) (dm TaskRelationTask, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_OtherIDs_BY_TaskID(taskID TaskUUID, offset, limit uint64) (otherIDs []TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_TaskIDs_BY_OtherID(otherID TaskUUID, offset, limit uint64) (taskIDs []TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type TaskRelationTask_Type uint8

const (
	TaskRelationTask_Type_Unset      TaskRelationTask_Type = 0
	TaskRelationTask_Type_Complement TaskRelationTask_Type = (1 << iota)
	TaskRelationTask_Type_Blocking
)
