/* For license and copyright information please see the LEGAL file in the code repository */

package form_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_FormID interface {
	FormID() UUID
}

type UUID thing_p.UUID
