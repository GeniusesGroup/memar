/* For license and copyright information please see the LEGAL file in the code repository */

package meeting_p

import (
	task_p "org/modules/management/task/protocol"
)

type Field_MeetingID interface {
	MeetingID() UUID
}

type Field_MeetingsID interface {
	MeetingsID() []UUID
}

type UUID task_p.UUID
