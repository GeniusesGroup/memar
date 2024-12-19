/* For license and copyright information please see the LEGAL file in the code repository */

package task_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_TaskID interface {
	TaskID() UUID
}

type Field_TasksID interface {
	TasksID() []UUID
}

type UUID quiddity_p.UUID
