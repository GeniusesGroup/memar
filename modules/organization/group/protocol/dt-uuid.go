/* For license and copyright information please see the LEGAL file in the code repository */

package group_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_GroupID interface {
	GroupID() UUID
}

type Field_GroupsID interface {
	GroupsID() []UUID
}

type UUID quiddity_p.UUID

// register group
