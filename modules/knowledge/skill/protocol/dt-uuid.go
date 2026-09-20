/* For license and copyright information please see the LEGAL file in the code repository */

package skill_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_SkillID interface {
	SkillID() UUID
}

// UUID
type UUID thing_p.UUID
