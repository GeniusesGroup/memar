/* For license and copyright information please see the LEGAL file in the code repository */

package timeline_p

import (
	group_p "org/modules/management/group/protocol"
)

type Field_TimelineID interface {
	TimelineID() UUID
}

type Field_TimelinesID interface {
	TimelinesID() []UUID
}

type UUID group_p.UUID
