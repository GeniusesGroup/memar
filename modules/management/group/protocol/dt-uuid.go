/* For license and copyright information please see the LEGAL file in the code repository */

package group_p

import (
	user_p "org/modules/identity/user/protocol"
)

type Field_GroupID interface {
	GroupID() UUID
}

type Field_GroupsID interface {
	GroupsID() []UUID
}

type UUID user_p.UUID

// register group
