/* For license and copyright information please see the LEGAL file in the code repository */

package count_unit_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_CountUnitID interface {
	// Hz, core, gram, liter, ...
	CountUnitID() UUID
}

type UUID quiddity_p.UUID
