/* For license and copyright information please see the LEGAL file in the code repository */

package group_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_GroupID interface {
	GroupID() GroupUUID
}

type GroupUUID ut16.UUID

// register group
