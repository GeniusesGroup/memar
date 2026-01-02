/* For license and copyright information please see the LEGAL file in the code repository */

package gender_p

import (
	label_p "org/modules/knowledge/label/protocol"
)

// Field_GenderID use when need to indicate the living thing gender
type Field_GenderID interface {
	GenderID() UUID
}

type UUID label_p.UUID
