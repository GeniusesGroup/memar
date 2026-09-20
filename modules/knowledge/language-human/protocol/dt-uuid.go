/* For license and copyright information please see the LEGAL file in the code repository */

package language_p

import (
	label_p "org/modules/knowledge/label/protocol"
)

type Field_LanguageUUID interface {
	LanguageUUID() UUID
}

type UUID label_p.UUID
