/* For license and copyright information please see the LEGAL file in the code repository */

package card_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_CardID interface {
	CardID() UUID
}

type UUID thing_p.UUID
