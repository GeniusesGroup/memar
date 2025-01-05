/* For license and copyright information please see the LEGAL file in the code repository */

package pos_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_PosID interface {
	PosID() UUID
}

// Used quiddity UUID to set title, ...
type UUID quiddity_p.UUID
