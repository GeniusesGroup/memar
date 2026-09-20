/* For license and copyright information please see the LEGAL file in the code repository */

package role_p

import (
	group_p "org/modules/management/group/protocol"
)

type Field_RoleID interface {
	RoleID() UUID
}

type UUID group_p.UUID
