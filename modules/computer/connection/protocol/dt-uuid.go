/* For license and copyright information please see the LEGAL file in the code repository */

package connection_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_ConnectionID interface {
	ConnectionID() UUID
}

type UUID quiddity_p.UUID
