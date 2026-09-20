/* For license and copyright information please see the LEGAL file in the code repository */

package object_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_ObjectUUID interface {
	ObjectUUID() UUID
}

type Field_ObjectsUUID interface {
	ObjectsUUID() []UUID
}

// It is
type UUID record_p.UUID
