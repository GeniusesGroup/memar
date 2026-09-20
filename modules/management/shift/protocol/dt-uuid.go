/* For license and copyright information please see the LEGAL file in the code repository */

package shift_p

import (
	task_p "org/modules/management/task/protocol"
)

type Field_ShiftID interface {
	ShiftID() UUID
}

type UUID task_p.UUID
