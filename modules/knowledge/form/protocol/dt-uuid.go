/* For license and copyright information please see the LEGAL file in the code repository */

package form_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_FormID interface {
	FormID() UUID
}

type UUID quiddity_p.UUID
