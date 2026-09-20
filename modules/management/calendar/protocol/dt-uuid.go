/* For license and copyright information please see the LEGAL file in the code repository */

package calendar_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_CalendarID interface {
	CalendarID() UUID
}

// Usually it is some other domains UUID
// e.g. `invoice`, `form`, `department`, `role`, `task`, `user`, `production`, `batch`, ...
type UUID thing_p.UUID
