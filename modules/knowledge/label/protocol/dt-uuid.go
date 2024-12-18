/* For license and copyright information please see the LEGAL file in the code repository */

package label_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_LabelID interface {
	LabelID() UUID
}

type Field_LabelsID interface {
	LabelsID() []UUID
}

type Field_Type interface {
	Type() UUID
}

// Label text indicate in `text` domain.
type UUID quiddity_p.UUID
