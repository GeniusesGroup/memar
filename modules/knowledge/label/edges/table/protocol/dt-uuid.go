/* For license and copyright information please see the LEGAL file in the code repository */

package lt_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_TableID interface {
	TableID() UUID
}

type UUID quiddity_p.UUID
