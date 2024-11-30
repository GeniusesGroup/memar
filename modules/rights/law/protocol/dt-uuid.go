/* For license and copyright information please see the LEGAL file in the code repository */

package law_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_LawID interface {
	LawID() UUID
}

// UUID use to track changes in a law
type UUID quiddity_p.UUID
