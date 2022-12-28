/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Skill indicate the domain record data fields.
type Skill interface {
	SkillID() [16]byte //

	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
