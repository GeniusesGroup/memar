/* For license and copyright information please see the LEGAL file in the code repository */

package qcu_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_CountUnitID interface {
	// Hz, core, gram, liter, ...
	CountUnitID() quiddity_p.UUID
}
