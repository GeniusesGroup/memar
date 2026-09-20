/* For license and copyright information please see the LEGAL file in the code repository */

package template_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_UUID interface {
	TemplateID() UUID
}

type UUID thing_p.UUID
