/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskRelationProject indicate the domain record data fields.
type TaskRelationProject interface {
	TaskID() TaskUUID               //
	ProjectID() ProjectUUID         //
	Priority() uint64               //
	Permyriad() protocol.PerMyriad  // 0 means unset e.g. equal to other tasks in the project
	Type() TaskRelationProject_Type //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type TaskRelationProject_StorageServices interface {
	Save(f TaskRelationProject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID,taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID ,taskID TaskUUID, vo protocol.VersionOffset) (f TaskRelationProject, nv protocol.NumberOfVersion, err protocol.Error)
}


type TaskRelationProject_Type uint32

const (
	TaskRelationProject_Type_Unset TaskRelationProject_Type = 0

	TaskRelationProject_Type_Blocking TaskRelationProject_Type = (1 << iota) // stuck
	TaskRelationProject_Type_Move                                            // move from other project

	TaskRelationProject_Type_Parent
	TaskRelationProject_Type_
)
