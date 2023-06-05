/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskRelationGroup indicate the Task-Relation-Group record data fields.
// Group here can treated as a team work on a task.
type TaskRelationGroup interface {
	TaskID() TaskUUID                     //
	GroupID() GroupUUID                   //
	RelationType() TaskRelationGroup_Type //
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       //
}

type TaskRelationGroup_StorageServices interface {
	Save(dm TaskRelationGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID, taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, taskID TaskUUID, vo protocol.VersionOffset) (dm TaskRelationGroup, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_TaskIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (taskIDs []TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_GroupIDs_BY_TaskID(taskID TaskUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type TaskRelationGroup_Type uint8

const (
	TaskRelationGroup_Type_Unset TaskRelationGroup_Type = iota
	TaskRelationGroup_Type_Assigned
	TaskRelationGroup_Type_Reviewer
)
