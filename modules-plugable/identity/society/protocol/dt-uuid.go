/* For license and copyright information please see the LEGAL file in the code repository */

package society_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_SocietyUUID interface {
	SocietyUUID() UUID
}

type UUID thing_p.UUID
