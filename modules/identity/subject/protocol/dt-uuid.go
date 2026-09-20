/* For license and copyright information please see the LEGAL file in the code repository */

package subject_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_SubjectUUID interface {
	SubjectUUID() UUID
}

type Field_SubjectsUUID interface {
	SubjectsUUID() []UUID
}

// It is the base identifier for any thing that is not `object`
type UUID record_p.UUID
