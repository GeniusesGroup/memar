/* For license and copyright information please see the LEGAL file in the code repository */

package production_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_ProductionID interface {
	ProductionID() UUID
}

type UUID quiddity_p.UUID
