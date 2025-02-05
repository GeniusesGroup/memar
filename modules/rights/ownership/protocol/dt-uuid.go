/* For license and copyright information please see the LEGAL file in the code repository */

package ownership_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_OwnershipID interface {
	OwnershipID() UUID
}

type UUID quiddity_p.UUID
