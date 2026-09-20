/* For license and copyright information please see the LEGAL file in the code repository */

package task_p

import (
	group_p "org/modules/management/group/protocol"
)

type Field_TaskID interface {
	TaskID() UUID
}

type Field_TasksID interface {
	TasksID() []UUID
}

// It is base on group to support some group rules e.g. invite, ...
type UUID group_p.UUID
