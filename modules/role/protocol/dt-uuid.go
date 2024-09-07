/* For license and copyright information please see the LEGAL file in the code repository */

package role_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_RoleID interface {
	RoleID() RoleUUID
}

type RoleUUID ut16.UUID
