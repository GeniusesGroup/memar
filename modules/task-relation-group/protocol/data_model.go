/* For license and copyright information please see the LEGAL file in the code repository */

package trgp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	tp "org/modules/task/protocol"
)

// DataModel indicate the Task-Relation-Group record data fields.
// Group here can treated as a team work on a task.
type DataModel interface {
	TaskID() tp.TaskUUID
	GroupID() gp.GroupUUID
	RelationType() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
