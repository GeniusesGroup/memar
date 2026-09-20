/* For license and copyright information please see the LEGAL file in the code repository */

package content_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_ContentUUID interface {
	ContentUUID() UUID
}

type UUID thing_p.UUID
