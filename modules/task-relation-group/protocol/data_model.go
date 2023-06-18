/* For license and copyright information please see the LEGAL file in the code repository */

package trgp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the Task-Relation-Group record data fields.
// Group here can treated as a team work on a task.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	GroupID() gp.GroupUUID          //
	RelationType() Type             //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Assigned
	Type_Reviewer
)
