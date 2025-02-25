/* For license and copyright information please see the LEGAL file in the code repository */

package status_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_StatusID interface {
	StatusID() UUID
}

type UUID quiddity_p.UUID
