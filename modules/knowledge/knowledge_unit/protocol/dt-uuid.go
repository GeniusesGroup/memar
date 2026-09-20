/* For license and copyright information please see the LEGAL file in the code repository */

package knowledge_unit_p

import (
	text_p "org/modules/knowledge/text/protocol"
)

type Field_KnowledgeUnitID interface {
	KnowledgeUnitID() UUID
}

type UUID text_p.UUID
